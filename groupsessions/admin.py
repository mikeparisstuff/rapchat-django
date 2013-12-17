from django.contrib import admin
from django.db import models

from groupsessions.models import GroupSession, Clip, Like

class GroupSessionAdmin(admin.ModelAdmin):

	list_display = (
		'id',
		'title',
		'crowd',
		'is_complete',
		'created'
	)

class ClipAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'creator',
		'session',
		'clip_num',
	)

class LikeAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'user',
		'session',
		'created'
	)

admin.site.register(GroupSession, GroupSessionAdmin)
admin.site.register(Clip, ClipAdmin)
admin.site.register(Like, LikeAdmin)