from typing import List
from utils import execute_query, fetch_all_query, with_connection

class User:
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password

    def __str__(self):
        return f"Username: {self.username}, Email: {self.email}"


class Student(User):
    def __init__(self, username: str, email: str, password: str, mark: int = 0):
        super().__init__(username, email, password)
        self.mark = mark
        self.scores = []

    def add_score(self, score: int):
        self.scores.append(score)
        self.update_score_in_db(score)

    def get_average_score(self) -> float:
        if not self.scores:
            return 0.0
        return sum(self.scores) / len(self.scores)

    @with_connection
    def update_score_in_db(self, connection, score: int, db_key='trivia_db'):
        # Retrieve student_id from the user_db before inserting the score in the trivia_db
        student_id = self.get_student_id_from_user_db()
        if not student_id:
            raise ValueError("Student ID not found for the user.")

        query = """
        INSERT INTO scores (student_id, quiz_id, score)
        VALUES (%s, %s, %s)
        """
        execute_query(connection, query, (student_id, None, score))

    @with_connection
    def get_student_id_from_user_db(self, connection, db_key='user_db'):
        # Retrieve the student's ID from the user database
        query = "SELECT id FROM students WHERE username = %s"
        result = fetch_all_query(connection, query, (self.username,))
        return result[0]['id'] if result else None


class Teacher(User):
    def __init__(self, username: str, email: str, password: str, subjects: List[str]):
        super().__init__(username, email, password)
        self.subjects = subjects

    def assign_mark(self, student: Student, score: int):
        student.add_score(score)


class Parent(User):
    def __init__(self, username: str, email: str, password: str, pupils: List[str]):
        super().__init__(username, email, password)
        self.pupils = pupils

    def get_pupils_scores(self):
        return {pupil: self.load_student_scores(pupil) for pupil in self.pupils}

    @staticmethod
    @with_connection
    def load_student_scores(connection, pupil_username: str, db_key='trivia_db'):
        query = """
        SELECT score FROM scores
        JOIN students ON scores.student_id = students.id
        WHERE students.username = %s
        """
        return [score['score'] for score in fetch_all_query(connection, query, (pupil_username,))]
