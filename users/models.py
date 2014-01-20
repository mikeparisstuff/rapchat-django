import datetime

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

class Profile(models.Model):
	'''
	Registered Rapchat User
	'''

	#The django auth user
	user = models.OneToOneField(
		User,
		null = False
	)

	def get_profile_picture_upload_path(self, filename):
		return 'profiles/profile_{}/profile_picture.jpg'.format(self.session.id, self.clip_num)

	profile_picture = models.FileField(
		upload_to=get_profile_picture_upload_path,
		null = True,
		blank = True
	)

	friends = models.ManyToManyField(
		'self'
	)

	phone_number = models.CharField(
		max_length = 15
	)


	def get_profile_picture_url(self, profile):
		return profile.profile_picture.url

	def get_token(self):
		return Token.objects.get(user=self.user)

	def friend_requests_pending_my_response(self):
		requests = FriendRequest.objects.filter(requested=self.user, is_accepted=False).all()
		return [elem for elem in requests]

	def friend_requests_pending_their_response(self):
		requests = FriendRequest.objects.filter(sender=self.user, is_accepted=False).all()
		return [elem for elem in requests]

	def send_friend_request(self, requested):
		FriendRequest.objects.create(
			sender = self.user,
			requested = requested.user,
			is_accepted = False
		)

	def accept_friend_request(self, sender):
		request = FriendRequest.objects.get(
			sender = sender.user,
			requested = self.user
		)
		request.is_accepted = True
		request.save()
		self.friends.add(sender)

	def decline_friend_request(self, sender):
		request = FriendRequest.objects.get(
			sender = sender.user,
			requested = self.user
		)
		request.delete()

	def get_num_friends(self):
		return self.friends.all().count()

	def get_num_raps(self):
		return self.clip_set.all().count()

	def get_num_likes(self):
		return self.like_set.all().count()

	def get_likes(self):
		return self.like_set.all().order_by('-created')

	def get_liked_sessions(self):
		likes = self.like_set.all()
		print 'Get liked sessions'
		sessions = [like.session for like in likes];
		return sessions

	def __unicode__(self):
		return 'Profile {}: {}'.format(self.pk, self.user.username)



class FriendRequest(models.Model):
	'''
	Rapchat friend request model
	'''

	sender = models.ForeignKey(
		User,
		related_name='request_sender_set'
	)
	requested = models.ForeignKey(
		User,
		related_name='request_receiver_set'
	)
	is_accepted = models.BooleanField(
		default= False
	)
	created = models.DateTimeField(
		auto_now_add = True,
		null=True,
		blank=True
	)
	modified = models.DateTimeField(
		auto_now = True,
		null=True,
		blank=True
	)

# class Friend(models.Model):
# 	'''
# 	Rapchat friend model
# 	'''
# 	creator = models.ForeignKey(
# 		User,
# 		related_name='friend_creator_set'
# 	)

# 	friend = models.ForeignKey(
# 		User,
# 		related_name='friend_set'
# 	)

# 	created = models.BooleanField(
# 		auto_now_add = True
# 	)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)