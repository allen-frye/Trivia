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
        self.database_path = "postgresql://allen:plumbflo22!@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'what is the average velocity of a sparrow?',
            'answer': '5000 miles per hour',
            'category': '1',
            'difficulty': '3'
            }    
        # self.quiz_category['id'] = "3"
        # self.previous_questions = []
        
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    


    def tearDown(self):
        """Executed after reach test"""
        pass

        """
        TODO
        Write at least one test for each test for successful operation and for expected errors.
        """

   # categories  all
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
    
    #get questions
 
    def test_get_all_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    #create question

    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
 
 
    #delete question - test fails if id does not exist. uncomment when going lie
    def test_delete_question(self):
        res = self.client().delete("/questions/103")
        # print(res.data)
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 103).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 103)
        self.assertEqual(question, None)
   
    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        # print(res.data)
        # data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        # self.assertEqual(data["success"], False)
        # self.assertEqual(data["message"], "unprocessable")


   #search question - 

    def test_search_results_with_results(self):
        res = self.client().post('/questions/search', json={'searchTerm':'soccer'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # Bug: total_questions returns false with only one result. 
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 2)


    #get category questions

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/5/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(len(data['questions']), 2)

    def test_category_does_not_exist(self):
        res = self.client().get('/categories/10000/questions')
        
        self.assertEqual(res.status_code, 404)
       

    # post quizzes

    def test_creating_quizzes(self):
        res = self.client().post("/quizzes", json={"previous_questions": [], "quiz_category": {"type": "History", "id": "4"}})
       
        data = json.loads(res.data)
        print(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['question'])

    def test_quiz_category_not_found(self):
        res = self.client().post("/quizzes", json={"previous_questions": [], "quiz_category": {"type": "space", "id": "10000"}})
       
        # data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()