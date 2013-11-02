from django.contrib import admin
from django.db import models

from crowds.models import Crowd

class CrowdAdmin(admin.ModelAdmin):

	list_display = (
		'id',
		'title',
		'created'
	)

admin.site.register(GroupSession, GroupSessionAdmin)