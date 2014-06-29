# Create your views here.
from rest_framework import status
from rest_framework.response import Response

from core.api import AuthenticatedView

from feedback.models import FeedbackMessage

class HandleFeedback(AuthenticatedView):

	def post(self, request, fromat=None):
		'''
		Create a new feedback message.

		message (required) -- The message to create the feedback
		'''
		try:
			creator = request.user.get_profile()
			message = request.DATA['message']
			feedback = FeedbackMessage.objects.create(
				creator = creator,
				message = message
			)
			return Response(
				{'detail': 'Successfully sent feedback'},
				status = status.HTTP_200_OK
			)
		except KeyError:
			return Response(
				{'error': 'Feedback posts require a message'},
				status = status.HTTP_400_BAD_REQUEST
			)