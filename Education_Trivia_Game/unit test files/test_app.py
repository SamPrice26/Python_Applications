import unittest
from flask import Flask, json
from app import app

class FlaskAppTestCase(unittest.Testcase):
    # Setting up a test for the
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Check to see if the login was successful
    def test_login_success(self):
        payload = json.dumps({
            "username": "testuser"
            "password": "PASSWORD"
        })
        response = self.app.post('/login', data=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data["message"], "Login successful")

    # Check to see if the login failed
    def test_login_fail(self):
        payload = json.dumps({
            "username": "testuser",
            "password": "<PASSWORD>"
        })
        response = self.app.post('/login', data=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertTrue(data["message"], "Login failed")

    # check to see if registration was successful
    def test_register_success(self):
        payload = json.dumps({
            "username": "newuser",
            "email": "<EMAIL>",
            "password": "<PASSWORD>",
            "user_type": "student"
        })
        response = self.app.post('/register', data=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data["success"])
        self.assertTrue(data["message"], "Register successful")

# Check to see if the user registration failed
    def test_register_fail(self):
        payload = json.dumps({
            "username": "newuser",
            "email": "<EMAIL>",
            "password": "<PASSWORD>",
            "user_type": "student"
        })
        response = self.app.post('/register', data=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", data)
        self.assertTrue(data["message"], "Register failed")

# Test to see the list of subjects available
    def test_get_subject(self):
        response = self.app.get('/subject')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["subjects", data])

# Check to see if the retrieval of questions operates as it should
    def test_get_questionset(self):
        response = self.app.get('/questionset')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["questionset", data])

# Check/Test to see the creation of the quiz
    def test_create_quiz(self):
        payload = json.dumps({
            "teacher_id": 1,
            "quiz_name": "Sample Quiz",
            "subject_id": 1,
            "difficulty": "medium"   # change level of difficulty where applicable
        })
        response = self.app.post('/create_quiz', data=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data["success"])
        self.assertTrue(data["message"], "Quiz created successfully")

# Test the quizzes which can be retrieved by teachers
    def test_get_teacher_quizzes(self):
        response = self.app.get('/teacher_quizzes')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["teacher_quizzes", data])

# Testing the saving of scores
    def test_save_score(self):
        payload = json.dumps({
            "username": "studentuser"
            "quiz_name": "Sample Quiz",
            "score": 95
        })
        response = self.app.post('/save_score', data=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data["message", data])
        self.assertTrue(data["message"], "Score saved successfully")

# Test the results of the quiz through retrieval
    def test_quiz_results(self):
        response = self.app.get('/quiz_results')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["quiz_results", data])

if __name__ == '__main__':
    unittest.main()
