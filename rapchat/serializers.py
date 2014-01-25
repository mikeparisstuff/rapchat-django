from django.contrib.auth.models import User
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework import serializers, pagination

from groupsessions.models import GroupSession, Clip, Comment, Like
from users.models import Profile, FriendRequest
from crowds.models import Crowd



########################################################################
#  User, Profile, Friends Serializers
########################################################################

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

class UserSerializerWithProfilePicture(serializers.ModelSerializer):
	
	def get_profile_picture(self, user):
		if user:
			profile = user.get_profile()
			if profile.profile_picture:	
				return profile.profile_picture.url if profile.profile_picture.url else None
		return None
	profile_picture = serializers.SerializerMethodField('get_profile_picture')
	
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
			'profile_picture',
			'date_joined',
			'last_login'
		)

class FriendRequestSerializer(serializers.ModelSerializer):

	sender = UserSerializerWithProfilePicture()
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

	def get_profile_picture_url(self, profile):
		if profile.profile_picture:
			return profile.profile_picture.url if profile.profile_picture.url else None
		return None

	profile_picture = serializers.SerializerMethodField('get_profile_picture_url')

	class Meta:
		model = Profile
		fields = (
			'id',
			'user',
			'phone_number',
			'profile_picture'
		)


class ProfileSerializer(serializers.ModelSerializer):

	user = UserSerializer()
	# Give nested information for friends
	friends = ProfileSerializerNoFriends(many=True)
	
	def get_profile_picture_url(self, profile):
		if profile.profile_picture:
			return profile.profile_picture.url if profile.profile_picture.url else None
		return None

	profile_picture = serializers.SerializerMethodField('get_profile_picture_url')

	class Meta:
		model = Profile
		fields = (
			'id',
			'user',
			'friends',
			'phone_number',
			'profile_picture'
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

	def get_profile_picture_url(self, profile):
		if profile.profile_picture:
			return profile.profile_picture.url if profile.profile_picture.url else None
		return None

	user = UserSerializer()
	friends = ProfileSerializerNoFriends(many=True)
	num_likes = serializers.SerializerMethodField('get_num_likes')
	num_friends = serializers.SerializerMethodField('get_num_friends')
	num_raps = serializers.SerializerMethodField('get_num_raps')
	profile_picture = serializers.SerializerMethodField('get_profile_picture_url')

	class Meta:
		model = Profile
		fields = (
			'id',
			'user',
			'friends',
			'phone_number',
			'num_likes',
			'num_friends',
			'num_raps',
			'profile_picture'
		)

#################################################################
# Crowd Serializers
#################################################################

class CrowdSerializer(serializers.ModelSerializer):

	members = ProfileSerializerNoFriends(many=True)

	class Meta:
		model = Crowd
		fields = (
			'id',
			'title',
			'members',
			'created',
			'modified'
		)

class CrowdSerializerNoMembers(serializers.ModelSerializer):
	
	class Meta:
		model = Crowd
		fields = (
			'id',
			'title',
			'created',
			'modified'
		)

###########################################################
# Comment, GroupSession, Clip, and Like Serializers
###########################################################

class CommentSerializer(serializers.ModelSerializer):

	commenter = serializers.Field(source='creator.user.username')

	class Meta:
		model = Comment
		fields = (
			'id',
			'commenter',
			'session',
			'text',
			'created',
			'modified'
		)


class GroupSessionSerializer(serializers.ModelSerializer):

	# May be a cleaner way to get this relationship
	# TODO: investigate
	def get_comments(self, group_session):
		if group_session:
			return CommentSerializer(group_session.get_comments(), many=True).data
		return None

	def get_likes(self, group_session):
		if group_session:
			return group_session.like_set.all().count()
		return None

	def get_most_recent_clip_url(self, group_session):
		if group_session:
			clip = group_session.most_recent_clip()
			if clip:
				return clip.clip.url
			return None
		return None

	def get_most_recent_thumbnail_url(self, group_session):
		if group_session:
			clip = group_session.most_recent_clip()
			if clip:
				try:
					return clip.thumbnail.url
				except ValueError:
					return None
			return None
		return None


	crowd = CrowdSerializer()
	comments = serializers.SerializerMethodField('get_comments')
	likes = serializers.SerializerMethodField('get_likes')
	clip_url = serializers.SerializerMethodField('get_most_recent_clip_url')
	thumbnail_url = serializers.SerializerMethodField('get_most_recent_thumbnail_url')

	class Meta:
		model = GroupSession
		fields = (
			'id',
			'crowd',
			'title',
			'is_complete',
			'comments',
			'likes',
			'clip_url',
			'thumbnail_url',
			'created',
			'modified'	
		)

class GroupSessionSerializerUnkownStatus(serializers.ModelSerializer):

	def get_comments(self, group_session):
			if group_session:
				return CommentSerializer(group_session.get_comments(), many=True).data
			return None

	def get_likes(self, group_session):
		if group_session:
			return group_session.like_set.all().count()
		return None

	def get_most_recent_clip_url(self, group_session):
		if group_session:
			clip = group_session.most_recent_clip()
			if clip:
				return clip.clip.url
			return None
		return None

	def get_most_recent_thumbnail_url(self, group_session):
		if group_session:
			clip = group_session.most_recent_clip()
			if clip:
				try:
					return clip.thumbnail.url
				except ValueError:
					return None
			return None
		return None

		def get_clips(self, group_session):
			if group_session:
				clips = group_session.get_clips()
				return ClipSerializer(clips, many=True).data
			return None

		crowd = CrowdSerializer()
		comments = serializers.SerializerMethodField('get_comments')
		clip_url = serializers.SerializerMethodField('get_most_recent_clip_url')
		thumbnail_url = serializers.SerializerMethodField('get_most_recent_thumbnail_url')
		likes = serializers.SerializerMethodField('get_likes')
		clips = serializers.SerializerMethodField('get_clips')

		class Meta:
			model = GroupSession
			fields = (
				'id',
				'crowd',
				'title',
				'is_complete',
				'comments',
				'likes',
				'clips',
				'created',
				'modified'	
			)	

class CompletedGroupSessionSerializer(serializers.ModelSerializer):

	def get_comments(self, group_session):
		if group_session:
			return CommentSerializer(group_session.get_comments(), many=True).data
		return None

	def get_likes(self, group_session):
		if group_session:
			return group_session.like_set.all().count()
		return None

	def get_most_recent_clip_url(self, group_session):
		if group_session:
			clip = group_session.most_recent_clip()
			if clip:
				return clip.clip.url
			return None
		return None

	def get_clips(self, group_session):
		if group_session:
			clips = group_session.get_clips()
			return ClipSerializer(clips, many=True).data
		return None

	crowd = CrowdSerializer()
	comments = serializers.SerializerMethodField('get_comments')
	likes = serializers.SerializerMethodField('get_likes')
	clips = serializers.SerializerMethodField('get_clips')

	class Meta:
		model = GroupSession
		fields = (
			'id',
			'crowd',
			'title',
			'is_complete',
			'comments',
			'likes',
			'clips',
			'created',
			'modified'	
		)



class GroupSessionSerializerNoMembers(serializers.ModelSerializer):
	# May be a cleaner way to get this relationship
	# TODO: investigate
	def get_comments(self, group_session):
		if group_session:
			return CommentSerializer(group_session.get_comments(), many=True).data
		return None

	def get_likes(self, group_session):
		if group_session:
			return group_session.like_set.all().count()
		return None

	def get_most_recent_clip_url(self, group_session):
		if group_session:
			clip = group_session.most_recent_clip()
			if clip:
				return clip.clip.url
			return None
		return None

	def get_most_recent_thumbnail_url(self, group_session):
		if group_session:
			clip = group_session.most_recent_clip()
			if clip:
				try:
					return clip.thumbnail.url
				except ValueError:
					return None
			return None
		return None

	def get_clips(self, group_session):
		if group_session:
			clips = group_session.get_clips()
			return ClipSerializer(clips, many=True).data
		return None

	crowd = CrowdSerializerNoMembers()
	comments = serializers.SerializerMethodField('get_comments')
	likes = serializers.SerializerMethodField('get_likes')
	clip_url = serializers.SerializerMethodField('get_most_recent_clip_url')
	thumbnail_url = serializers.SerializerMethodField('get_most_recent_thumbnail_url')
	clips = serializers.SerializerMethodField('get_clips')

	class Meta:
		model = GroupSession
		fields = (
			'id',
			'crowd',
			'title',
			'is_complete',
			'comments',
			'likes',
			'clip_url',
			'clips',
			'thumbnail_url',
			'created',
			'modified'	
		)


class PaginatedGroupSessionSerializer(pagination.PaginationSerializer):
	'''
	Serializes page objects of query sets
	'''
	class Meta:
		object_serializer_class = GroupSessionSerializer

class PaginatedCompletedGroupSessionSerializer(pagination.PaginationSerializer):
	class Meta:
		object_serializer_class = CompletedGroupSessionSerializer

class ClipSerializer(serializers.ModelSerializer):

	def get_url(self, clip):
		return clip.clip.url

	def get_thumbnail_url(self, clip):
		if clip.thumbnail:
			return clip.thumbnail.url if clip.thumbnail.url else None
		return None

	url = serializers.SerializerMethodField('get_url')
	thumbnail_url = serializers.SerializerMethodField('get_thumbnail_url')

	class Meta:
		model = Clip
		fields = (
			'id',
			'clip',
			'thumbnail_url',
			'url',
			'clip_num',
			'creator',
			'session',
			'created',
			'modified'
		)

class LikeSerializer(serializers.ModelSerializer):

	user = ProfileSerializer()
	session = GroupSessionSerializer()
	username = serializers.Field(source='user.user.username')

	class Meta:
		model = Like
		fields = (
			'id',
			'username',
			'session',
			'created',
			'modified'
		)

class LikeSerializerNoMembers(serializers.ModelSerializer):
	user = ProfileSerializer()
	session = GroupSessionSerializerNoMembers()
	username = serializers.Field(source='user.user.username')

	class Meta:
		model = Like
		fields = (
			'id',
			'username',
			'session',
			'created'
		)

######################################################################
#  Public Profile Serializer
######################################################################

class PublicProfileSerializer(serializers.ModelSerializer):

	user = UserSerializer()
	friends = ProfileSerializerNoFriends(many=True)
	num_likes = serializers.Field(source='get_num_likes')
	num_friends = serializers.Field(source='get_num_friends')
	num_raps = serializers.Field(source='get_num_raps')

	def get_profile_picture_url(self, profile):
		if profile.profile_picture:
			return profile.profile_picture.url if profile.profile_picture.url else None
		return None

	profile_picture = serializers.SerializerMethodField('get_profile_picture_url')

	class Meta:
		model = Profile
		fields = (
			'id',
			'user',
			'friends',
			'profile_picture',
			'num_likes',
			'num_friends',
			'num_raps'
			)