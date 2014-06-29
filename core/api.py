from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication


class BaseRapchatView(APIView):
	pass

class UnauthenticatedView(BaseRapchatView):
	'''
	View class for any views whcih do not require the user to be logged in.
	'''
	authentication_classes = (TokenAuthentication,)

class AuthenticatedView(BaseRapchatView):
	'''
	View class for any views which require the user to be logged in.
	'''
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)