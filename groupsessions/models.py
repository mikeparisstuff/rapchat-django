from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime

from users.models import Profile



################################ GROUP SESSIONS ##################################

class GroupSession(models.Model):
	'''
	Rapchat Session Model
	'''

	title = models.CharField(
		max_length=100
	)

	is_complete = models.BooleanField(
		default=False
	)

	session_creator = models.ForeignKey(
		Profile,
		related_name='session_creator_set',
		blank = True,
		null = True,
		default = None
	)

	# Populated only if it is a battle
	session_receiver = models.ForeignKey(
		Profile,
		related_name='battle_receiver_set',
		blank = True,
		null = True,
		default = None
	)

	is_battle = models.BooleanField(
		default = False
	)

	# video_url = models.URLField(
	# 	default = '',
	# 	blank = True,
	# 	null = True
	# )

	created = models.DateTimeField(
		auto_now_add = True,
		blank = True,
		null = True
	)

	modified = models.DateTimeField(
		auto_now = True,
		blank = True,
		null = True
	)

	def get_round(self):
		# Could be costly.. Maybe keep running tally
		return (self.num_clips() / 2) + 1

	def num_likes(self):
		return self.like_set.count()

	def num_clips(self):
		return self.clip_set.count()

	def get_comments(self):
		return self.comment_set.all().order_by('created')

	def get_clips(self):
		return self.clip_set.all().order_by('created')

	def most_recent_clip(self):
		try:
			return self.clip_set.latest('created')
		except Clip.DoesNotExist:
			return None

	def __unicode__(self):
		return 'Session: {}'.format(self.title)



class Clip(models.Model):
	'''
	Rapchat Music Clip
	'''

	# duration = models.IntegerField()

	clip_num = models.IntegerField(
		default = 1
	)

	creator = models.ForeignKey(
		Profile
	)

	session = models.ForeignKey(
		GroupSession
	)
	
	def get_clip_upload_path(self, filename):
		return 'sessions/session_{}/clip_{}.mp4'.format(self.session.id, self.clip_num)

	def get_thumbnail_upload_path(self, filename):
		return 'sessions/session_{}/thumbnail_{}.jpg'.format(self.session.id, self.clip_num)

	def get_url(self, clip):
		return clip.clip.url

	clip = models.FileField(
		upload_to=get_clip_upload_path
	)

	thumbnail = models.FileField(
		upload_to=get_thumbnail_upload_path,
		null = True,
		blank = True
	)

	created = models.DateTimeField(
		auto_now_add = True,
		blank = True,
		null = True
	)

	modified = models.DateTimeField(
		auto_now_add = True,
		blank = True,
		null = True
	)

@receiver(post_save, sender=Clip)
def update_session_modified_timestamp(sender, instance=None, created=False, **kwargs):
	if created and instance:
		print 'Updating modified timestamp on session: {}'.format(instance.session.pk)
		instance.session.save()


class Comment(models.Model):
	'''
	Rapchat Comment Model
	'''

	# User who made the comment
	creator = models.ForeignKey(
		Profile
	)

	# GroupSession being commented on
	session = models.ForeignKey(
		GroupSession
	)

	# Comment text
	text = models.CharField(
		max_length=250,
		default = '',
		null = False,
		blank = False
	)

	created = models.DateTimeField(
		auto_now_add = True,
		blank=True,
		null=True
	)

	modified = models.DateTimeField(
		auto_now = True,
		blank = True,
		null = True
	)

class Like(models.Model):
	'''
	Rapchat Like Model
	'''

	# User who made the like
	user = models.ForeignKey(
		Profile
	)

	session = models.ForeignKey(
		GroupSession
	)

	created = models.DateTimeField(
		auto_now_add = True,
		blank=True,
		null=True
	)

	modified = models.DateTimeField(
		auto_now = True,
		blank = True,
		null = True
	)

	def __unicode__(self):
		return 'Like: {}'.format(self.session.title)


############################# BATTLES ##################################

# class BattleSession(models.Model):
# 	'''
# 	Rapback Battle Session
# 	'''

# 	title = models.CharField(
# 		max_length=100
# 	)

# 	is_complete = models.BooleanField(
# 		default=False
# 	)

# 	battle_creator = models.ForeignKey(
# 		Profile,
# 		related_name='battle_creator_set'
# 	)

# 	battle_receiver = models.ForeignKey(
# 		Profile,
# 		related_name='battle_receiver_set'
# 	)

# 	created = models.DateTimeField(
# 		auto_now_add = True,
# 		blank = True,
# 		null = True
# 	)

# 	modified = models.DateTimeField(
# 		auto_now = True,
# 		blank = True,
# 		null = True
# 	)

# 	def get_round(self, battle_clip):
# 		return self.num_clips / 2 + 1

# 	def num_likes(self):
# 		return self.battlelike_set.count()

# 	def num_clips(self):
# 		return self.battleclip_set.count()

# 	def get_comments(self):
# 		return self.battlecomment_set.all().order_by('created')

# 	def get_clips(self):
# 		return self.battleclip_set.all().order_by('created')

# 	def most_recent_clip(self):
# 		try:
# 			return self.battleclip_set.latest('created')
# 		except BattleClip.DoesNotExist:
# 			return None

# 	def __unicode__(self):
# 		return 'Session: {}'.format(self.title)

# class BattleClip(models.Model):
# 	'''
# 	Rapchat Music Clip
# 	'''

# 	# duration = models.IntegerField()

# 	clip_num = models.IntegerField(
# 		default = 1
# 	)

# 	creator = models.ForeignKey(
# 		Profile
# 	)

# 	battle = models.ForeignKey(
# 		BattleSession
# 	)
	
# 	def get_clip_upload_path(self, filename):
# 		return 'battles/battle_{}/clip_{}.mp4'.format(self.battle.id, self.clip_num)

# 	def get_thumbnail_upload_path(self, filename):
# 		return 'battles/battle_{}/thumbnail_{}.jpg'.format(self.battle.id, self.clip_num)

# 	def get_url(self, battle_clip):
# 		return battle_clip.clip.url

# 	clip = models.FileField(
# 		upload_to=get_clip_upload_path
# 	)

# 	thumbnail = models.FileField(
# 		upload_to=get_thumbnail_upload_path,
# 		null = True,
# 		blank = True
# 	)

# 	created = models.DateTimeField(
# 		auto_now_add = True,
# 		blank = True,
# 		null = True
# 	)

# 	modified = models.DateTimeField(
# 		auto_now_add = True,
# 		blank = True,
# 		null = True
# 	)

# @receiver(post_save, sender=BattleClip)
# def update_session_modified_timestamp(sender, instance=None, created=False, **kwargs):
# 	if created and instance:
# 		print 'Updating modified timestamp on session: {}'.format(instance.battle.pk)
# 		instance.battle.save()


# class BattleLike(models.Model):
# 	'''
# 	Rapback Like for BattleSessions Model
# 	'''

# 	# User who made the like
# 	user = models.ForeignKey(
# 		Profile
# 	)

# 	battle = models.ForeignKey(
# 		BattleSession
# 	)

# 	created = models.DateTimeField(
# 		auto_now_add = True,
# 		blank=True,
# 		null=True
# 	)

# 	modified = models.DateTimeField(
# 		auto_now = True,
# 		blank = True,
# 		null = True
# 	)

# 	def __unicode__(self):
# 		return 'BattleLike: {}'.format(self.battle.title)

# class BattleComment(models.Model):
# 	'''
# 	Rapback comment for BattleSession Model
# 	'''
# 	creator = models.ForeignKey(
# 		Profile
# 	)

# 	# GroupSession being commented on
# 	battle = models.ForeignKey(
# 		BattleSession
# 	)

# 	# Comment text
# 	text = models.CharField(
# 		max_length=250,
# 		default = '',
# 		null = False,
# 		blank = False
# 	)

# 	created = models.DateTimeField(
# 		auto_now_add = True,
# 		blank=True,
# 		null=True
# 	)

# 	modified = models.DateTimeField(
# 		auto_now = True,
# 		blank = True,
# 		null = True
# 	)