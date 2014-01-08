from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Profile
from crowds.models import Crowd
from rapchat.serializers import CrowdSerializer
from core.api import AuthenticatedView

class HandleCrowds(AuthenticatedView):

	def post(self, request, format=None):
		'''
		Create a new crowd given a list of profiles as members
		
		title (required) -- The title of the session
		members (required) -- The list of usernames to add as members
		'''
		try:
			usernames = request.DATA['members']
			print 'USERNAMES: {}'.format(usernames)
			profiles = Profile.objects.filter(user__username__in=usernames)
			print 'PROFILES: {}'.format(profiles)
			title = ''
			if 'title' in request.DATA:
				title = request.DATA['title']
			c = Crowd.objects.create(
				title = title
			)
			for item in profiles.all():
				c.members.add(item)
			c.members.add(request.user.get_profile())
			print 'New Crowd Members: {}'.format(c.members)
			serializer = CrowdSerializer(c)
			return Response(
				{'detail': 'Successfully created new crowd',
				'crowd': serializer.data
				},
				status = status.HTTP_201_CREATED
			)
		except KeyError:
			return Response(
				{'error': 'All crowds must have a list of members'},
				status=status.HTTP_400_BAD_REQUEST
			)
		except Profile.DoesNotExist:
			return Response(
				{'error': 'One or more profiles in the members list could not be found'},
				status=status.HTTP_404_NOT_FOUND
			)

	def get(self, request, format=None):
		'''
		Return a list of crowds that the logged in user is a member of

		returns {
			crowds: [
				{"title": "Rappin' here",
				 "members": [ ... List of memeber profiles ...]
				}
			]
		}
		'''
		crowds = request.user.get_profile().crowd_set.all()
		serializer = CrowdSerializer(crowds, many=True)
		return Response(
			{'crowds': serializer.data},
			status=status.HTTP_200_OK	
		)