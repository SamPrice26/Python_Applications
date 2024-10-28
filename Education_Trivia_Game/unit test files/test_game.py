import threading
import unittest
from unittest.mock import patch, MagicMock
import io
from app.game import EducationTriviaGame


class TestEducationTriviaGame(unittest.TestCase):

    def setUp(self):
        # Create a game instance for each test
        self.game = EducationTriviaGame('TestUser')

    def test_calculate_score_correct_easy(self):
        # Test scoring when the answer is correct on easy difficulty
        score = self.game.calculate_score(correct=True, diff_level='easy', time_taken=10)
        self.assertEqual(score, 4)  # Expected score based on time factor

    def test_calculate_score_incorrect(self):
        # Test scoring when the answer is incorrect
        score = self.game.calculate_score(correct=False, diff_level='hard', time_taken=5)
        self.assertEqual(score, 0)  # No points for incorrect answers

    def test_get_answers(self):
        # Test the randomization of answers
        answers = ['A', 'B', 'C', 'D']
        shuffled_answers = self.game.get_answers(answers.copy())
        self.assertEqual(sorted(shuffled_answers), sorted(answers))  # Should contain same elements
        self.assertNotEqual(shuffled_answers, answers)  # Order should be different

    @patch('builtins.input', side_effect=['a'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_get_user_answer_correct_input(self, mock_stdout, mock_input):
        # Test getting a user answer with valid input
        index, time_taken = self.game.get_user_answer("Choose A, B, C, or D: ", 4)
        self.assertEqual(index, 0)  # 'A' corresponds to index 0
        self.assertGreater(time_taken, 0)  # Time taken should be positive

    @patch('builtins.input', side_effect=['z', 'a'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_get_user_answer_invalid_then_valid_input(self, mock_stdout, mock_input):
        # Test getting a user answer with invalid then valid input
        index, time_taken = self.game.get_user_answer("Choose A, B, C, or D: ", 4)
        output = mock_stdout.getvalue()
        self.assertIn("Invalid input", output)
        self.assertEqual(index, 0)  # 'A' corresponds to index 0

    @patch('builtins.input', side_effect=['a'])
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('time.sleep', return_value=None)
    def test_countdown_timer_with_answer(self, mock_sleep, mock_stdout, mock_input):
        # Test the countdown timer when an answer is provided in time
        timer_thread = threading.Thread(target=self.game.countdown_timer)
        timer_thread.start()
        self.game.user_input_ready.set()
        timer_thread.join()
        output = mock_stdout.getvalue()
        self.assertIn("Time remaining", output)

    @patch('requests.get')
    def test_fetch_questions(self, mock_get):
        # Mock API response
        mock_get.return_value.json.return_value = {
            'questions': [{'question_id': 1, 'question_text': 'Sample Question'}]
        }
        questions = self.game.fetch_questions('Maths', 'easy')
        self.assertEqual(len(questions), 1)
        self.assertEqual(questions[0]['question_text'], 'Sample Question')

    @patch('builtins.input', side_effect=['n'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_play_again_no(self, mock_stdout, mock_input):
        # Test play again functionality with 'n'
        result = self.game.play_again()
        self.assertFalse(result)
        output = mock_stdout.getvalue()
        self.assertIn("Bye TestUser", output)


if __name__ == '__main__':
    unittest.main()
