from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from groupsessions.models import GroupSession
from groupsessions.serializers import GroupSessionSerializer
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