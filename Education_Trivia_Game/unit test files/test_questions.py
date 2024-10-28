import unittest
from unittest.mock import patch, MagicMock
from questions import QuestionManager

class TestQuestionManager(unittest.TestCase):
    def setUp(self):
        self.subject = "Test Subject"
        self.question_manager = QuestionManager(self.subject)

    @patch('questions.execute_query')
    @patch('questions.with_connection')
    def test_add_question(self, mock_with_connection, mock_execute_query):
        question_data = {
            'difficulty': 'easy',
            'question_text': 'What is the opposite of cold?',
            'option_a': 'Warm',
            'option_b': 'Hot',
            'option_c': 'Cool',
            'option_d': 'Freezing',
            'correct_option': 'Hot'
        }
        self.question_manager.add_question(question_data)
        mock_execute_query.assert_called_with(question_data)

    @patch('questions.fetch_all_query')
    @patch('questions.with_connection')
    def test_get_filtered_questions(self, mock_with_connection, mock_fetch_all_query):
        difficulty_level = 'easy'
        self.question_manager.get_filtered_questions(difficulty_level)
        mock_fetch_all_query.assert_called_with(difficulty_level)

    @patch('questions.execute_query')
    @patch('questions.with_connection')
    def test_update_question(self, mock_with_connection, mock_execute_query):
        question_id = 1
        question_data = {
            'difficulty': 'easy',
            'question_text': 'What is 2 + 3?',
            'option_a': '4',
            'option_b': '5',
            'option_c': '6',
            'option_d': '7',
            'correct_option': '5',
        }
        self.question_manager.update_question(question_id, question_data)
        mock_execute_query.assert_called_with(question_data)

    @patch('questions_fetch_all_query')
    @patch('questions.with_connection')
    def test_get_available_subjects(self, mock_with_connection, mock_fetch_all_query):
        self.question_manager.get_available_subjects()
        mock_fetch_all_query.assert_called_with()

    @patch('questions_fetch_all_query')
    @patch('questions.with_connection')
    def test_get_questions_by_difficulty(self, mock_with_connection, mock_fetch_all_query):
        difficulty_level = 'easy'
        self.question_manager.get_questions_by_difficulty(difficulty_level)
        mock_fetch_all_query.assert_called_with(difficulty_level)

    @patch('questions.execute_query')
    @patch('questions.with_connection')
    def test_delete_question(self, mock_with_connection, mock_execute_query):
        question_id = 1
        self.question_manager.delete_question(question_id)
        mock_execute_query.assert_called_with(question_id)

if __name__ == '__main__':
    unittest.main()
