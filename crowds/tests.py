"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from rest_framework.test import APITestCase
from crowds.models import Crowd
from rest_framework.authtoken.models import Token

class TestCrowds(APITestCase):

	fixtures = ['test_fixtures.json']

	def setUp(self):
		token = Token.objects.get(user__username='DeerDoe')
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
		self.client.content_type = 'application/json'

	def test_create_crowd_valid_info(self):
		data = {
			'title': 'Cha Boys',
			'members': [1,3]
		}
		res = self.client.post(
			'/crowds/',
			data=data
		)
		self.assertEqual(res.status_code, 201)
		self.assertEqual(res.data['crowd']['title'], 'Cha Boys')
		self.assertEqual(len(res.data['crowd']['members']), 3)

	def test_get_crowds(self):
		res = self.client.get(
			'/crowds/'
		)
		self.assertEqual(res.status_code, 200)
		self.assertIsNotNone(res.data['crowds'])
		self.assertEqual(len(res.data['crowds'][0]['members']), 3)
