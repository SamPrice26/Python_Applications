import unittest
from unittest.mock import patch, MagicMock
from combinedfiles2.user import Student, Teacher, Parent


class TestUserClasses(unittest.TestCase):

    @patch('combinedfiles2.user.execute_query')
    @patch('combinedfiles2.user.fetch_all_query')
    @patch('combinedfiles2.user.with_connection', lambda x: x)  # Mocking the decorator to pass through
    def test_student_add_score(self, mock_fetch_all_query, mock_execute_query):
        # Set up mock return values
        mock_fetch_all_query.return_value = [{'id': 1}]
        student = Student('testuser', 'testemail', 'testpass')

        # Test adding a score
        student.add_score(85)

        # Check the score list
        self.assertIn(85, student.scores)

        # Check if the update_score_in_db method was called with correct arguments
        mock_execute_query.assert_called_with(
            None,  # Mocked connection
            """
            INSERT INTO scores (student_id, quiz_id, score)
            VALUES (%s, %s, %s)
            """,
            (1, None, 85)
        )

    @patch('combinedfiles2.user.execute_query')
    @patch('combinedfiles2.user.fetch_all_query')
    @patch('combinedfiles2.user.with_connection', lambda x: x)  # Mocking the decorator to pass through
    def test_student_get_average_score(self, mock_fetch_all_query, mock_execute_query):
        student = Student('testuser', 'testemail', 'testpass')
        student.scores = [80, 90, 70]

        # Test average score
        self.assertEqual(student.get_average_score(), 80.0)

    @patch('combinedfiles2.user.execute_query')
    @patch('combinedfiles2.user.fetch_all_query')
    @patch('combinedfiles2.user.with_connection', lambda x: x)  # Mocking the decorator to pass through
    def test_student_get_student_id_from_user_db(self, mock_fetch_all_query, mock_execute_query):
        mock_fetch_all_query.return_value = [{'id': 1}]
        student = Student('testuser', 'testemail', 'testpass')

        # Test getting student ID
        student_id = student.get_student_id_from_user_db()
        self.assertEqual(student_id, 1)

    @patch('combinedfiles2.user.execute_query')
    @patch('combinedfiles2.user.fetch_all_query')
    @patch('combinedfiles2.user.with_connection', lambda x: x)  # Mocking the decorator to pass through
    def test_teacher_assign_mark(self, mock_fetch_all_query, mock_execute_query):
        teacher = Teacher('teacheruser', 'teacheremail', 'teacherpass', ['Math'])
        student = Student('studentuser', 'studentemail', 'studentpass')

        with patch.object(student, 'add_score') as mock_add_score:
            teacher.assign_mark(student, 95)
            mock_add_score.assert_called_with(95)

    @patch('combinedfiles2.user.execute_query')
    @patch('combinedfiles2.user.fetch_all_query')
    @patch('combinedfiles2.user.with_connection', lambda x: x)  # Mocking the decorator to pass through
    def test_parent_get_pupils_scores(self, mock_fetch_all_query, mock_execute_query):
        mock_fetch_all_query.return_value = [{'score': 90}, {'score': 85}]
        parent = Parent('parentuser', 'parentemail', 'parentpass', ['student1', 'student2'])

        with patch('combinedfiles2.user.Parent.load_student_scores') as mock_load_student_scores:
            mock_load_student_scores.return_value = [90, 85]
            scores = parent.get_pupils_scores()
            self.assertEqual(scores, {
                'student1': [90, 85],  # Adjust based on your actual expected behavior
                'student2': [90, 85]  # Adjust based on your actual expected behavior
            })

    @patch('combinedfiles2.user.execute_query')
    @patch('combinedfiles2.user.fetch_all_query')
    @patch('combinedfiles2.user.with_connection', lambda x: x)  # Mocking the decorator to pass through
    def test_parent_load_student_scores(self, mock_fetch_all_query, mock_execute_query):
        mock_fetch_all_query.return_value = [{'score': 90}]
        scores = Parent.load_student_scores('student1')
        self.assertEqual(scores, [90])


if __name__ == '__main__':
    unittest.main()