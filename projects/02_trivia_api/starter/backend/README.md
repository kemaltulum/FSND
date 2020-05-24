# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## API Documentation

### Error Handling

Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 500: Internal Server Error

### Endpoints

#### GET /categories 
- General:
    - Returns all available categories
    - Returns a dictionary whose keys are ids of categories and values are corresponding category types.

- **Example Request**: `curl 'http://localhost:5000/categories'`

- **Expected Result**:

    ```json
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
    ```

#### GET \questions?page=int
- General
    - Retrieve all the questions with pagination. 
	- Page size is 10. If no page is specified as a parameter, first page is retrieved.
	- Returns questions for the given page, current category, all categories and total number of questions

- **Example Request**: `curl 'http://localhost:5000/questions?page=2'`

- **Example Response**: 
```json
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
		],
		"success": true,
		"total_questions": 21
	}
```

#### DELETE /questions/<int:question_id>
- General
	- Deletes the question with given id 

- **Example Request:** `curl --request DELETE 'http://localhost:5000/questions/26'`

- **Example Response:**
```json 
	{
		"deleted": 26,
		"success": true
	}
```


#### POST /questions
- General
	- Creates a new question or searches for a question.
	- Requires the question and answer text, category, and difficulty score for creating question.
	- Requires search term for searching.

- **Example Request:** (Create)
```bash 
	curl --location --request POST 'http://localhost:5000/questions' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			"question": "What is the most crowded city in Turkey?",
			"answer": "İstanbul",
			"difficulty": 3,
			"category": 3
		}'
```

- **Example Response:**
```json 
	{
		"success": true
	}
```

- **Example Request:** (Search)
```bash
	curl --location --request POST 'http://localhost:5000/questions' \
	--header 'Content-Type: application/json' \
	--data-raw '{
		"searchTerm": "title"
	}'
```

- **Example Response:** 
```json
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
```

#### GET /categories/<int:category_id>/questions
- General
	- Retrieve questions based on category. 

- **Example Request:** `curl 'http://localhost:5000/categories/1/questions'`

- **Example Response:**
```json
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
```

#### POST /quizzes
- General
    - Get random questions to play the quiz. 
	- Requires category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
	- If category is given with id 0, a random question is chosen from all questions.

- **Example Request:**
```bash
	curl --request POST 'http://localhost:5000/quizzes' \
	--header 'Content-Type: application/json' \
	--data-raw '{
		"previous_questions": [],
		"quiz_category": {"id": 1, "type": "Science"}
	}'
```

- **Example Response:**
```json
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
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py

```

```

```