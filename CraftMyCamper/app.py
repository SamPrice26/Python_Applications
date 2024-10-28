from flask import Flask, jsonify, request
from utils import get_projects, add_project, get_resources, add_resource, calculate_remaining_budget, get_categories, add_project_resource, remove_project_resource, get_project_resources

app = Flask(__name__)

# Endpoint to fetch all projects
@app.route('/projects', methods=['GET'])
def fetch_projects():
    projects = get_projects()
    return jsonify(projects)

# Endpoint to create a new project
@app.route('/projects', methods=['POST'])
def create_project():
    project = request.get_json()
    add_project(
        project_name=project['project_name'],
        description=project['description'],
        budget=project['budget']
    )
    return jsonify({'message': 'Project added successfully!'}), 201

# Endpoint to fetch all resources
@app.route('/resources', methods=['GET'])
def fetch_resources():
    resources = get_resources()
    return jsonify(resources)

# Endpoint to create a new resource
@app.route('/resources', methods=['POST'])
def create_resource():
    try:
        resource = request.get_json()
        add_resource(
            name=resource['name'],
            category_id=resource['category_id'],
            description=resource['description'],
            price=resource['price'],
            quantity=resource['quantity'],
            weight_kg=resource.get('weight_kg', None),
            project_id=resource.get('project_id', None)
        )
        return jsonify({'message': 'Resource added successfully!'}), 201
    except Exception as e:
        print(f"Error adding resource: {e}")
        return jsonify({'error': str(e)}), 500

# Endpoint to fetch resources linked to a specific project
@app.route('/projects/<int:project_id>/resources', methods=['GET'])
def fetch_project_resources(project_id):
    resources = get_project_resources(project_id)
    return jsonify(resources)

# Endpoint to link a resource to a project
@app.route('/project_resources', methods=['POST'])
def create_project_resource():
    try:
        data = request.get_json()
        add_project_resource(
            project_id=data['project_id'],
            resource_id=data['resource_id']
        )
        return jsonify({'message': 'Resource linked to project successfully!'}), 201
    except Exception as e:
        print(f"Error linking resource to project: {e}")
        return jsonify({'error': str(e)}), 500

# Endpoint to remove a resource from a project
@app.route('/project_resources', methods=['DELETE'])
def delete_project_resource():
    try:
        data = request.get_json()
        remove_project_resource(
            project_id=data['project_id'],
            resource_id=data['resource_id']
        )
        return jsonify({'message': 'Resource removed from project successfully!'}), 200
    except Exception as e:
        print(f"Error removing resource from project: {e}")
        return jsonify({'error': str(e)}), 500

# Endpoint to calculate the remaining budget for a project
@app.route('/projects/<int:project_id>/remaining_budget', methods=['GET'])
def fetch_remaining_budget(project_id):
    remaining_budget = calculate_remaining_budget(project_id)
    return jsonify({'remaining_budget': remaining_budget})

# Endpoint to fetch all categories
@app.route('/categories', methods=['GET'])
def fetch_categories():
    categories = get_categories()
    return jsonify(categories)

if __name__ == '__main__':
    app.run(debug=True, port=5001)