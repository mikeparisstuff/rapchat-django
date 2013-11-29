from rest_framework import serializers
from groupsessions.models import GroupSession, Clip, Comment
from crowds.serializers import CrowdSerializer


class CommentSerializer(serializers.ModelSerializer):

	class Meta:
		model = Comment
		fields = (
			'creator',
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
			return CommentSerializer(group_session.comment_set.all(), many=True).data
		return None

	crowd = CrowdSerializer()
	comments = serializers.SerializerMethodField('get_comments')

	class Meta:
		model = GroupSession
		fields = (
			'id',
			'crowd',
			'title',
			'is_complete',
			'comments',
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
			'clip',
			'url',
			'clip_num',
			'creator',
			'session',
			'created',
			'modified'
		)
