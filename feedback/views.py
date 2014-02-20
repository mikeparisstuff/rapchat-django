# Create your views here.
from rest_framework import status
from rest_framework.response import Response

from feedback.models import FeedbackMessage

class HandleFeedback(AuthenticatedView):

	def post(self, request, fromat=None):
		'''
		Create a new feedback message.
		'''
		try:
			creator = request.user.get_profile()
			feedback = FeedbackMessage.create(
				creator = creator,
				message = request.DATA['message']
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