from rest_framework import serializers
from crowds.models import Crowd
from users.serializers import ProfileSerializer

class CrowdSerializer(serializers.ModelSerializer):

	members = ProfileSerializer(many=True)

	class Meta:
		model = Crowd
		fields = (
			'title',
			'members',
			'created',
			'modified'
		)

