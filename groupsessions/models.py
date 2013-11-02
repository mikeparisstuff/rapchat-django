from django.db import models

from crowds.models import Crowd

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

	video_url = models.URLField(
		default = '',
		blank = True,
		null = True
	)

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