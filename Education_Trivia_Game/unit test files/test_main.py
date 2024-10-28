import builtins
import unittest
from unittest.mock import patch

from combinedfiles2.main import handle_existing_user, handle_new_user, current_user
from combinedfiles2.user import Student, Teacher, Parent


class TestGame(unittest.TestCase):
    @patch('combinedfiles2.main.load_user_from_database')
    @patch('combinedfiles2.main.get_user_id')
    @patch('combinedfiles2.main.hash_password')
    @patch('builtins.input', side_effect=['testuser', 'testpass'])
    def test_handle_existing_user(self, mock_input, mock_hash_password, mock_get_user_id, mock_load_user):
        # Test if handle_existing_user sets the current_user correctly
        mock_load_user.return_value = (Student('testuser', 'testemail',
                                               mock_hash_password('testpass'), 0), 1, 'student')
        mock_get_user_id.return_value = 1
        mock_hash_password.return_value = 'hashedtestpass'

        handle_existing_user()
        self.assertIsInstance(current_user, Student)
        self.assertEqual(current_user.username, 'testuser')

    @patch('combinedfiles2.main.create_user_in_db')
    @patch('combinedfiles2.main.get_user_id')
    @patch('combinedfiles2.main.hash_password')
    @patch('builtins.input', side_effect=['student', 'newstudent', 'student@example.com', 'studentpass'])
    def test_handle_new_user_student(self, mock_input, mock_hash_password, mock_get_user_id, mock_create_user):
        # Test if handle_new_user sets the current_user correctly for a student
        mock_create_user.return_value = True
        mock_get_user_id.return_value = None
        mock_hash_password.return_value = 'hashedstudentpass'

        handle_new_user()
        self.assertIsInstance(current_user, Student)
        self.assertEqual(current_user.username, 'newstudent')

    @patch('combinedfiles2.main.create_user_in_db')
    @patch('combinedfiles2.main.get_user_id')
    @patch('combinedfiles2.main.hash_password')
    @patch('builtins.input', side_effect=['teacher', 'newteacher', 'teacher@example.com', 'teacherpass', 'Math'])
    def test_handle_new_user_teacher(self, mock_input, mock_hash_password, mock_get_user_id, mock_create_user):
        mock_create_user.return_value = True
        mock_get_user_id.return_value = None
        mock_hash_password.return_value = 'hashedteacherpass'

        handle_new_user()
        self.assertIsInstance(current_user, Teacher)
        self.assertEqual(current_user.username, 'newteacher')

    @patch('combinedfiles2.main.create_user_in_db')
    @patch('combinedfiles2.main.get_user_id')
    @patch('combinedfiles2.main.hash_password')
    @patch('builtins.input',
           side_effect=['parent', 'newparent', 'parent@example.com', 'parentpass', 'student1, student2'])
    def test_handle_new_user_parent(self, mock_input, mock_hash_password, mock_get_user_id, mock_create_user):
        mock_create_user.return_value = True
        mock_get_user_id.return_value = None
        mock_hash_password.return_value = 'hashedparentpass'

        handle_new_user()
        self.assertIsInstance(current_user, Parent)
        self.assertEqual(current_user.username, 'newparent')


if __name__ == '__main__':
    unittest.main()