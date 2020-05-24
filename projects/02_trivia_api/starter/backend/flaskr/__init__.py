import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
	page = request.args.get('page', 1, type=int)
	start =  (page - 1) * QUESTIONS_PER_PAGE
	end = start + QUESTIONS_PER_PAGE

	questions = [question.format() for question in selection]
	current_questions = questions[start:end]

	return current_questions

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__)
	setup_db(app)
	
	'''
	@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
	'''
	CORS(app) # CAREFUL

	'''
	@TODO: Use the after_request decorator to set Access-Control-Allow
	'''
	# CORS Headers 
	@app.after_request
	def after_request(response):
		response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
		response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
		return response

	'''
	GET /categories 
	Get all available categories

	Example Request: curl 'http://localhost:5000/categories'

	Expected Result:
	{
		"categories": {
			"1": "Science",
			"2": "Art",
			"3": "Geography",
			"4": "History",
			"5": "Entertainment",
			"6": "Sports"
		},
		"success": true
	}
	'''
	@app.route('/categories', methods=['GET'])
	def categories():
		categories = Category.query.all()
		categories_dict = {}
		for category in categories:
			category = category.format()
			categories_dict[category['id']] = category['type']
		return jsonify({
			"success": True,
			"categories": categories_dict
		})


	'''
	GET \questions?page=1
	Retrieve all the questions with pagination. 
	Page size is 10. If no page is specified as a parameter, first page is retrieved.
	Returns questions for the given page, current category, all categories and total number of questions

	Example Request: curl 'http://localhost:5000/questions?page=2'

	Example Response: 

	{
		"categories": {
			"1": "Science",
			"2": "Art",
			"3": "Geography",
			"4": "History",
			"5": "Entertainment",
			"6": "Sports"
		},
		"current_category": null,
		"questions": [
			{
			"answer": "Agra",
			"category": 3,
			"difficulty": 2,
			"id": 15,
			"question": "The Taj Mahal is located in which Indian city?"
			},
			{
			"answer": "Escher",
			"category": 2,
			"difficulty": 1,
			"id": 16,
			"question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
			},
			...
		],
		"success": true,
		"total_questions": 21
	}

	'''
	@app.route('/questions', methods=['GET'])
	def retrieve_questions():
		selection = Question.query.order_by(Question.id).all()
		total_num_questions = len(selection)
		current_questions = paginate_questions(request, selection)
		categories = Category.query.all()
		categories_dict = {}
		for category in categories:
			category = category.format()
			categories_dict[category['id']] = category['type']
		return jsonify({
			"success": True,
			"questions": current_questions,
			"current_category": None,
			"categories": categories_dict,
			"total_questions": total_num_questions
		})

	'''
	DELETE /questions/<int:question_id>
	Deletes the question with given id 

	Example Request: curl --request DELETE 'http://localhost:5000/questions/26'

	Example Response: 
	{
		"deleted": 26,
		"success": true
	}
	'''
	@app.route('/questions/<int:question_id>', methods=['DELETE'])
	def delete_question(question_id):
		question = Question.query.filter(Question.id == question_id).one_or_none()

		if question is None:
			abort(404)

		question.delete()

		return jsonify({
		'success': True,
		'deleted': question_id
		})


	'''
	POST /questions
	Creates a new question or searches for a question.
	Requires the question and answer text, 
	category, and difficulty score for creating question.
	Requires search term for searching.

	Example Request: (Create)
	curl --location --request POST 'http://localhost:5000/questions' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			"question": "What is the most crowded city in Turkey?",
			"answer": "İstanbul",
			"difficulty": 3,
			"category": 3
		}'

	Example Response: 
	{
		"success": true
	}

	Example Request: (Search)
	curl --location --request POST 'http://localhost:5000/questions' \
	--header 'Content-Type: application/json' \
	--data-raw '{
		"searchTerm": "title"
	}'

	Example Response: 
	{
		"current_category": null,
		"questions": [
			{
			"answer": "Maya Angelou",
			"category": 4,
			"difficulty": 2,
			"id": 5,
			"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
			},
			{
			"answer": "Edward Scissorhands",
			"category": 5,
			"difficulty": 3,
			"id": 6,
			"question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
			}
		],
		"success": true,
		"total_questions": 2
	}
	'''
	@app.route('/questions', methods=['POST'])
	def create_question():
		body = request.get_json()

		question = body.get('question', None)
		answer = body.get('answer', None)
		difficulty = body.get('difficulty', None)
		category = body.get('category', None)
		search_term = body.get('searchTerm', None)

		if search_term:
			selection = Question.query.order_by(Question.id) \
						.filter(Question.question.ilike(f'%{search_term}%')).all()

			current_questions = paginate_questions(request, selection)
		
			return jsonify({
				'success': True,
				'questions': current_questions,
				'total_questions': len(selection),
				'current_category': None
			})

		else:
		
			if question is None or answer is None or answer is None or category is None:
				abort(400)
			
			question = Question(question=question, 
								answer=answer, 
								difficulty=difficulty, 
								category=category)

			question.insert()

			return jsonify({
				"success": True
			})

	'''
	GET /categories/<int:category_id>/questions
	Retrieve questions based on category. 

	Example Request: curl 'http://localhost:5000/categories/1/questions'

	Example Response:
	{
		"current_category": "Science",
		"questions": [
			{
			"answer": "The Liver",
			"category": 1,
			"difficulty": 4,
			"id": 20,
			"question": "What is the heaviest organ in the human body?"
			},
			{
			"answer": "Alexander Fleming",
			"category": 1,
			"difficulty": 3,
			"id": 21,
			"question": "Who discovered penicillin?"
			},
			{
			"answer": "Blood",
			"category": 1,
			"difficulty": 4,
			"id": 22,
			"question": "Hematology is a branch of medicine involving the study of what?"
			}
		],
		"success": true,
		"total_questions": 3
	}
	'''
	@app.route('/categories/<int:category_id>/questions', methods=['GET'])
	def get_questions_by_category(category_id):

		
		category = Category.query.get(category_id)
		if not category:
			abort(404)

		selection = Question.query.order_by(Question.id) \
			.filter(Question.category == category_id).all()
		total_num_questions = len(selection)
		current_questions = paginate_questions(request, selection)

		return jsonify({
			"success": True,
			"questions": current_questions,
			"current_category": category.format()['type'],
			"total_questions": total_num_questions
		})

	'''
	POST /quizzes
	Get random questions to play the quiz. 
	Requires category and previous question parameters 
	and return a random questions within the given category, 
	if provided, and that is not one of the previous questions. 
	If category is given with id 0, a random question is chosen from all questions.

	Example Request:
	curl --request POST 'http://localhost:5000/quizzes' \
	--header 'Content-Type: application/json' \
	--data-raw '{
		"previous_questions": [],
		"quiz_category": {"id": 1, "type": "Science"}
	}'

	Example Response:
	{
		"question": {
			"answer": "Blood",
			"category": 1,
			"difficulty": 4,
			"id": 22,
			"question": "Hematology is a branch of medicine involving the study of what?"
		},
		"success": true
	}

	'''

	@app.route('/quizzes', methods=['POST'])
	def get_quiz_question():

		body = request.get_json()

		previous_question_ids = body.get('previous_questions', [])
		quiz_category = body.get('quiz_category', None)

		if quiz_category is None or type(quiz_category) is not type({}):
			abort(400)

		if 'id' not in quiz_category:
			abort(400)

		if quiz_category['id'] == 0:
			selection = Question.query.all()
		else:
			selection = Question.query.order_by(Question.id) \
				.filter(Question.category == quiz_category['id']).all()
		
		questions = [question.format() for question in selection]
		questions_filtered = []
		for question in questions:
			if question['id'] not in previous_question_ids:
				questions_filtered.append(question)

		if questions_filtered == []:
			question = None
		else:
			question = random.choice(questions_filtered)
		
		return jsonify({
			"success": True,
			"question": question
		})

	'''
	@TODO: 
	Create error handlers for all expected errors 
	including 404 and 422. 
	'''

	@app.errorhandler(404)
	def not_found(error):
		return jsonify({
			'success': False,
			'error': 404,
			'message': 'Resource not found'
		}), 404

	@app.errorhandler(422)
	def unprocessable(error):
		return jsonify({
			'success': False,
			'error': 422,
			'message': 'request cannot be processed'
		}), 422

	@app.errorhandler(400)
	def bad_request(error):
		return jsonify({
			'success': False,
			'error': 400,
			'message': 'invalid syntax'
		}), 400

	@app.errorhandler(500)
	def server_error(error):
		return jsonify({
			'success': False,
			'error': 500,
			'message': 'internal server error'
		}), 500
	
	return app

		