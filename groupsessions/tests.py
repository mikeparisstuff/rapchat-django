from django.test import TestCase
from rest_framework.test import APITestCase
from groupsessions.models import GroupSession
from rest_framework.authtoken.models import Token
import os

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
		self.assertIsNotNone(res.data['session'])

	def test_get_sessions(self):
		res = self.client.get('/sessions/')
		self.assertEqual(res.status_code, 200)
		self.assertEqual(res.data['sessions'][0]['title'], 'Rap Sesh')
		self.assertEqual(res.data['sessions'][0]['comments'][0]['text'], 'This is a comment')

	# def test_upload_file(self):
	# 	path = os.path.dirname(__file__)
	# 	path = os.path.join(path, 'test_upload.mp4')
	# 	f = open(path, 'rb')
	# 	data = {
	# 		'clip': f,
	# 		'session': 1,
	# 		'duration': 7
	# 	}
	# 	res = self.client.post(
	# 		'/sessions/addclip/',
	# 		data=data
	# 	)
	# 	f.close()
	# 	self.assertEqual(res.status_code, 200)

	def test_get_comments(self):
		data = {'session': 1}
		res = self.client.get('/sessions/comments/1/')
		print res.data
		self.assertEqual(res.status_code, 200)
		self.assertIsNotNone(res.data['comments'])
		self.assertEqual(len(res.data['comments']), 2)

	def test_add_comment_to_session(self):
		data = {
			'session': 1,
			'comment_text': 'This was pretty tight...'
		}
		res = self.client.post(
			'/sessions/comments/',
			data = data
		)
		self.assertEqual(res.status_code, 200)
		self.assertIsNotNone(res.data['comment'])