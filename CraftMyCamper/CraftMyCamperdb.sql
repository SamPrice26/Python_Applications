-- Create database if not exists
CREATE DATABASE IF NOT EXISTS CraftMyCamperdb;

-- Use the database
USE CraftMyCamperdb;

-- Create categories table
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- Insert initial categories
INSERT INTO categories (name, description) VALUES
('tools', 'Tools used for construction and assembly.'),
('materials', 'Materials used in building and insulation.'),
('electrical', 'Components related to electrical systems.'),
('external', 'External fittings and fixtures.'),
('utilities', 'Utilities such as gas cookers, fridges, etc.');

-- Create projects table
CREATE TABLE projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE,
    budget DECIMAL(10, 2) -- total budget for project
);
-- Create budgets table
CREATE TABLE budgets (
    budget_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    category_id INT,
    amount DECIMAL(10, 2),
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Create resources table
CREATE TABLE resources (
    resource_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category_id INT NOT NULL,
    quantity INT,
    price DECIMAL(10, 2) NOT NULL,
    weight_kg DECIMAL(8, 2),
    description TEXT,
	project_id INT,
	FOREIGN KEY (project_id) REFERENCES projects(project_id),
	FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Insert initial resources
INSERT INTO resources (name, category_id, quantity, price, weight_kg, description)
VALUES
    ('Evolution R210SMS Sliding Mitre saw', 1, 1, 230.00, NULL, 'Sliding mitre saw for woodworking'),
    ('Bosch drill', 1, 1, 99.00, NULL, 'Electric drill for general use'),
    ('Circular saw', 1, 1, 40.00, NULL, 'Circular saw for cutting wood'),
    ('Jigsaw', 1, 1, 28.99, NULL, 'Jigsaw for precise cutting'),

    ('Recticel Instafit Polyurethane Insulation board(T)25mm multi pack', 2, 1, 50.00, NULL, 'Polyurethane insulation board'),
    ('Closed cell foam spray', 2, 1, 22.00, NULL, 'Closed cell foam for insulation'),
    ('Sikaflex', 2, 1, 16.00, NULL, 'Adhesive sealant'),
    ('Rough sawn treated timber', 2, 1, 43.76, NULL, 'Treated timber for construction'),

    ('Core-12V 24V 48V 200Ah Deep Cycle Lithium Iron Phosphate Battery', 3, 1, 516.65, NULL, 'Lithium iron phosphate battery'),
    ('2000W 12V Pure Sine Wave Inverter With English Standard Socket (UPS Function)', 3, 1, 174.99, NULL, 'Power inverter with UPS function'),
    ('100w compact rigid solar panel', 3, 1, 97.91, NULL, 'Compact solar panel'),

    ('Dometic Heki 2 skylight', 4, 1, 400.00, NULL, 'Roof skylight for vans'),
    ('Caravan door', 4, 1, 150.00, NULL, 'External door for caravans'),

    ('Gas cooker', 5, 1, 325,  NULL, 'Gas-powered cooker'),
    ('Dometic 10.4 Compressor Fridge', 5, 1, 599.00, NULL, 'Compressor fridge for camping');

INSERT INTO projects (project_id, project_name, description, start_date, budget)
VALUES
    (1, 'LutonVan', 'my first campervan conversion', '2024-04-30', '15000');

-- Create project_resources table
CREATE TABLE project_resources (
    project_resources_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    resource_id INT,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (resource_id) REFERENCES resources(resource_id)
);
