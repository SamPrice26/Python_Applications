import mysql.connector
from mysql.connector import Error
from config import DATABASE_CONFIG

def create_connection(db_key):
    """Create and return a database connection using the given key."""
    db_config = DATABASE_CONFIG.get(db_key)
    if not db_config:
        print(f"Error: No configuration found for key '{db_key}'")
        return None
    try:
        connection = mysql.connector.connect(**db_config)
        return connection  # Return the connection if successful
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None  # Return None if connection fails

def with_connection(func):
    """A decorator that automatically manages the database connection."""
    def wrapper(*args, **kwargs):
        # Extract `self` if present (for methods within classes)
        if len(args) > 0 and hasattr(args[0], '__dict__'):
            self = args[0]
            args = args[1:]
        else:
            self = None

        # Get the database key from the arguments
        db_key = kwargs.pop('db_key', None)
        if not db_key:
            print("No database key provided.")
            return None

        # Create a connection using the provided key
        connection = create_connection(db_key)
        if not connection:
            print("Failed to create a database connection.")
            return None

        try:
            if self:
                return func(self, connection, *args, **kwargs)  # Handle methods
            else:
                return func(connection, *args, **kwargs)  # Handle plain functions
        finally:
            connection.close()  # Always close the connection
            print("Connection closed.")

    return wrapper

def execute_query(connection, query, params=None):
    """Run an SQL command (like INSERT or UPDATE)."""
    with connection.cursor() as cursor:
        try:
            cursor.execute(query, params or ())
            connection.commit()  # Save the changes
            return cursor.lastrowid  # Return the ID of the new row
        except Error as e:
            print(f"Error executing query: {e}")
            connection.rollback()  # Undo changes if there's an error
            return None

def fetch_all_query(connection, query, params=None):
    """Run a SELECT command and return all matching rows."""
    with connection.cursor(dictionary=True) as cursor:
        try:
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            return results  # Get all results
        except Error as e:
            print(f"Error fetching data: {e}")
            return None

def fetch_one_query(connection, query, params=None):
    """Run a SELECT command and return the first matching row."""
    with connection.cursor(dictionary=True) as cursor:
        try:
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            cursor.fetchall()
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            return None

            cursor.fetchall()
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            return None
