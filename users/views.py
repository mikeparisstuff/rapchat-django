import hashlib
import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from users.models import Profile, FriendRequest
from rapchat.serializers import ProfileSerializer, UserSerializer, FriendRequestSerializer, ProfileSerializerNoFriends, MyProfileSerializer, PublicProfileSerializer, LikeSerializerNoMembers
from core.api import AuthenticatedView, UnauthenticatedView

class WelcomePage(APIView):
	def get(self, request, format=None):
		return Response('Welcome to the Rapchat API.  Goto /api-docs/ for more details.')

class HandleUsers(APIView):
	
	def post(self, request, format=None):
		'''
		Create a new user profile.
		Return the information on the newly created user.

		Returns Appropriately:
		{
			"user": {
			    ...
			    userinfo
			    ...
			}, 
			"phone_number": "", 
			"token": "4a2483f4a94b9ff0447945a9d03ebf048e7faf8d"
		}

		email (required) -- Email address for the new user
		username (required) -- The new user's rapchat username
		password (required) -- Password for the new user's account
		first_name (optional) -- User's first name
		last_name (optional) -- User's last name
		phone_number (optional) -- User's current smartphone number
		profile_picture (optional) -- A Square clipped profile picture encoded as jpg
		'''
		try:
			user = User.objects.create_user(
				request.DATA['username'],
				request.DATA['email'],
				request.DATA['password']
			)
			if 'first_name' in request.DATA:
				user.first_name = request.DATA['first_name']
			if 'last_name' in request.DATA:
				user.last_name = request.DATA['last_name']
			user.save()
			token = Token.objects.get(user=user)
			profile = Profile(
				user = user
			)
			if 'phone_number' in request.DATA:
				profile.phone_number = request.DATA['phone_number']
			if 'profile_picture' in request.FILES:
				f = request.FILES['profile_picture']
				profile.profile_picture = f
			profile.save()
			serializer = ProfileSerializer(profile)
			serializer.data['token'] = token.key
			return Response(
				serializer.data,
				status=status.HTTP_201_CREATED
			)
		except KeyError:
			error = {
				'error': "User's must have a username, email address, and password"
			}
			return Response(
				error,
				status=status.HTTP_400_BAD_REQUEST
			)

	def get(self, request, format=None):
		'''
		Return all user profiles
		'''
		profiles = Profile.objects.all()
		serializer = ProfileSerializer(profiles, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

class HandleUser(AuthenticatedView):
	def get(self, request, format=None, username=None):
		'''
		Return a profiles designated by the profile id in the url /users/<id>/
		'''
		try:
			user = User.objects.get(username=username)
			profile = user.get_profile()
			prof_serializer = PublicProfileSerializer(profile)
			likes = profile.get_likes()
			likes_serializer = LikeSerializerNoMembers(likes, many=True)
			return Response({
				'profile': prof_serializer.data,
				'likes': likes_serializer.data
				}, status=status.HTTP_200_OK
			)
		except User.DoesNotExist:
			return Response({
				'error': 'Could not find that user'
				})

class HandleSearch(AuthenticatedView):

	def get(self, request, format=None):
		'''
		Search for rapchat users!

		username (required) -- The username query to search for as a query parameter
		'''
		try:
			print 'search'
			print 'Query Params: {}'.format(request.QUERY_PARAMS['username'])
			profiles = User.objects.filter(username__icontains = request.QUERY_PARAMS['username'])
			serializer = UserSerializer(profiles, many=True)
			return Response({
				'profiles': serializer.data
				}, status=status.HTTP_200_OK
			)
		except Profile.DoesNotExist:
			return Response({
				'profiles': []
				})

class HandleInvites(UnauthenticatedView):

	def get(self, request, format=None):
		'''
		Hit this endpoint to be redirected to the correct app store to download the app
		'''
		type_of_device = None
		if 'iPhone' in request.META['HTTP_USER_AGENT']:
			type_of_device = 'iPhone'
		elif 'Android' in request.META['HTTP_USER_AGENT']:
			type_of_device = 'Android'
		return Response('You are using an {} device'.format(type_of_device))


class HandleMyProfile(AuthenticatedView):

	def get(self, request, format=None):
		'''
		Get my profile.
		'''
		me = Profile.objects.get(user__username = request.user.username)
		serializer = MyProfileSerializer(me)
		return Response(
			serializer.data,
			status=status.HTTP_200_OK
		)

	def put(self, request, format=None):
		'''
		Update my profile

		first_name (required) -- The users first name
		last_name (required) -- The users last name
		email (required) -- The users email address
		phone_number (required) -- The users phone number in format 'xxx-xxx-xxxx'		 
		profile_picture (optional) -- A square clipped jpg to act as the users profile picture
		'''
		me = request.user.get_profile()
		try:
			me.user.first_name = request.DATA['first_name']
			me.user.last_name = request.DATA['last_name']
			me.user.email = request.DATA['email']
			me.phone_number = request.DATA['phone_number']
			if 'profile_picture' in request.FILES:
				f = request.FILES['profile_picture']
				me.profile_picture = f
			me.save()
			me.user.save()
			serializer = ProfileSerializer(me)
			return Response({
				'profile': serializer.data
				}, status=status.HTTP_200_OK
			)
		except KeyError:
			return Response({
				'error': 'Must include first_name, last_name, email, and phone_number'
				}, status=status.HTTP_400_BAD_REQUEST
			)

class HandleFriendRequests(AuthenticatedView):

	def post(self, request, format=None):
		'''
		Create a new friend request from the logged in user to another user.

		username (required) -- The username to send the friend request to
		'''
		try:
			requested = User.objects.get(username=request.DATA['username'])
			f = FriendRequest.objects.create(
				sender = request.user,
				requested = requested
			)
			serializer = FriendRequestSerializer(f)
			return Response(
				{'detail': 'Successfully sent a request to {}'.format(requested),
				 'request': serializer.data},
				status=status.HTTP_201_CREATED
			)
		except KeyError:
			return Response(
				{'error': 'You must include the friends username to create a friend request'},
				status= status.HTTP_400_BAD_REQUEST
				)
		except User.DoesNotExist:
			return Response({
				'error': 'Could not find that user'
				}, status=HTTP_400_BAD_REQUEST
			)

	def get(self, request, format=None):
		'''
		Return a list of friend requests that involve you in the form:
		{
			pending_me: [...],
			pending_them: [...]
		}
		'''
		pending_me = request.user.get_profile().friend_requests_pending_my_response()
		me_serializer = FriendRequestSerializer(pending_me, many=True)
		pending_them = request.user.get_profile().friend_requests_pending_their_response()
		them_serializer = FriendRequestSerializer(pending_them, many=True)
		return Response(
			{
				'pending_me': me_serializer.data,
				'pending_them': them_serializer.data
			},
			status=status.HTTP_200_OK
		)

class HandleFriendRequestReplies(AuthenticatedView):

	def post(self, request, format=None):
		'''
		Reply to a friend request.

		username (required) -- The username of the person who sent the request you are responding to
		accepted (required) -- Boolean stating whether we should accept the the request or decline it
		'''
		try:
			sender = User.objects.get(username=request.DATA['username'])
			sender = sender.get_profile()
			me = request.user.get_profile()
			accepted = request.DATA['accepted']
			if isinstance(accepted, unicode):
				# Fixes some weird bug where json bools are converted to unicode
				accepted = False if accepted == u'0' else True
			if accepted:
				print 'Accepting Request'
				request = me.accept_friend_request(sender)
				serializer = FriendRequestSerializer(request)
				return Response(
					{
					'detail':'Successfully accepted friend request from {}'.format(sender.user.username),
					'request': serializer.data
					},
					status=status.HTTP_200_OK
				)
			else:
				print 'Declining request'
				request = me.decline_friend_request(sender)
				serializer = FriendRequestSerializer(request)
				return Response(
					{'detail': 'Successfully declined friend request from {}'.format(sender.user.username),
					'request': serializer.data
					},
					status=status.HTTP_200_OK
				)

		except User.DoesNotExist:
			return Response(
				{'error': 'User could not be found with that username'},
				status=stuats.HTTP_404_NOT_FOUND
			)
		except KeyError:
			return Response(
				{'error': 'Invalid parameters for responding to a friend request'},
				status=status.HTTP_400_BAD_REQUEST
			)

class HandleFriends(AuthenticatedView):

	def get(self, request, format=None):
		'''
		Get a list of the logged in users friends

		return {
			"friends": [...]
		}
		'''
		profile = request.user.get_profile()
		friends = profile.friends.all()
		serializer = ProfileSerializerNoFriends(friends, many=True)
		return Response(
			{"friends": serializer.data},
			status=status.HTTP_200_OK
		)

	def delete(self, request, format=None):
		'''
		Remove a friend for the current user.

		username -- The username of the user to remove as friend
		'''
		me = request.user.get_profile()
		friend = me.remove_friend(request.QUERY_PARAMS['username'])
		serializer = ProfileSerializerNoFriends(friend)
		return Response(
			{'friend': serializer.data,
			'detail': 'Successfully Removed Friend.'},
			status=status.HTTP_200_OK
		)