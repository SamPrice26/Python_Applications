from utils import execute_query, fetch_all_query, with_connection

class QuestionManager:
    def __init__(self, subject):
        # Initialize the QuestionManager with a subject name
        self.subject = subject

    @with_connection
    def add_question(self, connection, question_data, db_key='trivia_db'):
        """Add a new question to the database."""
        add_question_query = """
        INSERT INTO questions 
        (subject_id, difficulty_level, question_text, option_a, option_b, option_c, option_d, correct_option)
        VALUES ((SELECT subject_id FROM subjects WHERE subject_name = %s), %s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(connection, add_question_query, (
            self.subject,
            question_data['difficulty_level'],
            question_data['question_text'],
            question_data['option_a'],
            question_data['option_b'],
            question_data['option_c'],
            question_data['option_d'],
            question_data['correct_option']
        ))

    @with_connection
    def get_filtered_questions(self, connection, difficulty_level=None, db_key='trivia_db'):
        """Retrieve questions filtered by subject and difficulty level."""
        query = "SELECT * FROM questions WHERE subject_id = (SELECT subject_id FROM subjects WHERE subject_name = %s)"
        params = [self.subject]

        if difficulty_level:
            query += " AND difficulty_level = %s"
            params.append(difficulty_level)

        return fetch_all_query(connection, query, tuple(params))

    @with_connection
    def update_question(self, connection, question_id, question_data, db_key='trivia_db'):
        """Update an existing question in the database."""
        update_question_query = """
        UPDATE questions
        SET question_text = %s, option_a = %s, option_b = %s, option_c = %s, 
            option_d = %s, correct_option = %s, difficulty_level = %s
        WHERE question_id = %s
        """
        execute_query(connection, update_question_query, (
            question_data['question_text'],
            question_data['option_a'],
            question_data['option_b'],
            question_data['option_c'],
            question_data['option_d'],
            question_data['correct_option'],
            question_data['difficulty_level'],
            question_id
        ))

    @with_connection
    def get_available_subjects(self, connection):
        """Retrieve all available subjects from the database."""
        query = "SELECT subject_name FROM subjects"
        subjects = fetch_all_query(connection, query)
        return [subject['subject_name'] for subject in subjects]

    @with_connection
    def get_questions_by_difficulty(self, connection, difficulty_level):
        """Retrieve questions filtered by subject and difficulty level."""
        query = """
        SELECT question_text, option_a, option_b, option_c, option_d, correct_option
        FROM questions
        WHERE subject_id = (SELECT subject_id FROM subjects WHERE subject_name = %s)
        AND difficulty_level = %s
        """
        params = (self.subject, difficulty_level)
        return fetch_all_query(connection, query, params)

    @with_connection
    def delete_question(self, connection, question_id):
        """Delete a question from the database based on its ID."""
        execute_query(connection, "DELETE FROM questions WHERE question_id = %s", (question_id,))
