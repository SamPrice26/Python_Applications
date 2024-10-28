from flask import Flask, jsonify, request
from utils import create_connection, execute_query, fetch_all_query, fetch_one_query
from config import API_PORT, DATABASE_CONFIG

app = Flask(__name__)

# User Management (Connecting to the user database)

@app.route('/api/login', methods=['POST'])
def login():
    # Handle user login
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Connect to the user database
    connection = create_connection('user_db')
    query = "SELECT id, username, user_type FROM users WHERE username = %s AND password = %s"
    user = fetch_one_query(connection, query, (username, password))
    connection.close()

    if user:
        return jsonify({"message": "Login successful", "user": user}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/register', methods=['POST'])
def register():
    # Handle user registration
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type')

    # Connect to the user database
    connection = create_connection('user_db')
    query = "INSERT INTO users (username, email, password, user_type) VALUES (%s, %s, %s, %s)"
    result = execute_query(connection, query, (username, email, password, user_type))
    connection.close()

    if result:
        return jsonify({"message": "User registered successfully"}), 201
    else:
        return jsonify({"error": "Registration failed"}), 500

# Subject and Question Management (Connecting to the trivia_questions database)

@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    # Retrieve available subjects
    connection = create_connection('trivia_db')
    if not connection:
        return jsonify({"error": "Failed to connect to the database"}), 500

    query = "SELECT subject_id, subject_name FROM subjects"
    subjects = fetch_all_query(connection, query)
    connection.close()
    return jsonify({"subjects": subjects})

@app.route('/api/questions', methods=['GET'])
def get_questions():
    # Retrieve questions based on subject and difficulty
    subject_id = request.args.get('subject_id')
    difficulty = request.args.get('difficulty')

    connection = create_connection('trivia_db')
    if not connection:
        return jsonify({"error": "Failed to connect to the database"}), 500

    query = """
    SELECT question_id, question_text, option_a, option_b, option_c, option_d, correct_option
    FROM questions
    WHERE subject_id = %s AND difficulty_level = %s
    """
    questions = fetch_all_query(connection, query, (subject_id, difficulty))
    connection.close()
    return jsonify({"questions": questions})

# Quiz Management (Connecting to the trivia_questions database)

@app.route('/api/quiz', methods=['POST'])
def create_quiz():
    # Create a new quiz
    data = request.json
    teacher_id = data.get('teacher_id')
    quiz_name = data.get('quiz_name')
    subject_id = data.get('subject_id')
    difficulty = data.get('difficulty')

    connection = create_connection('trivia_db')
    if not connection:
        return jsonify({"error": "Failed to connect to the database"}), 500

    query = """
    INSERT INTO quizzes (teacher_id, quiz_name, subject_id, difficulty_level)
    VALUES (%s, %s, %s, %s)
    """
    quiz_id = execute_query(connection, query, (teacher_id, quiz_name, subject_id, difficulty))
    connection.close()

    if quiz_id:
        return jsonify({"message": "Quiz created successfully", "quiz_id": quiz_id})
    else:
        return jsonify({"error": "Failed to create quiz"}), 500

@app.route('/api/teacher/<int:teacher_id>/quizzes', methods=['GET'])
def get_teacher_quizzes(teacher_id):
    # Get all quizzes created by a specific teacher
    connection = create_connection('trivia_db')
    if not connection:
        return jsonify({"error": "Failed to connect to the database"}), 500

    query = "SELECT quiz_id, quiz_name, subject_id, created_at FROM quizzes WHERE teacher_id = %s"
    quizzes = fetch_all_query(connection, query, (teacher_id,))
    connection.close()

    return jsonify({"quizzes": quizzes})

# Score Management (Cross-database interaction)

@app.route('/api/scores', methods=['POST'])
def save_score():
    # Save a student's score for a quiz
    data = request.json
    username = data.get('username')
    quiz_id = data.get('quiz_id')
    score = data.get('score')

    # Get student ID from user database
    user_connection = create_connection('user_db')
    student_query = "SELECT id FROM users WHERE username = %s AND user_type = 'student'"
    student_id = fetch_one_query(user_connection, student_query, (username,))
    user_connection.close()

    if not student_id:
        return jsonify({"error": "Student not found"}), 404

    # Save score in trivia_questions database
    trivia_connection = create_connection('trivia_db')
    score_query = """
    INSERT INTO scores (student_id, quiz_id, score)
    VALUES (%s, %s, %s)
    """
    result = execute_query(trivia_connection, score_query, (student_id['id'], quiz_id, score))
    trivia_connection.close()

    if result:
        return jsonify({"message": "Score saved successfully"}), 201
    else:
        return jsonify({"error": "Failed to save score"}), 500

# Retrieve Quiz Results by Subject for Students, Teachers, and Parents

@app.route('/api/results/<int:user_id>', methods=['GET'])
def get_quiz_results(user_id):
    # Get quiz results based on user type (student, teacher, or parent)
    connection = create_connection('user_db')
    user_query = "SELECT user_type FROM users WHERE id = %s"
    user_type = fetch_one_query(connection, user_query, (user_id,))
    connection.close()

    if not user_type:
        return jsonify({"error": "User not found"}), 404

    connection = create_connection('trivia_db')
    if user_type['user_type'] == 'student':
        # Get quiz results for a student
        query = """
        SELECT q.quiz_name, s.score, s.taken_at
        FROM scores s
        JOIN quizzes q ON s.quiz_id = q.quiz_id
        WHERE s.student_id = %s
        ORDER BY s.taken_at DESC
        """
        results = fetch_all_query(connection, query, (user_id,))
    elif user_type['user_type'] == 'teacher':
        # Get quiz results for a teacher's students
        query = """
        SELECT u.username as student_name, q.quiz_name, s.score, s.taken_at
        FROM scores s
        JOIN quizzes q ON s.quiz_id = q.quiz_id
        JOIN users u ON s.student_id = u.id
        WHERE q.teacher_id = %s
        ORDER BY s.taken_at DESC
        """
        results = fetch_all_query(connection, query, (user_id,))
    elif user_type['user_type'] == 'parent':
        # Get quiz results for a parent's children
        query = """
        SELECT u.username as student_name, q.quiz_name, s.score, s.taken_at
        FROM scores s
        JOIN quizzes q ON s.quiz_id = q.quiz_id
        JOIN users u ON s.student_id = u.id
        JOIN users p ON p.pupils LIKE CONCAT('%', u.username, '%')
        WHERE p.id = %s
        ORDER BY s.taken_at DESC
        """
        results = fetch_all_query(connection, query, (user_id,))
    else:
        return jsonify({"error": "Invalid user type"}), 400

    connection.close()
    return jsonify({"results": results})

if __name__ == '__main__':
    # Start the Flask application
    app.run(port=API_PORT, debug=True)
