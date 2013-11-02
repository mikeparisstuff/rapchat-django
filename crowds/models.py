from django.db import models
from users.models import Profile

class Crowd(models.Model):
	'''
	Rapchat Crowd
	'''

	title = models.CharField(
		max_length = 100,
		null = True,
		blank = True
	)

	members = models.ManyToManyField(
		Profile
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

	def num_members(self):
		return self.members.count()