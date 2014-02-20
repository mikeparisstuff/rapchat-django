from django.contrib import admin
from django.db import models

from feedback.models import FeedbackMessage

class FeedbackMessageAdmin(admin.ModelAdmin):
	list_display = (
		'creator',
		'created',
		'was_read'
	)

admin.site.register(FeedbackMessage, FeedbackMessageAdmin)