import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
	"""This class represents the trivia test case"""

	def setUp(self):
		"""Define test variables and initialize app."""
		self.app = create_app()
		self.client = self.app.test_client
		self.database_name = "trivia_test"
		self.database_path = "postgres:///{}".format(self.database_name)
		self.q_id = 2
		setup_db(self.app, self.database_path)

		self.question = {
			"question": "Türkiye'nin başkenti hangi ilimizdir?",
			"answer": "Ankara",
			"difficulty": 1,
			"category": 3
		}

		self.wrong_question = {
			"question": "Türkiye'nin başkenti hangi ilimizdir?",
			"answer": "Ankara",
			"difficulty": 1
		}

		# binds the app to the current context
		with self.app.app_context():
			self.db = SQLAlchemy()
			self.db.init_app(self.app)
			# create all tables
			self.db.create_all()
	
	def tearDown(self):
		"""Executed after reach test"""
		pass
	
	def test_get_categories(self):
		res = self.client().get('/categories')
		data = json.loads(res.data)

		self.assertEqual(type(data["categories"]), type({}))
		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])

	def test_get_questions(self):
		res = self.client().get('/questions?page=1')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])
		self.assertGreater(len(data['questions']), 0)
		self.assertGreater(data["total_questions"], 0)
		self.assertEqual(type(data["categories"]), type({}))

	def test_delete_question(self):
		q_id = self.q_id
		res = self.client().delete(f'/questions/{q_id}')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])

		res = self.client().get('/questions')
		q_data = json.loads(res.data)

		found_deleted = False

		for q in q_data["questions"]:
			if q["id"] == q_id:
				found_deleted = True
				break
	
		self.assertFalse(found_deleted)

	def test_delete_question_fail_404(self):
		q_id = -100
		res = self.client().delete(f'/questions/{q_id}')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 404)
		self.assertFalse(data['success'])

	def test_create_question(self):
		res = self.client().post(f'/questions', json=self.question)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])

	def test_create_question_fail_400(self):
		res = self.client().post(f'/questions', json=self.wrong_question)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 400)
		self.assertFalse(data['success'])
		self.assertEqual(data['message'], 'invalid syntax')

	def test_search_question(self):
		search_term = "penicillin"
		res = self.client().post('questions', json={"searchTerm": search_term})
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])
		self.assertTrue(len(data["questions"]) == 1)

	def test_search_question_not_found(self):
		search_term = "penicillin2"
		res = self.client().post('questions', json={"searchTerm": search_term})
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])
		self.assertTrue(len(data["questions"]) == 0)

	def test_search_question_fail_400(self):
		search_term = "penicilin2"
		res = self.client().post('questions', json={"search_Term": search_term})
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 400)
		self.assertFalse(data['success'])
		self.assertEqual(data['message'], 'invalid syntax')

	def test_get_questions_by_category(self):
		id = 1 # Science
		res = self.client().get(f'/categories/{id}/questions')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])
		self.assertTrue(len(data["questions"]) == 3)

	def test_get_questions_by_category_fail_404(self):
		id = 100
		res = self.client().get(f'/categories/{id}/questions')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 404)
		self.assertFalse(data['success'])

	def test_quizzes(self):
		id = 1 # Science
		previous_questions = []
		questions = Question.query.order_by(Question.id).filter(Question.category == id).limit(2).all()
		for question in questions:
			previous_questions.append(question.format()['id'])
		json_obj = {
			"previous_questions": previous_questions,
      "quiz_category": {
				"id": id,
				"type": "Science"
			}
		}
		res = self.client().post(f'/quizzes', json=json_obj)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])

		question = data['question']
		found_prev = False

		for prev_question in previous_questions:
			if question['id'] == prev_question['id']:
				found_prev = True

		self.assertFalse(found_prev)

		
	"""
	TODO
	Write at least one test for each test for successful operation and for expected errors.
	"""


# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()