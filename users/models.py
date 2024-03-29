import datetime

from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

def get_profile_picture_upload_path(self, filename):
	return 'profiles/profile_{}/profile_picture.jpg'.format(self.username)

class Profile(AbstractUser):
	'''
	Registered Rapchat User
	'''

	# #The django auth user
	# user = models.OneToOneField(
	# 	User,
	# 	null = False
	# )

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

	modified_at = models.DateTimeField(
		auto_now = True,
		blank = True,
		null = True
	)

	# objects = UserManager()


	def get_profile_picture_url(self, profile):
		return profile.profile_picture.url

	def get_token(self):
		return Token.objects.get(user=self)

	def friend_requests_pending_my_response(self):
		requests = FriendRequest.objects.filter(requested=self, is_accepted=False).all()
		return [elem for elem in requests]

	def friend_requests_pending_their_response(self):
		requests = FriendRequest.objects.filter(sender=self, is_accepted=False).all()
		return [elem for elem in requests]

	def send_friend_request(self, requested):
		FriendRequest.objects.create(
			sender = self,
			requested = requested,
			is_accepted = False
		)

	def accept_friend_request(self, sender):
		request = FriendRequest.objects.get(
			sender = sender,
			requested = self,
			is_accepted = False
		)
		request.is_accepted = True
		request.save()
		self.friends.add(sender)
		return request

	def decline_friend_request(self, sender):
		request = FriendRequest.objects.get(
			sender = sender,
			requested = self,
			is_accepted = False
		)
		request.delete()
		return request

	def remove_friend(self, username):
		# friend = self.friends.objects.get(username=username)
		friend = Profile.objects.get(username=username)
		self.friends.remove(friend)
		print 'Removed Friend {}'.format(friend.username)
		return friend

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
		return 'Profile {}: {}'.format(self.pk, self.username)



class FriendRequest(models.Model):
	'''
	Rapchat friend request model
	'''

	sender = models.ForeignKey(
		Profile,
		related_name='request_sender_set'
	)
	requested = models.ForeignKey(
		Profile,
		related_name='request_receiver_set'
	)
	is_accepted = models.BooleanField(
		default= False
	)
	created_at = models.DateTimeField(
		auto_now_add = True,
		null=True,
		blank=True
	)
	modified_at = models.DateTimeField(
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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)