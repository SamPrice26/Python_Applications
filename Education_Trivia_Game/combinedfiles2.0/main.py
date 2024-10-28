import getpass
import hashlib
import logging
from utils import execute_query, fetch_one_query, fetch_all_query, with_connection, create_connection
from user import User, Student, Teacher, Parent
from game import EducationTriviaGame


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

current_user = None  # Global variable to store the current user


def add_separator1():
    # Add a decorative separator to the output
    print('\n-----------------------------------------------------')
    print('▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️\n')


def add_separator2():
    # Add a decorative separator to the output
    print('\n▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️')
    print('-----------------------------------------------------')


def hash_password(password):
    # Hash the password using SHA-256 for security
    return hashlib.sha256(password.encode()).hexdigest()


def hash_password(password):
    # Hash the password using SHA-256 for security
    return hashlib.sha256(password.encode()).hexdigest()

@with_connection
def create_user_in_db(connection, user):
    try:
        if isinstance(user, Teacher):
            query = """
            INSERT INTO teachers (username, email, password, subject)
            VALUES (%s, %s, %s, %s)
            """
            execute_query(connection, query, (user.username, user.email, user.password, ','.join(user.subjects)))
        elif isinstance(user, Student):
            query = """
            INSERT INTO students (username, email, password)
            VALUES (%s, %s, %s)
            """
            execute_query(connection, query, (user.username, user.email, user.password))
        elif isinstance(user, Parent):
            query = """
            INSERT INTO parents (username, email, password, pupils)
            VALUES (%s, %s, %s, %s)
            """
            execute_query(connection, query, (user.username, user.email, user.password, ','.join(user.pupils)))

        connection.commit()
        logging.info(f"User {user.username} of type {type(user).__name__} created successfully.")
        return True  # Indicate success

    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        connection.rollback()  # Explicitly rollback in case of error
        return False  # Indicate failure

    except Exception as e:
        logging.error(f"Error creating user in database: {str(e)}")
        connection.rollback()
        raise

# Function to get the user ID based on username and user_type
@with_connection
def get_user_id(connection, username, user_type):
    """Retrieve the user ID from the appropriate table based on user_type."""
    if user_type == 'teacher':
        query = "SELECT id FROM teachers WHERE username = %s"
    elif user_type == 'student':
        query = "SELECT id FROM students WHERE username = %s"
    elif user_type == 'parent':
        query = "SELECT id FROM parents WHERE username = %s"
    else:
        return None

    result = fetch_one_query(connection, query, (username,))
    return result['id'] if result else None

# Function to handle new user registration
def handle_new_user():
    global current_user
    user_type = input("Are you a student, teacher, or parent? Enter your user type here: ").strip().lower()

    if user_type not in ["student", "teacher", "parent"]:
        print("Invalid user type entered. Please choose either 'student', 'teacher', or 'parent'.")
        return

    username = input("Brilliant! Let's start by choosing your username: ")

    # Check if the username already exists
    existing_user_id = get_user_id(username=username, user_type=user_type, db_key='user_db')
    if existing_user_id:
        print(f"The username '{username}' is already taken. Please choose a different username.")
        return

    email_address = input("Enter your email address here: ")
    password = getpass.getpass("You're almost there! Now choose a password: ")
    hashed_password = hash_password(password)

    if user_type == "teacher":
        subject = input("Please enter your subject: ")
        current_user = Teacher(username, email_address, hashed_password, [subject])
    elif user_type == "student":
        current_user = Student(username, email_address, hashed_password, mark=0)
    elif user_type == "parent":
        pupils = input(
            "Please enter the username(s) of your pupil(s). If multiple, please enter the usernames separated by a comma and a space: ").split(
            ", ")
        current_user = Parent(username, email_address, hashed_password, pupils)

    try:
        create_user_in_db(current_user, db_key='user_db')
        add_separator1()
        print(f'Welcome to Educational Trivia, {username}!')
        add_separator2()

        # Log and confirm successful account creation
        logging.info(f"User {username} of type {user_type.capitalize()} created successfully.")
        print(f"Account for {user_type.capitalize()} '{username}' created successfully!")

        # Retrieve the newly created user ID
        user_id = get_user_id(username=username, user_type=user_type, db_key='user_db')
        if not user_id:
            raise Exception(f"Failed to retrieve {user_type} ID after creation.")

        # Proceed to user menu for specific user
        if user_type == 'teacher':
            handle_teacher_menu(user_id)  # Pass teacher_id to the menu
        elif user_type == 'student':
            handle_student_menu(user_id)
        elif user_type == 'parent':
            handle_parent_menu(user_id)

    except Exception as e:
        logging.error(f"Error during user registration: {e}")
        print("An error occurred during registration. Please try again.")
        current_user = None

@with_connection
def load_user_from_database(connection, username, db_key='user_db'):
    """
    Fetch user data from the database using the username. It also determines whether the user is a teacher, student, or parent.
    """

    # Query to find out if the user is a teacher, student, or parent
    detect_user_type_query = """
    SELECT 'teacher' as user_type, id FROM teachers WHERE username = %s
    UNION ALL
    SELECT 'student' as user_type, id FROM students WHERE username = %s
    UNION ALL
    SELECT 'parent' as user_type, id FROM parents WHERE username = %s
    LIMIT 1;
    """

    try:
        # Run the query to find the user type and ID
        user_type_result = fetch_one_query(connection, detect_user_type_query, (username, username, username))
        if not user_type_result:
            # If no user is found, return None
            logging.error(f"No user found with username: {username}")
            return None, None, None

        # Get the user type and ID from the result
        user_type = user_type_result['user_type']
        user_id = user_type_result['id']
        logging.debug(f"User type detected for {username}: {user_type} with ID: {user_id}")

        # Fetch full user details based on their type
        if user_type == "teacher":
            query = "SELECT * FROM teachers WHERE username = %s"
        elif user_type == "student":
            query = "SELECT * FROM students WHERE username = %s"
        elif user_type == "parent":
            query = "SELECT * FROM parents WHERE username = %s"
        else:
            return None, None, None

        user_data = fetch_one_query(connection, query, (username,))
    except Exception as e:
        logging.error(f"Error loading user from database: {e}")
        return None, None, None

    # Return the user object, their ID, and type
    if user_data:
        if user_type == "teacher":
            return Teacher(user_data['username'], user_data['email'], user_data['password'], [user_data['subject']]), user_id, user_type
        elif user_type == "student":
            return Student(user_data['username'], user_data['email'], user_data['password'], mark=0), user_id, user_type
        elif user_type == "parent":
            return Parent(user_data['username'], user_data['email'], user_data['password'], user_data['pupils'].split(',')), user_id, user_type

    return None, None, None


def handle_existing_user():
    """
    Handle login for an existing user and load their menu.
    """
    global current_user
    username = input("Enter your username here: ")
    password = getpass.getpass("Enter your password here: ")
    hashed_password = hash_password(password)

    print(f"DEBUG: Username entered: {username}")
    print(f"DEBUG: Password entered: {password}")
    print(f"DEBUG: Hashed password: {hashed_password}")

    try:
        # Load the user from the database
        current_user, user_id, user_type = load_user_from_database(username=username, db_key='user_db')

        print(f"DEBUG: Load user result - current_user: {current_user}, user_id: {user_id}, user_type: {user_type}")
    except Exception as e:
        logging.error(f"Error loading user: {e}")
        print("An error occurred while loading the user. Please try again later.")
        return

    if current_user:
        print(f"DEBUG: Password comparison: stored = {current_user.password}, entered = {hashed_password}")
        if current_user.password == hashed_password:
            add_separator1()
            print(f"Welcome back, {username}!")
            add_separator2()

            # Show the correct menu based on user type
            if user_type == 'teacher':
                handle_teacher_menu(user_id)
            elif user_type == 'student':
                handle_student_menu(user_id)
            elif user_type == 'parent':
                handle_parent_menu(user_id)
        else:
            print("Invalid username or password. Please try again.")
            current_user = None
    else:
        print("User not found. Please check your username and user type.")

# User menus handling options for user
def handle_student_menu(student_id, db_key='trivia_db'):
    logging.info(f"Displaying menu for student: {current_user.username}")
    print('1. Start new quiz')
    print('2. Check your current score')
    user_choice = input("Enter the number corresponding to your choice: ").strip()

    if user_choice == '1':
        start_new_quiz(student_id, db_key=db_key)
    elif user_choice == '2':
        check_student_score(student_id, db_key=db_key)
    else:
        logging.warning(f"Invalid choice for student: {user_choice}")
        print("Invalid choice.")
        # Always pass student_id when calling handle_student_menu again
        handle_student_menu(student_id)

def handle_teacher_menu(teacher_id):
    logging.info(f"Displaying menu for teacher: {current_user.username}")
    print('1. Create new quiz')
    print('2. Update an existing quiz')
    print('3. Check student score')
    print('4. Log out')
    user_choice = input("Enter the number corresponding to your choice: ").strip()

    if user_choice == '1':
        create_new_quiz(teacher_id)
    elif user_choice == '2':
        update_quiz(teacher_id)
    elif user_choice == '3':
        check_student_scores(teacher_id)
    elif user_choice == '4':
        logout()
    else:
        logging.warning(f"Invalid choice for teacher: {user_choice}")
        print("Invalid choice.")


def handle_parent_menu(parent_id):
    logging.info(f"Displaying menu for parent: {current_user.username}")
    print('1. Check your pupil(s)\'s score')
    user_choice = input("Enter the number corresponding to your choice: ").strip()

    if user_choice == '1':
        check_pupil_scores(parent_id)
    else:
        logging.warning(f"Invalid choice for parent: {user_choice}")
        print("Invalid choice.")

# Student menu handling options, checking scores, playing quiz

def start_new_quiz(student_id, db_key='trivia_db'):
    """Start a new quiz for the student."""
    game = EducationTriviaGame(current_user)
    game.play_game(student_id, db_key=db_key)


@with_connection
def check_student_score(connection, student_id, db_key='trivia_db'):
    """Check the current score of the student."""

    # Validate student_id
    if not isinstance(student_id, int) or student_id <= 0:
        logging.error(f"Invalid student_id: {student_id}. Must be a positive integer.")
        print("Error: Invalid student ID.")
        return

    query = """
    SELECT q.quiz_name, s.score, s.taken_at
    FROM scores s
    JOIN quizzes q ON s.quiz_id = q.quiz_id
    WHERE s.student_id = %s
    ORDER BY s.taken_at DESC
    """

    try:
        results = fetch_all_query(connection, query, (student_id,))

        if results:
            print("\nYour quiz scores:")
            for result in results:
                print(f"Quiz: {result['quiz_name']}, Score: {result['score']}, Date: {result['taken_at']}")
        else:
            print("No scores available.")

    except Exception as e:
        logging.error(f"Failed to retrieve scores for student_id: {student_id}. Error: {e}")
        print("An error occurred while retrieving your scores. Please try again later.")

    finally:
        # Return to the student menu
        handle_student_menu(student_id, db_key=db_key)



def logout():
    global current_user

    if current_user:
        logging.info(f"User {current_user.username} logged out.")
        print(f"Goodbye, {current_user.username}! You have been logged out successfully.")
        current_user = None  # Clear the current user

    # Optionally return to the main menu or exit
    # main_menu()

    # to exit the program
    # exit()

# Teacher options, quiz related handling

@with_connection
def insert_quiz(connection, teacher_id, quiz_name, subject, difficulty_level, db_key='trivia_db'):
    """Insert a new quiz into the trivia_questions database."""
    query = """
    INSERT INTO quizzes (teacher_id, quiz_name, subject_id, difficulty_level)
    VALUES (%s, %s, (SELECT subject_id FROM subjects WHERE subject_name = %s), %s)
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (teacher_id, quiz_name, subject, difficulty_level))
            connection.commit()
            return cursor.lastrowid  # Return the ID of the inserted quiz
    except Exception as e:
        logging.error(f"Error creating quiz: {e}")
        connection.rollback()
        raise

@with_connection
def add_question_to_quiz(connection, quiz_id, teacher_id, difficulty_level, db_key='trivia_db'):
    """Add a new question to the quiz."""
    question_text = input("Enter the question text: ")
    option_a = input("Enter option A: ")
    option_b = input("Enter option B: ")
    option_c = input("Enter option C: ")
    option_d = input("Enter option D: ")
    correct_option = input("Enter the correct option (A/B/C/D): ").upper()

    if correct_option not in ['A', 'B', 'C', 'D']:
        print("Invalid option. Please enter A, B, C, or D.")
        return

    query = """
    INSERT INTO custom_questions (teacher_id, question_text, option_a, option_b, option_c, option_d, correct_option, difficulty_level)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (
                teacher_id, question_text, option_a, option_b, option_c, option_d, correct_option, difficulty_level))
            question_id = cursor.lastrowid

            # Map the question to the quiz
            map_query = """
            INSERT INTO quiz_questions (quiz_id, question_id, question_source)
            VALUES (%s, %s, 'custom')
            """
            cursor.execute(map_query, (quiz_id, question_id))
            connection.commit()
            print("Question added to the quiz successfully!")
    except Exception as e:
        logging.error(f"Error adding question to quiz: {e}")
        connection.rollback()
        print("Failed to add question to the quiz.")

def create_new_quiz(teacher_id, db_key='trivia_db'):
    quiz_name = input("Enter the name for your quiz: ")
    subject = current_user.subjects[0]  # Assuming current_user.subjects is a list with at least one subject
    difficulty = input("Enter the difficulty level for this quiz (easy/medium/hard): ").lower()

    if difficulty not in ["easy", "medium", "hard"]:
        print("Invalid difficulty level. Please choose 'easy', 'medium', or 'hard'.")
        return

    try:
        # Insert the quiz into trivia_questions using the teacher_id
        quiz_id = insert_quiz(teacher_id, quiz_name, subject, difficulty_level, db_key=db_key)

        if quiz_id:
            print(f"Quiz '{quiz_name}' created successfully! Now, let's add some questions.")
            for i in range(10):
                print(f"\nAdding question {i + 1}/10:")
                add_question_to_quiz(quiz_id, teacher_id, difficulty_level, db_key=db_key)
            print(f"\nQuiz '{quiz_name}' created with 10 questions.")
        else:
            print("Failed to create quiz.")
    except Exception as e:
        logging.error(f"Error creating quiz: {e}")
        print("Failed to create quiz due to an error.")

def update_quiz(teacher_id, db_key='trivia_db'):
    quizzes = fetch_quizzes(teacher_id, db_key=db_key)

    if not quizzes:
        print("You have no existing quizzes to update.")
        return

    print("Existing quizzes:")
    for i, quiz in enumerate(quizzes, 1):
        print(f"{i}. {quiz['quiz_name']}")

    try:
        choice = int(input("Select the quiz number you want to update: "))
        if choice < 1 or choice > len(quizzes):
            print("Invalid choice. Please select a valid quiz number.")
            return
        selected_quiz_id = quizzes[choice - 1]['quiz_id']
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    print(f"\nWhat would you like to do with the quiz '{quizzes[choice - 1]['quiz_name']}'?")
    print("1. Update questions in quiz")
    print("2. Delete quiz")

    try:
        sub_choice = int(input("Enter the number corresponding to your choice: "))
        if sub_choice not in [1, 2]:
            raise ValueError("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    if sub_choice == 1:
        update_quiz_questions(selected_quiz_id, quizzes[choice - 1]['quiz_name'], teacher_id, db_key=db_key)
    elif sub_choice == 2:
        delete_quiz(selected_quiz_id, db_key=db_key)

@with_connection
def fetch_quizzes(connection, teacher_id, db_key='trivia_db'):
    """Fetch quizzes associated with the teacher."""
    query = """
    SELECT quiz_id, quiz_name FROM quizzes WHERE teacher_id = %s
    """
    return fetch_all_query(connection, query, (teacher_id,))

@with_connection
def fetch_quiz_questions(connection, quiz_id, db_key='trivia_db'):
    """Fetch questions for the selected quiz."""
    query = """
    SELECT cq.question_id, cq.question_text, cq.option_a, cq.option_b, cq.option_c, cq.option_d, cq.correct_option
    FROM quiz_questions qq
    JOIN custom_questions cq ON qq.question_id = cq.question_id
    WHERE qq.quiz_id = %s
    """
    return fetch_all_query(connection, query, (quiz_id,))

def update_quiz_questions(quiz_id, quiz_name, teacher_id, db_key='trivia_db'):
    questions = fetch_quiz_questions(quiz_id, db_key=db_key)

    if not questions:
        print(f"No questions found for quiz '{quiz_name}'.")
        return

    print(f"\nQuiz '{quiz_name}' Questions:")
    for i, question in enumerate(questions, 1):
        print(f"{i}. {question['question_text']}")
        print(f"   A: {question['option_a']}")
        print(f"   B: {question['option_b']}")
        print(f"   C: {question['option_c']}")
        print(f"   D: {question['option_d']}")
        print(f"   Correct Option: {question['correct_option']}\n")

    try:
        question_choice = int(input(
            "Enter the question number you want to update, or enter a number greater than the existing number to add a new question: "))
        if question_choice > len(questions):
            print("Adding a new question to the quiz...")
            add_question_to_quiz(quiz_id, teacher_id, current_user.subjects[0], db_key=db_key)
        else:
            print("Updating an existing question... (this feature can be added)")
            # Logic for updating an existing question can be added here.
    except ValueError:
        print("Invalid input. Please enter a number.")

@with_connection
def delete_quiz(connection, quiz_id, db_key='trivia_db'):
    """Delete the selected quiz from the database."""
    query = "DELETE FROM quizzes WHERE quiz_id = %s"
    execute_query(connection, query, (quiz_id,))
    print("Quiz deleted successfully.")




def run():
    # Main function to start the application
    try:
        global current_user
        add_separator1()
        logging.info("Starting the Educational Trivia Game")
        print("Hi there! Welcome to the Educational Trivia Game!")
        add_separator2()
        input("Please press enter to start:")
        existing_user = input("Do you have an existing account? Enter y/n: ").strip().lower()

        if existing_user == "y":
            handle_existing_user()
        elif existing_user == "n":
            handle_new_user()
        else:
            logging.warning("Invalid input received for existing account query")
            print("Invalid input, please re-run the game and start again!")
            return

        if current_user is None:
            logging.warning("No valid user logged in")
            print("No valid user logged in.")
            return

        print("Let's start, shall we? 🤓")
        add_separator1()

        if isinstance(current_user, Student):
            handle_student_menu()
        elif isinstance(current_user, Teacher):
            handle_teacher_menu(teacher_id)
        elif isinstance(current_user, Parent):
            handle_parent_menu()
        else:
            logging.error(f"Unknown user type: {type(current_user)}")
            print("Unknown user type.")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise  # Re-raise the exception for debugging


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        logging.critical(f"Critical error: {str(e)}")

