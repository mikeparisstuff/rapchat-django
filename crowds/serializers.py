from rest_framework import serializers
from crowds.models import Crowd
from users.serializers import ProfileSerializerNoFriends

class CrowdSerializer(serializers.ModelSerializer):

	members = ProfileSerializerNoFriends(many=True)

	class Meta:
		model = Crowd
		fields = (
			'title',
			'members',
			'created',
			'modified'
		)

