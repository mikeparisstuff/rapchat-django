from django.contrib import admin
from django.db import models

from groupsessions.models import GroupSession

class GroupSessionAdmin(admin.ModelAdmin):

	list_display = (
		'id',
		'title',
		'crowd',
		'is_complete',
		'created'
	)

admin.site.register(GroupSession, GroupSessionAdmin)