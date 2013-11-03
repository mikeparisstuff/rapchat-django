from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from groupsessions.models import GroupSession, Clip
from groupsessions.serializers import GroupSessionSerializer, ClipSerializer
from crowds.models import Crowd
from core.api import AuthenticatedView

class HandleSessions(AuthenticatedView):

	def post(self, request, format=None):
		'''
		Create a GroupSession for the specified crowd

		title (required) -- The title for the rap session
		crowd (required) -- The id of the crowd to link the session to
		'''
		try:
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