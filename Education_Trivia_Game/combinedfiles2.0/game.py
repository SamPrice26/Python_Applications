import logging
import random
import threading
import time
from questions import QuestionManager
from utils import with_connection, execute_query, fetch_one_query, fetch_all_query
from config import DATABASE_CONFIG


class EducationTriviaGame:
    timeout_duration = 30  # Time limit for answering questions

    def __init__(self, current_user):
        if not current_user:
            raise ValueError("Current user cannot be None")
        self.current_user = current_user
        self.question_manager = None  # Initialize the question manager later with a subject
        self.timer_expired = False
        self.user_input_ready = threading.Event()
        self.user_input = None
        self.score = 0

    def play_game(self, student_id, db_key='trivia_db'):
        try:
            subject_name, difficulty_level = self.get_quiz_preferences(db_key=db_key)
            if not subject_name or not difficulty_level:
                logging.error("Error fetching quiz preferences. Please try again.")
                return

            self.question_manager = QuestionManager(subject=subject_name)
            questions = self.fetch_questions(difficulty_level, db_key=db_key)
            if not questions:
                logging.error(f"No questions available for subject: {subject_name}, difficulty: {difficulty_level}")
                return

            correct_answers, answers = self.ask_questions(questions)

            quiz_id = self.create_quiz_entry(student_id, subject_name, difficulty_level, db_key=db_key)
            if not quiz_id:
                logging.error("Failed to create quiz entry, cannot log results.")
                return

            self.log_quiz_results(student_id, quiz_id, answers, correct_answers, db_key=db_key)
            logging.info(f"\nQuiz complete! Your score: {correct_answers}/{len(questions)}")

        except Exception as e:
            logging.error(f"An error occurred during the game: {e}")
        finally:
            from main import handle_student_menu
            handle_student_menu(student_id, db_key=db_key)

    def get_quiz_preferences(self, db_key='trivia_db'):
        subjects = self.get_available_subjects(db_key=db_key)
        if not subjects:
            logging.error("No subjects found.")
            return None, None

        subject_selection = self.get_user_selection("Choose a subject:",
                                                    {str(i + 1): s for i, s in enumerate(subjects)})
        if not subject_selection or not subject_selection.isdigit() or int(subject_selection) not in range(1,
                                                                                                           len(subjects) + 1):
            logging.error("Invalid subject selected.")
            return None, None

        subject_name = subjects[int(subject_selection) - 1]
        difficulty_level = self.get_user_selection("Choose a difficulty level:",
                                                   {'1': 'easy', '2': 'medium', '3': 'hard'})
        if difficulty_level not in {'1', '2', '3'}:
            logging.error("Invalid difficulty level selected.")
            return None, None

        return subject_name, {'1': 'easy', '2': 'medium', '3': 'hard'}[difficulty_level]

    @with_connection
    def get_available_subjects(self, connection, db_key='trivia_db'):
        query = "SELECT subject_name FROM subjects"
        try:
            subjects = fetch_all_query(connection, query)
            return [subject['subject_name'] for subject in subjects]
        except Exception as e:
            logging.error(f"Error fetching subjects: {e}")
            return []

    @with_connection
    def log_quiz_results(self, connection, student_id, quiz_id, answers, score, db_key='trivia_db'):
        logging.debug(f"Logging quiz results for student_id: {student_id}, quiz_id: {quiz_id}, score: {score}")

        # Queries for inserting into the quiz_results and scores tables
        quiz_results_query = """
              INSERT INTO quiz_results (student_id, quiz_id, answers, score)
              VALUES (%s, %s, %s, %s)
          """
        scores_query = """
              INSERT INTO scores (student_id, quiz_id, score)
              VALUES (%s, %s, %s)
          """

        try:
            with connection.cursor() as cursor:
                # Attempt to insert into the quiz_results table
                try:
                    cursor.execute(quiz_results_query, (student_id, quiz_id, ','.join(answers), score))
                    logging.info(f"Successfully logged quiz results for student {student_id}, quiz {quiz_id}")
                except Exception as e:
                    logging.error(f"Failed to insert into quiz_results: {e}")
                    raise  # Re-raise the exception to trigger rollback

                # Attempt to insert into the scores table
                try:
                    cursor.execute(scores_query, (student_id, quiz_id, score))
                    logging.info(f"Successfully logged score for student {student_id}, quiz {quiz_id}")
                except Exception as e:
                    logging.error(f"Failed to insert into scores: {e}")
                    raise  # Re-raise the exception to trigger rollback

                # If all inserts were successful, commit the transaction
                connection.commit()
                logging.info(f"Transaction committed successfully for student {student_id}, quiz {quiz_id}")

        except Exception as e:
            logging.error(f"Transaction failed: {e}")
            try:
                connection.rollback()
                logging.info("Transaction rolled back successfully.")
            except Exception as rollback_error:
                logging.critical(f"Failed to roll back transaction: {rollback_error}")
    
    @with_connection
    def create_quiz_entry(self, connection, student_id, subject_name, difficulty_level, db_key='trivia_db'):
        subject_id = self.get_subject_id(connection, subject_name, db_key=db_key)
        if not subject_id:
            logging.error(f"Subject ID not found for subject '{subject_name}'")
            return None

        quiz_name = f"{subject_name} Quiz"
        quiz_query = """
            INSERT INTO quizzes (teacher_id, quiz_name, subject_id, difficulty_level)
            VALUES (%s, %s, %s, %s)
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(quiz_query, (student_id, quiz_name, subject_id, difficulty_level))
                connection.commit()
                return cursor.lastrowid
        except Exception as e:
            logging.error(f"Error creating quiz entry: {e}")
            connection.rollback()
            return None

    def get_subject_id(self, connection, subject_name, db_key='trivia_db'):
        query = "SELECT subject_id FROM subjects WHERE subject_name = %s"
        try:
            result = fetch_one_query(connection, query, (subject_name,))
            if result:
                return result['subject_id']
            else:
                logging.error(f"No subject found with the name {subject_name}")
                return None
        except Exception as e:
            logging.error(f"Error fetching subject ID: {e}")
            return None

    def fetch_questions(self, difficulty_level, db_key='trivia_db'):
        return self.question_manager.get_questions_by_difficulty(difficulty_level, db_key=db_key)

    def ask_questions(self, questions):
        correct_answers = 0
        asked_questions = set()
        answers = []

        for i in range(min(10, len(questions))):
            question = random.choice([q for q in questions if q['question_text'] not in asked_questions])
            asked_questions.add(question['question_text'])

            print(f"\nQuestion {i + 1}: {question['question_text']}")
            options, correct_index = self.get_shuffled_options(question)
            self.display_answers(options)

            user_answer, time_taken = self.get_user_answer("Enter your answer (A, B, C, or D):", len(options))

            if user_answer is not None:
                user_letter = chr(65 + user_answer)
                print(f"Your answer is '{user_letter}'.")
                if user_answer == correct_index:
                    print("Correct answer, well done!")
                    correct_answers += 1
                else:
                    correct_letter = chr(65 + correct_index)
                    print(f"Nice try! The correct answer is '{correct_letter}'.")
                answers.append(f"Q{i + 1}: {user_letter}")
            else:
                correct_letter = chr(65 + correct_index)
                print(f"Time's up! The correct answer was '{correct_letter}'.")
                answers.append(f"Q{i + 1}: Timed out")

        return correct_answers, answers

    def get_shuffled_options(self, question):
        options = [question['option_a'], question['option_b'], question['option_c'], question['option_d']]
        correct_index = ord(question['correct_option'].upper()) - 65
        shuffled_options = options[:]
        random.shuffle(shuffled_options)
        correct_index = shuffled_options.index(options[correct_index])
        return shuffled_options, correct_index

    def display_answers(self, options):
        for i, option in enumerate(options):
            print(f"{chr(65 + i)}. {option}")

    def get_user_selection(self, prompt, options_dict):
        print(prompt)
        for key, value in options_dict.items():
            print(f"{key}. {value}")
        choice = input("Choose an option: ").strip()
        return choice if choice in options_dict else None

    def countdown_timer(self):
        for remaining in range(self.timeout_duration, 0, -1):
            if self.timer_expired or self.user_input_ready.is_set():
                break
            if remaining % 5 == 0:
                print(f"\rTime remaining: {remaining} seconds", end="")
            time.sleep(1)
        if not self.user_input_ready.is_set():
            print("\n\nTime's up!")
            self.timer_expired = True

    def get_user_answer(self, prompt, num_options):
        print(prompt)
        self.timer_expired = False
        self.user_input_ready.clear()
        self.user_input = None
        start_time = time.time()
        timer_thread = threading.Thread(target=self.countdown_timer)
        timer_thread.start()
        letter_to_index = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        while not self.timer_expired and self.user_input is None:
            try:
                user_input = input().strip().upper()
                if user_input in letter_to_index and letter_to_index[user_input] < num_options:
                    self.user_input = user_input
                    self.user_input_ready.set()
                else:
                    print("Invalid input. Enter A, B, C, or D.")
            except EOFError:
                break
        timer_thread.join()
        time_taken = time.time() - start_time
        return letter_to_index.get(self.user_input), time_taken

