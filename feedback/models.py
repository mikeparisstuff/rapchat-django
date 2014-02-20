from django.db import models

from users.models import Profile

# Create your models here.
class FeedbackMessage(models.Model):
	'''
	Rapback feedback model
	'''
	creator = models.ForeignKey(
		Profile
	)

	message = models.CharField(
		max_length = 2000
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