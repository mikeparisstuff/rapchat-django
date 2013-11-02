from django.test import TestCase
from rest_framework.test import APITestCase
from groupsessions.models import GroupSession
from rest_framework.authtoken.models import Token

class TestGroupSessions(APITestCase):

	fixtures = ['test_fixtures.json']

	def setUp(self):
		token = Token.objects.get(user__username='DeerDoe')
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
		self.client.content_type = 'application/json'

	def test_create_session_valid_info(self):
		data = {
			'title': 'Rap Session Title',
			'crowd': 1
		}		
		res = self.client.post(
			'/sessions/',
			data=data
		)
		self.assertEqual(res.status_code, 201)
		self.assertNotNone(res.data['session'])
