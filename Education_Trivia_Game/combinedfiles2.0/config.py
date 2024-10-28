#API Configuration
API_PORT = 5001
API_URL = f"http://localhost:{API_PORT}/api"

#Database configuration to use database
DATABASE_CONFIG = {
    'user_db': {
        'host': 'localhost',
        'user': 'root',  # Replace with your MySQL username
        'password': 'LadyMandrake96',  # Replace with your MySQL password
        'database': 'user_database'
    },
   'trivia_db': {
        'host': 'localhost',
        'user': 'root',
        'password': 'LadyMandrake96',
        'database':  'trivia_questions'
    }
}
