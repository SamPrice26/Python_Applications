# CraftMyCamper API

## Introduction

This project is a Flask API for managing campervan conversion projects. It allows you to create projects, add resources, link resources to projects, and manage budgets.

## Installation Requirements

### Prerequisites

- Python 3.x
- MySQL

### Step-by-Step Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/CraftMyCamper.git
   cd CraftMyCamper

2. **Set Up Virtual Enviroment**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt

4. **Configure MySQL Database** 
   ```sh
   config = { # Replace with your database credentials
    'user': 'yourusername',
    'password': 'yourpassword', 
    'host': 'localhost',
    'database': 'CraftMyCamperdb',
    'raise_on_warnings': True 
   }

5. **Initialise the Database** 
   ```sh #run the SQL script to set up database schema
   mysql -u yourusername -p CraftMyCamperdb < schema.sql
   
6. **Run the Flask Application**
   ```sh
   flask run --port=5001

7. **Using the Api**

Access the API at http://127.0.0.1:5001/
Example endpoints:
   
 - __GET /projects__
 - __POST /projects__
 - __GET /resources__
 - __POST /resources__
 - __GET /projects/<int:project_id>/resources__
 - __DELETE /project_resources__

8. **Running the Client-Side Script
   ```sh
   python main.py

**Project Structure**

* __app.py__ : Flask application with API endpoints.
* __utils.py__: Utility functions for database operations.
* __config.py__: Database configuration.
* __main.py__: Client-side script for interacting with the API.
* __requirements.txt__: Python dependencies.
* __CraftMyCamperdb.sql__: SQL script for setting up the database schema.

**Usage**

Follow the prompts in the main.py script to interact with the API, manage projects, add resources, and check budgets.

**Notes**

Ensure your MySQL server is running and accessible.
Adjust the configuration and script paths as needed for your environment.
