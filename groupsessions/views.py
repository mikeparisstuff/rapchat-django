from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from groupsessions.models import GroupSession, Clip, Comment, Like
from groupsessions.serializers import GroupSessionSerializer, ClipSerializer, CommentSerializer, LikeSerializer
from crowds.models import Crowd
from users.models import Profile
from core.api import AuthenticatedView

import json

class HandleSessions(AuthenticatedView):

	def post(self, request, format=None):
		'''
		Create a GroupSession for the specified crowd

		title (required) -- The title for the rap session
		use_existing_crowd (required) -- Boolean value. If true we will use 'crowd' else create a new crowd with 'members' and 'title'
		clip (required) -- File. A file holding the clip to be added to the new session
		crowd_title (depends) -- The title of the crowd to create and link to this session
		crowd_members (depends) -- A json formatted list string of usernames to use as members for the crowd
		crowd (depends) -- The id of the crowd to link the session to
		'''
		try:
			crowd = None
			print 'Request use_existing_crowd: {}'.format(request.DATA['use_existing_crowd'])
			use_existing = request.DATA['use_existing_crowd']
			if not isinstance(request.DATA['use_existing_crowd'], bool):
				# The param is a string not a boolean
				use_existing = False if request.DATA['use_existing_crowd'].lower() == 'false' else True
			if not use_existing: 
				usernames = json.loads(request.DATA['crowd_members'])
				print 'USERNAMES: {}'.format(usernames)
				profiles = Profile.objects.filter(user__username__in=usernames)
				title = ''
				if 'crowd_title' in request.DATA:
					title = request.DATA['crowd_title']
				crowd = Crowd.objects.create(
					title = title
				)
				for item in profiles.all():
					crowd.members.add(item)
				crowd.members.add(request.user.get_profile())
			if crowd is None:
				crowd = Crowd.objects.get(pk=request.DATA['crowd'])
			title = request.DATA['title']
			gs = GroupSession.objects.create(
				crowd = crowd,
				title = title
			)		

			# Create a new clip for the newly created session
			f =  request.FILES['clip']
			thumbnail = None
			c = Clip(
				clip_num = gs.num_clips()+1,
				session = gs,
				creator = request.user.get_profile()
			)
			if 'thumbnail' in request.FILES:
				thumbnail = request.FILES['thumbnail']
				c.thumbnail = thumbnail
			c.clip = f
			print 'Clip Created'
			c.save()
			print 'Clip Saved'

			serializer = GroupSessionSerializer(gs)

			return Response(
				{'session': serializer.data},
				status=status.HTTP_201_CREATED
			)


		except KeyError:
			return Response(
				{'error_description': 'New sessions require a title and crowd'},
				status=status.HTTP_400_BAD_REQUEST
			)
		except Crowd.DoesNotExist:
			return Response(
				{'error_description': 'Could not find crowd with id {}'.format(request.DATA['crowd'])},
				status=status.HTTP_404_NOT_FOUND
			)

	def get(self, request, format=None):
		'''
		Return a list of sessions for the currently logged in user.

		TODO: Filter the user data that gets send at this endpoint.
		We probably don't want each users friend information to be being sent etc.
		'''
		user_crowds = request.user.get_profile().crowd_set.all()
		sessions = GroupSession.objects.filter(crowd__in=user_crowds).order_by('-modified')
		serializer = GroupSessionSerializer(sessions, many=True)
		return Response(
			{'sessions': serializer.data},
			status=status.HTTP_200_OK
		)

class HandleSession(AuthenticatedView):

	def get(self, request, format=None, session=None):
		'''
		Return a single session as designated by the id in the URL
		'''
		try:
			sesh = GroupSession.objects.get(pk=session)
			serializer = GroupSessionSerializer(sesh)
			return Response(serializer.data, status=status.HTTP_200_OK)
		except GroupSession.DoesNotExist:
			return Response({
				'error_description': 'Could not find a session with that id.'
				}, status=status.HTTP_400_BAD_REQUEST
			)

class HandleClips(AuthenticatedView):

	def post(self, request, format=None, session=None):
		'''
		Add a clip to a session.

		clip (required) -- The clip file to add to the session
		thumbnail (required)  -- A jpg image file to serve as a thumbnail for the clipg
		'''
		try:
			sesh = GroupSession.objects.get(pk=session)
			f =  request.FILES['clip']
			thumbnail = None
			c = Clip(
				clip_num = sesh.num_clips()+1,
				session = sesh,
				creator = request.user.get_profile()
			)
			c.clip = f
			if 'thumbnail' in request.FILES:
				thumbnail = request.FILES['thumbnail']
				c.thumbnail = thumbnail
			print 'Clip Created'
			c.save()
			print 'Clip Saved'
			serializer = ClipSerializer(c)
			return Response(
				serializer.data,
				status=status.HTTP_200_OK
			)
		except KeyError:
			return Response(
				{'error_description': 'A clip file and session are required to add a clip'},
				status=status.HTTP_400_BAD_REQUEST
			)
		except GroupSession.DoesNotExist:
			return Response(
				{'error_description': 'The session with id {} could not be found'.format(request.DATA['session'])},
				status = status.HTTP_404_NOT_FOUND
			)

	def get(self, request, format=None, session=None):
		'''
		Return data on each of the clips for the session specified in the url.
		'''
		try:
			clips = Clip.objects.filter(session=session)
			serializer = ClipSerializer(clips, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		except Clip.DoesNotExist:
			return Response({
				'error_description': 'Could not find any clips for session {}'.format(session)
				}, status=status.HTTP_400_BAD_REQUEST
			)

class HandleSessionComments(AuthenticatedView):
	def post(self, request, format=None, session=None):
		'''
		Add a comment to a session.

		text (required) -- The text of the comment itself
		'''
		try:
			sesh = GroupSession.objects.get(pk=session)
			comment = Comment.objects.create(
				session=sesh,
				creator=request.user.get_profile(),
				text = request.DATA['text']
			)
			serializer = CommentSerializer(comment)
			return Response({
				'comment': serializer.data,
				'detail': 'Successfully added comment to session %d' % sesh.id
				},
				status=status.HTTP_200_OK
			)
		except KeyError:
			return Response({
				'error_description': 'Error creating comment. Comments need a session and comment_text.'
				},
				status=status.HTTP_400_BAD_REQUEST
			)

	def get(self, request, format=None, session=None):
		'''
		Get all of a sessions comments.

		session (required) -- The id of the session. This must be included in the url e.g. /sessions/comments/1/
		would refer to the session with id == 1.
		'''
		try:
			sesh = GroupSession.objects.get(pk=session)
			comments = sesh.get_comments()
			# s_serializer = GroupSessionSerializer(sesh)
			print ' Found comments'
			c_serializer = CommentSerializer(comments, many=True)
			print 'Serialized comments'
			return Response({
				'comments': c_serializer.data,
				'detail': 'Successfully found comments for session %d' % sesh.id
				},
				status=status.HTTP_200_OK
			)
		except KeyError:
			return Response({
				'error_description': 'Need a session to find comments for.'
				},
				status=status.HTTP_400_BAD_REQUEST
			)
		except GroupSession.DoesNotExist:
			return Response({
				'error_description': 'Sorry, we could not find that session.'
				},
				status=status.HTTP_400_BAD_REQUEST
			)

class HandleSessionLikes(AuthenticatedView):
	def post(self, request, format=None):
		'''
		Add a like to a session

		session (required) -- The id of the session to add the comment to
		'''
		try:
			session = GroupSession.objects.get(id=request.DATA['session'])
			like = Like.objects.get(
				user = request.user.get_profile(),
				session= session
			)
			like.delete()
			return Response({
				'like': {'detail': 'Successfully deleted like'}
				}, status=status.HTTP_200_OK
			)
		except Like.DoesNotExist:
			like = Like.objects.create(
				user= request.user.get_profile(),
				session= session
			)
			serializer = LikeSerializer(like)
			return Response({
				'like': serializer.data
				},
				status=status.HTTP_201_CREATED
			)
		except KeyError:
			return Response({
				'detail': 'Failed to create like'},
				status = status.HTTP_400_BAD_REQUEST
				)

	def get(self, request, format=None):
		'''
		Get all the likes for the currently logged in user
		'''
		likes = request.user.get_profile().get_likes()
		print likes
		serializer = None
		if len(likes) > 1:
			serializer = LikeSerializer(likes, many=True)
		else:
			serializer = LikeSerializer(likes)
		return Response({
			'likes': serializer.data
			},
			status = status.HTTP_200_OK
		)	
