from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from users.models import User, FriendRequest
import json


class TestUsers(APITestCase):

	fixtures = ['test_fixtures.json']

	def setUp(self):
		# self.client = APIClient()
		pass

	def test_create_user_all_info(self):
		data = {
			'username': 'Parisi',
			'email': 'mlp5ab@virginia.edu',
			'first_name': 'Michael',
			'last_name': 'Paris',
			'phone_number': '757-285-6806',
			'password': 'wonderboy'
		}
		res = self.client.post(
			'/users/',
			data=data
		)
		self.assertEqual(res.status_code, 201)
		self.assertNotEqual(res.data['token'], None)
		self.assertEqual(res.data['user']['username'],'Parisi')
		self.assertEqual(res.data['user']['first_name'],'Michael')
		self.assertEqual(res.data['user']['last_name'],'Paris')

	def test_create_user_min_info(self):
		data = {
			'username': 'NerdsRope',
			'email': 'nerdy@example.com',
			'password': 'forgetit'
		}
		res = self.client.post(
			'/users/',
			data=data
		)
		self.assertEqual(res.status_code, 201)
		self.assertNotEqual(res.data['token'], None)
		self.assertEqual(res.data['user']['username'],'NerdsRope')		

	def test_create_user_invalid_info(self):
		data = {
			'username': 'needanemail',
			'password': 'noemail'
		}
		res = self.client.post(
			'/users/',
			data=data
		)
		self.assertEqual(res.status_code, 400)
		self.assertNotEqual(res.data['error_description'], None)
		#TODO: Add more assertions once Serializers are more fleshed out


class TestFriendRequests(APITestCase):
	fixtures = ['test_fixtures.json']	

	def setUp(self):
		token = Token.objects.get(user__username='DeerDoe')
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

	def test_create_friend_request(self):
		data = {
			'username': 'WhoAmI'
		}
		res = self.client.post(
			'/friends/requests/',
			data=data
		)
		self.assertEqual(res.status_code, 201)
		self.assertIn('WhoAmI', res.data['detail'])

	def test_get_my_requests(self):
		res = self.client.get(
			'/friends/requests/'
		)
		self.assertEqual(res.status_code, 200)
		self.assertEqual(len(res.data['pending_me']), 2)
		self.assertEqual(len(res.data['pending_them']), 1)

	def test_create_friend_request_no_auth(self):
		self.client.credentials(HTTP_AUTHORIZATION='')
		data = {
			'username': 'WhoAmI'
		}
		res = self.client.post(
			'/friends/requests/',
			data=data
		)
		self.assertEqual(res.status_code, 401)

	def test_accept_friend_request(self):
		data = {
			'username': 'Slappher',
			'accepted': True
		}
		res = self.client.post(
			'/friends/requests/reply/',
			data=data
		)
		self.assertEqual(res.status_code, 200)
		profile = User.objects.get(username='DeerDoe').get_profile()
		friends = profile.friends
		self.assertEqual(friends.count(), 3)
		self.assertIsNotNone(friends.get(user__username='Slappher'))

	def test_decline_friend_request(self):
		data = {
			'username': 'WhoAmI',
			'accepted': False
		}
		res = self.client.post(
			'/friends/requests/reply/',
			data=data
		)
		self.assertEqual(res.status_code, 200)
		with self.assertRaises(FriendRequest.DoesNotExist):
			FriendRequest.objects.get(sender=1, requested=2)

	def test_list_friends(self):
		res = self.client.get(
			'/friends/'
		)
		self.assertEqual(len(res.data['friends']), 2)


