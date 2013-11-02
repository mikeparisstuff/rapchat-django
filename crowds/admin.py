from django.contrib import admin
from django.db import models

from crowds.model import Crowd

class CrowdAdmin(admin.ModelAdmin):

	list_display = (
		'id',
		'title',
		'created'
	)

admin.site.register(GroupSession, GroupSessionAdmin)