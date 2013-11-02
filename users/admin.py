from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

from users.models import Profile

class ProfileAdmin(admin.ModelAdmin):

	def first_name(self, the_profile):
		if the_profile.user:
			return '{}'.format(
				the_profile.user.first_name
			)
		return None

	def last_name(self, the_profile):
		if the_profile.user:
			return '{}'.format(the_profile.user.last_name)
		return None

	def email(self, the_profile):
		if the_profile.user:
			return '{}'.format(the_profile.user.email)
		return None

	list_display = (
		'id',
		'first_name',
		'last_name',
		'email'
	)

admin.site.register(Profile, ProfileAdmin)