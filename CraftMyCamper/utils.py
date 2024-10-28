import mysql.connector
from mysql.connector import Error
from config import config

# Function to establish MySQL connection
def get_mysql_connection():
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Function to fetch all projects from the database
def get_projects():
    query = "SELECT * FROM projects"
    connection = get_mysql_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            projects = cursor.fetchall()
            return projects
        except Error as e:
            print(f"Error fetching projects: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            connection.close()
    return []

# Function to add a new project to the database
def add_project(project_name, description, budget):
    query = "INSERT INTO projects (project_name, description, budget, start_date) VALUES (%s, %s, %s, CURDATE())"
    connection = get_mysql_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query, (project_name, description, budget))
            connection.commit()
            print("Project added successfully!")
        except Error as e:
            print(f"Error adding project: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            connection.close()

# Function to fetch all resources from the database
def get_resources():
    query = """
        SELECT r.*, c.name AS category_name
        FROM resources r
        JOIN categories c ON r.category_id = c.id
    """
    connection = get_mysql_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            resources = cursor.fetchall()
            for resource in resources:  # Print fetched resources for debugging
                print(resource)
            return resources
        except Error as e:
            print(f"Error fetching resources: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            connection.close()
    return []

# Function to fetch all categories from the database
def get_categories():
    query = "SELECT * FROM categories"
    connection = get_mysql_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            categories = cursor.fetchall()
            return categories
        except Error as e:
            print(f"Error fetching categories: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            connection.close()
    return []

# Function to add a new resource to the database
def add_resource(name, category_id, description, price, quantity, weight_kg=None, project_id=None):
    connection = get_mysql_connection()
    if connection:
        try:
            cursor = connection.cursor()
            resource_query = "INSERT INTO resources (name, category_id, description, price, quantity, weight_kg) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(resource_query, (name, category_id, description, price, quantity, weight_kg))
            resource_id = cursor.lastrowid
            connection.commit()

            if project_id:
                project_resource_query = "INSERT INTO project_resources (project_id, resource_id) VALUES (%s, %s)"
                cursor.execute(project_resource_query, (project_id, resource_id))
                connection.commit()

            print("Resource added successfully!")
        except Error as e:
            print(f"Error adding resource: {e}")
            print(f"Resource Query: {resource_query}")
            print(f"Resource Values: {(name, category_id, description, price, quantity, weight_kg)}")
            if project_id:
                print(f"Project Resource Query: {project_resource_query}")
                print(f"Project Resource Values: {(project_id, resource_id)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            connection.close()

# Function to link an existing resource to a project
def add_project_resource(project_id, resource_id):
    connection = get_mysql_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO project_resources (project_id, resource_id) VALUES (%s, %s)"
            cursor.execute(query, (project_id, resource_id))
            connection.commit()
            print("Resource linked to project successfully!")
        except Error as e:
            print(f"Error linking resource to project: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            connection.close()

# Function to remove a resource from a project
def remove_project_resource(project_id, resource_id):
    connection = get_mysql_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM project_resources WHERE project_id = %s AND resource_id = %s"
            cursor.execute(query, (project_id, resource_id))
            connection.commit()
            print("Resource removed from project successfully!")
        except Error as e:
            print(f"Error removing resource from project: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            connection.close()

# Function to fetch resources linked to a specific project
def get_project_resources(project_id):
    query = """
        SELECT r.*, c.name AS category_name
        FROM resources r
        JOIN project_resources pr ON r.resource_id = pr.resource_id
        JOIN categories c ON r.category_id = c.id
        WHERE pr.project_id = %s
    """
    connection = get_mysql_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (project_id,))
            resources = cursor.fetchall()
            return resources
        except Error as e:
            print(f"Error fetching project resources: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            connection.close()
    return []

# Function to calculate the remaining budget for a project
def calculate_remaining_budget(project_id):
    resources_query = """
        SELECT SUM(r.price * r.quantity) AS total_cost
        FROM resources r
        JOIN project_resources pr ON r.resource_id = pr.resource_id
        WHERE pr.project_id = %s
    """
    project_query = "SELECT budget FROM projects WHERE project_id = %s"
    connection = get_mysql_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(project_query, (project_id,))
            project = cursor.fetchone()
            if not project:
                return None # Project not found

            project_budget = float(project['budget']) if project else 0
            cursor.execute(resources_query, (project_id,))
            result = cursor.fetchone()
            total_cost = float(result['total_cost']) if result['total_cost'] else 0
            remaining_budget = project_budget - total_cost
            return remaining_budget
        except Error as e:
            print(f"Error calculating remaining budget: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            connection.close()
    return None
