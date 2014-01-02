from django.contrib.auth.models import User

from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework import serializers
from users.models import Profile, FriendRequest



class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		read_only_fields = (
			'id',
		)
		fields = (
			'id',
			'first_name',
			'last_name',
			'email',
			'username',
			'date_joined',
			'last_login'
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
	# Give nested information for friends
	friends = ProfileSerializerNoFriends(many=True)

	class Meta:
		model = Profile
		fields = (
			'id',
			'user',
			'friends',
			'phone_number'
		)

class MyProfileSerializer(serializers.ModelSerializer):

	def get_num_likes(self, profile):
		if profile:
			return profile.get_num_likes()
		return None

	def get_num_raps(self, profile):
		if profile:
			return profile.get_num_raps()

	def get_num_friends(self, profile):
		if profile:
			return profile.get_num_friends()
		return None

	user = UserSerializer()
	friends = ProfileSerializerNoFriends(many=True)
	num_likes = serializers.SerializerMethodField('get_num_likes')
	num_friends = serializers.SerializerMethodField('get_num_friends')
	num_raps = serializers.SerializerMethodField('get_num_raps')

	class Meta:
		model = Profile
		fields = (
			'id',
			'user',
			'friends',
			'phone_number',
			'num_likes',
			'num_friends',
			'num_raps'
		)