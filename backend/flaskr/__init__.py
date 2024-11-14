import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
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
  CORS(app)
 
  
  # CORS Headers

  @app.after_request
  def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
    )
    return response
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route("/categories")
  def retrieve_categories():
    
    categories = Category.query.order_by(Category.type).all()
    # Rahul's solution
    # https://knowledge.udacity.com/questions/224220
    categories_formatted = {category.id: category.type for category in categories}  
    # selection = Category.query.order_by(Category.type).all()
       
       
    if len(categories_formatted) == 0:
      abort(404)

    return jsonify(
      {
        "success": True,
        "categories": categories_formatted,

      }
    )
  @app.route("/questions")
  def getQuestions():
    # questions_list = []
    # categories = []
    categories = Category.query.order_by(Category.type).all()
    selection = Question.query.order_by(Question.id).all()
    # questions_count = len(selection)
    current_questions = paginate_questions(request, selection)
    # categories = Category.query.filter_by(id=current_questions.category).first()
    
    # Rahul's solution
    # https://knowledge.udacity.com/questions/224220
    categories_formatted = {category.id: category.type for category in categories}
    # for item in categories_list:
    #   categories.append(item.type)


    if len(current_questions) == 0:
      abort(404)

    return jsonify(
      {
        "success": True,
        "questions": current_questions,
        "total_questions": len(Question.query.all()),
        "current_category": '',
        # Category.query.filter_by(id=current_questions.category).first(),
        "categories": categories_formatted
      }
    )
  '''
  @TODO: DONE
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: OK - At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  '''
  @TODO: DONE 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route("/questions/<int:question_id>", methods=["DELETE"])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      return jsonify(
        {
        "success": True,
        "deleted": question_id
                    
        }
      )

    except:
      abort(422)



  '''
  @TODO: Done
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route("/questions", methods=["POST"])
  def create_question():
    body = request.get_json()


    new_question = body.get("question", None)
    new_answer = body.get("answer", None)
    new_difficulty = body.get("difficulty", None)
    new_category = body.get("category", None)

    try:
      question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
      question.insert()

        # selection = Book.query.order_by(Book.id).all()
        # current_books = paginate_books(request, selection)

      return jsonify(
        {
          "success": True,
          "created": question.id
          }
      )

    except:
      abort(422)

  '''
  @TODO: DONE
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route("/questions/search", methods=["POST"])
  def search_question():

   # https://knowledge.udacity.com/questions/267545
    body = request.get_json()
    search_term = body.get('searchTerm', None)

    look_for = '%{0}%'.format(search_term)
    questions = Question.query.filter(Question.question.ilike(look_for)).all()

    current_questions = paginate_questions(request, questions)
    
    result = {
      "success": True,
      "total_questions": len(questions),
      # "questions": [],
      "questions": current_questions,
      "current_category": None      
      }
    

    return result

  '''
  @TODO: DONE
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, cliking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route("/categories/<int:category_id>/questions", methods=["GET"])
  def get_category(category_id):
    # body = request.get_json()
    
    category = Category.query.filter_by(id=category_id).one_or_none()
    
    if category is None:
        abort(404)

    # category_name = category.type
    try:
      questions = Question.query.filter_by(category=str(category_id)).all()
      # questions = Question.query.filter(
      #           Question.category == str(category_id)
      #       ).all()

      if questions is None:
        abort(404)

      current_questions = paginate_questions(request, questions) 
      result = { 
        "success": True,
        "questions": current_questions,
        "totalQuestions": len(current_questions),
        "currentCategory": None
        }

      return result

    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route("/quizzes", methods=["POST"])
  def set_quiz():
    body = request.get_json()
    previous_questions = body.get('previous_questions', [])
    quiz_category = body.get('quiz_category', 0)
    

    try:
      if quiz_category['id'] == 0:
        quiz = Question.query.filter(Question.id.not_in(previous_questions)).all()

      else:
        quiz = Question.query.filter(Question.category==quiz_category['id']).filter(Question.id.not_in(previous_questions)).all()

    # category = Category.query.filter_by(id=body.get(quiz_category).one_or_none()
    
    # have to randomize query and not include prev question
    # questions = Question.query.filter_by(category=str(category_id)).all()
      
      current_question = random.choice(quiz).format()

      result = {
      "success": True,
      "question": current_question

      }

      return result
     
    except:
      abort(400) 
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422.
  Done 
  '''
  
  return app

    