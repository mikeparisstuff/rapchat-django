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

	message = models.TextField(
		max_length = 2000
	)

	was_read = models.BooleanField(
		default = False
	)

	created_at = models.DateTimeField(
		auto_now_add = True,
		blank = True,
		null = True
	)

	modified_at = models.DateTimeField(
		auto_now = True,
		blank = True,
		null = True
	)