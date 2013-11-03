from rest_framework import serializers
from groupsessions.models import GroupSession, Clip
from crowds.serializers import CrowdSerializer


class GroupSessionSerializer(serializers.ModelSerializer):

	crowd = CrowdSerializer()

	class Meta:
		model = GroupSession
		fields = (
			'id',
			'crowd',
			'title',
			'is_complete',
			'created',
			'modified'	
		)

class ClipSerializer(serializers.ModelSerializer):

	def get_url(self, clip):
		return clip.clip.url

	url = serializers.SerializerMethodField('get_url')

	class Meta:
		model = Clip
		fields = (
			'duration',
			'clip',
			'url',
			'clip_num',
			'creator',
			'session',
			'created',
			'modified'
		)