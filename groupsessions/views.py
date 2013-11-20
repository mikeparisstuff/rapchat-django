from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from groupsessions.models import GroupSession, Clip, Comment, Like
from groupsessions.serializers import GroupSessionSerializer, ClipSerializer, CommentSerializer
from crowds.models import Crowd
from users.models import Profile
from core.api import AuthenticatedView

class HandleSessions(AuthenticatedView):

	def post(self, request, format=None):
		'''
		Create a GroupSession for the specified crowd

		title (required) -- The title for the rap session
		use_existing_crowd (required) -- Boolean value. If true we will use 'crowd' else create a new crowd with 'members' and 'title'
		crowd_title (depends) -- The title of the crowd to create and link to this session
		crowd_members (depends) -- A list of usernames to use as members for the crowd
		crowd (depends) -- The id of the crowd to link the session to
		'''
		try:
			crowd = None
			if not request.DATA['use_existing_crowd']:
				usernames = request.DATA['crowd_members']
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
		sessions = GroupSession.objects.filter(pk__in=user_crowds)
		serializer = GroupSessionSerializer(sessions, many=True)
		return Response(
			{'sessions': serializer.data},
			status=status.HTTP_200_OK
		)

class HandleClips(AuthenticatedView):

	def post(self, request, format=None):
		'''
		Add a clip to a session.

		clip (required) -- The clip file to add to the session
		duration (required) -- The length of the clip to be added
		session (required) -- The ID of the session to add the clip to
		'''
		try:
			sesh = GroupSession.objects.get(pk=request.DATA['session'])
			f =  request.FILES['clip']
			c = Clip(
				clip_num = sesh.num_clips()+1,
				session = sesh,
				duration = request.DATA['duration'],
				creator = request.user.get_profile()
			)
			c.clip = f
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
				{'error_description': 'A clip file, duration, and session are required to add a clip'},
				status=status.HTTP_400_BAD_REQUEST
			)
		except GroupSession.DoesNotExist:
			return Response(
				{'error_description': 'The session with id {} could not be found'.format(request.DATA['session'])},
				status = status.HTTP_404_NOT_FOUND
			)

class HandleSessionComments(AuthenticatedView):
	def post(self, request, format=None):
		'''
		Add a comment to a session.

		session (required) -- The id of the session to add the comment to
		comment_text (required) -- The text of the comment itself
		'''
		try:
			sesh = GroupSession.objects.get(pk=request.DATA['session'])
			comment = Comment.objects.create(
				session=sesh,
				creator=request.user.get_profile(),
				text = request.DATA['comment_text']
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