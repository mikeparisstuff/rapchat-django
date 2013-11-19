from django.contrib.auth.models import User

from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework import serializers
from users.models import Profile, FriendRequest



class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		read_only_fields = (
			'id',
			'username',
			'date_joined'
		)
		fields = (
			'id',
			'first_name',
			'last_name',
			'email',
			'username',
			'date_joined'
		)

class FriendRequestSerializer(serializers.ModelSerializer):

	sender = UserSerializer()
	requested = UserSerializer()

	class Meta:
		model=FriendRequest
		fields = (
			'sender',
			'requested',
			'is_accepted',
			'created',
			'modified'
		)

class ProfileSerializerNoFriends(serializers.ModelSerializer):
	user = UserSerializer()

	class Meta:
		model = Profile
		fields = (
			'id',
			'user',
			'phone_number'
		)

class ProfileSerializer(serializers.ModelSerializer):

	user = UserSerializer()

	class Meta:
		model = Profile
		fields = (
			'id',
			'user',
			'friends',
			'phone_number'
		)
		read_only_fields = (
			'phone_number',
		)