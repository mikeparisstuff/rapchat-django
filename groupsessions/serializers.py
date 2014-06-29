from rest_framework import serializers, pagination
from groupsessions.models import GroupSession, Clip, Comment, Like
from users.serializers import ProfileSerializer

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

class PaginatedGroupSessionSerializer(pagination.PaginationSerializer):
	'''
	Serializes page objects of query sets
	'''
	class Meta:
		object_serializer_class = GroupSessionSerializer

class ClipSerializer(serializers.ModelSerializer):

	url = serializers.Field(source='get_url')

	class Meta:
		model = Clip
		fields = (
			'clip',
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