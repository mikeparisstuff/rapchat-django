from django.db import models

from crowds.models import Crowd
from users.models import Profile

class GroupSession(models.Model):
	'''
	Rapchat Session Model
	'''
	crowd = models.ForeignKey(
		Crowd
	)

	title = models.CharField(
		max_length=100
	)

	is_complete = models.BooleanField(
		default=False
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

	def num_likes(self):
		return self.like_set.count()

	def num_clips(self):
		return self.clip_set.count()

	def get_comments(self):
		return self.comment_set.all().order_by('-created')



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
	
	def get_upload_path(self, filename):
		return 'sessions/session_{}/clip_{}.mp4'.format(self.session.id, self.clip_num)

	clip = models.FileField(
		upload_to=get_upload_path
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