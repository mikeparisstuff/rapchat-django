from django.contrib.auth.models import User

class AuthTokenBackend(object):
	'''
	Token Authentication AuthTokenBackend

	Allow a user to login each request with their access_token
	'''
	def authenticate(self, token=None):
		'''
		Authenticate a user based on access_token
		'''
		try: 
			user = User.objects.get(access_token=token)
			if user:
				return user
			return None
		except User.DoesNotExist:
			return None

	def get_user(sel,)
