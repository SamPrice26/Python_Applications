import json
import requests


# Function to fetch projects from the API
def get_projects():
    try:
        response = requests.get('http://127.0.0.1:5001/projects')
        response.raise_for_status()  # Raise error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching projects: {e}")
        return []


# Function to add a new project via POST request to API
def add_new_project(project_data):
    try:
        response = requests.post(
            'http://127.0.0.1:5001/projects',
            headers={'content-type': 'application/json'},
            data=json.dumps(project_data)
        )
        response.raise_for_status()  # Raise error for bad responses
        print("Project added successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error adding project: {e}")
        print(response.text)  # Print the error response for debugging


# Function to fetch resources from the API
def get_resources():
    try:
        response = requests.get('http://127.0.0.1:5001/resources')
        response.raise_for_status()  # Raise error for bad responses
        resources = response.json()
        return resources
    except requests.exceptions.RequestException as e:
        print(f"Error fetching resources: {e}")
        return []


# Function to fetch categories from the API
def get_categories():
    try:
        response = requests.get('http://127.0.0.1:5001/categories')
        response.raise_for_status()  # Raise error for bad responses
        categories = response.json()
        return categories
    except requests.exceptions.RequestException as e:
        print(f"Error fetching categories: {e}")
        return []


# Function to add a new resource via POST request to API
def add_new_resource(resource_data):
    try:
        response = requests.post(
            'http://127.0.0.1:5001/resources',
            headers={'content-type': 'application/json'},
            data=json.dumps(resource_data)
        )
        response.raise_for_status()  # Raise error for bad responses
        print("Resource added successfully!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error adding resource: {e}")
        print(response.text)  # Print the error response for debugging
        return False


# Function to remove a resource from a project
def remove_resource_from_project(project_id, resource_id):
    try:
        response = requests.delete(
            'http://127.0.0.1:5001/project_resources',
            headers={'content-type': 'application/json'},
            data=json.dumps({'project_id': project_id, 'resource_id': resource_id})
        )
        response.raise_for_status()
        print("Resource removed from project successfully!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error removing resource from project: {e}")
        print(response.text)  # Print the error response for debugging
        return False


# Function to get a valid float input from the user
def get_valid_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


# Function to get a valid int input from the user
def get_valid_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer value.")


# Function to calculate remaining budget
def calculate_remaining_budget(project_id):
    try:
        response = requests.get(f'http://127.0.0.1:5001/projects/{project_id}/remaining_budget')
        response.raise_for_status()  # Raise error for bad responses
        data = response.json()
        return data.get('remaining_budget', 0)
    except requests.exceptions.RequestException as e:
        print(f"Error calculating remaining budget: {e}")
        return 0


# Function to fetch resources linked to a specific project from the API
def get_project_resources(project_id):
    try:
        response = requests.get(f'http://127.0.0.1:5001/projects/{project_id}/resources')
        response.raise_for_status()  # Raise error for bad responses
        resources = response.json()
        return resources
    except requests.exceptions.RequestException as e:
        print(f"Error fetching project resources: {e}")
        return []


# Function to manage resource addition and removal
def manage_resources(selected_project_id):
    action = input(
        "Would you like to add a new resource, remove a resource, check van build budget, or close the program? (add/remove/check/close) ").lower()
    if action == 'add':
        resources = get_resources()
        print("####### Existing Resources #######")
        for idx, resource in enumerate(resources, start=1):
            print(
                f"{idx}. Name: {resource.get('name', 'N/A')}, Category: {resource.get('category_name', 'N/A')}, Price: {resource.get('price', 'N/A')}, Quantity: {resource.get('quantity', 'N/A')}")

        choice = input("Would you like to choose an existing resource or create a new one? (existing/new) ").lower()
        if choice == 'existing':
            resource_index = get_valid_int("Enter the number of the resource you want to add: ") - 1
            if 0 <= resource_index < len(resources):
                selected_resource = resources[resource_index]
                add_existing_resource_to_project(selected_resource, selected_project_id)
            else:
                print("Invalid resource selection.")
        elif choice == 'new':
            add_new_resource_to_project(selected_project_id)
        else:
            print("Invalid option. Please choose 'existing' or 'new'.")

        manage_resources(selected_project_id)
    elif action == 'remove':
        resources = get_project_resources(selected_project_id)
        if not resources:
            print("No resources found for this project.")
        else:
            print("####### Resources in Project #######")
            for idx, resource in enumerate(resources, start=1):
                print(
                    f"{idx}. Name: {resource.get('name', 'N/A')}, Category: {resource.get('category_name', 'N/A')}, Price: {resource.get('price', 'N/A')}, Quantity: {resource.get('quantity', 'N/A')}")

            resource_index = get_valid_int("Enter the number of the resource you want to remove: ") - 1
            if 0 <= resource_index < len(resources):
                selected_resource = resources[resource_index]
                remove_resource_from_project(selected_project_id, selected_resource['resource_id'])
            else:
                print("Invalid resource selection.")

        manage_resources(selected_project_id)
    elif action == 'check':
        check_budget(selected_project_id)
        manage_resources(selected_project_id)
    elif action == 'close':
        print("Thank you for using CreateMyCamper!")
    else:
        print("Invalid option. Please choose 'add', 'remove', 'check', or 'close'.")
        manage_resources(selected_project_id)


# Function to add an existing resource to a project
def add_existing_resource_to_project(resource, selected_project_id):
    project_resource_data = {
        'resource_id': resource.get('resource_id'),  # Use only resource_id to link resource to project
        'project_id': selected_project_id
    }
    print("Adding existing resource to project with data:",
          project_resource_data)  # Print the data being sent for debugging
    try:
        response = requests.post(
            'http://127.0.0.1:5001/project_resources',  # Correct endpoint for linking resource to project
            headers={'content-type': 'application/json'},
            data=json.dumps(project_resource_data)
        )
        response.raise_for_status()  # Raise error for bad responses
        print("Resource added to project successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error adding resource to project: {e}")
        print(response.text)  # Print the error response for debugging


# Function to add a new resource and link to a project
def add_new_resource_to_project(selected_project_id):
    categories = get_categories()
    if categories:
        print("####### Categories #######")
        for idx, category in enumerate(categories, start=1):
            print(f"{idx}. {category['name']}")
        category_index = get_valid_int("Enter the number of the category for the resource: ") - 1
        if 0 <= category_index < len(categories):
            category_id = categories[category_index]['id']
        else:
            print("Invalid category selection.")
            return
    else:
        print("No categories found. Please add categories first.")
        return

    name = input("Enter resource name: ")
    quantity = get_valid_int("Enter quantity: ")
    price = get_valid_float("Enter price: ")
    weight_kg = get_valid_float("Enter weight in kg: ") if categories[category_index]['name'] != 'tools' else None
    description = input("Enter description: ")

    resource_data = {
        'name': name,
        'category_id': category_id,
        'quantity': quantity,
        'price': price,
        'weight_kg': weight_kg,
        'description': description,
        'project_id': selected_project_id  # Include project_id to link resource to project
    }
    print("Adding resource to resource bank with data:", resource_data)  # Print the data being sent for debugging
    if add_new_resource(resource_data):
        print("Resource added to resource bank successfully.")


# Function to check the budget
def check_budget(selected_project_id):
    remaining_budget = calculate_remaining_budget(selected_project_id)
    print(f"${remaining_budget:.2f} of your budget is left for the camper build.")


# Main function to run the program
def run():
    print("Hello, welcome to CreateMyCamper")

    # Fetch and display projects
    projects = get_projects()
    if projects:
        print("####### Projects #######")
        for project in projects:
            print(
                f"ID: {project['project_id']}, Name: {project['project_name']}, Description: {project['description']}, Budget: {project['budget']}")
    else:
        print("No projects found or unable to connect to the API server.")

    # Prompt user to create a new project
    create_project = input("Would you like to create a new project? (yes/no) ").lower()
    if create_project == 'yes':
        project_name = input("Enter your project name: ")
        description = input("Enter your project description: ")
        budget = get_valid_float("Enter your project budget: ")

        project_data = {
            'project_name': project_name,
            'description': description,
            'budget': budget
        }
        add_new_project(project_data)
        # Fetch updated projects to get the new project's ID
        projects = get_projects()
        new_project_id = next(project['project_id'] for project in projects if project['project_name'] == project_name)
        manage_resources(new_project_id)

    elif create_project == 'no':
        existing_project = input("Do you have an existing project? (yes/no) ").lower()
        if existing_project == 'yes':
            if projects:
                print("Please choose from the existing projects:")
                project_names = [project['project_name'] for project in projects]
                for idx, project_name in enumerate(project_names, start=1):
                    print(f"{idx}. {project_name}")
                selected_project_index = get_valid_int("Enter the number of your project: ") - 1
                if 0 <= selected_project_index < len(project_names):
                    selected_project = projects[selected_project_index]
                    selected_project_id = selected_project['project_id']
                    print(f"Selected Project: {selected_project['project_name']}")
                    manage_resources(selected_project_id)
                else:
                    print("Invalid project selection.")
            else:
                print("No existing projects found.")
        else:
            print("Thank you for using CreateMyCamper!")
            return


if __name__ == '__main__':
    run()