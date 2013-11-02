from rest_framework import serializers
from groupsessions.models import GroupSession
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
			'video_url',
			'created',
			'modified'	
		)