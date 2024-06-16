-- create data base 
CREATE DATABASE IF NOT EXISTS aet;

-- use database aet
USE aet;

-- creates customers table 
CREATE TABLE customers ( 
customer_id INT PRIMARY KEY,
business_name VARCHAR(200) NOT NULL, 
last_name VARCHAR(50) NOT NULL, 
first_name VARCHAR(50) NOT NULL, 
contact_number VARCHAR(20), 
email VARCHAR(100) UNIQUE
);

-- create categories table
CREATE TABLE categories ( 
category_id INT PRIMARY KEY NOT NULL, 
category_name VARCHAR(100), 
description TEXT 
);

-- create table suppliers
CREATE TABLE suppliers ( 
supplier_id INT PRIMARY KEY, 
supplier_name VARCHAR(50) NOT NULL, 
contact_number VARCHAR(20), 
email VARCHAR(150) UNIQUE
);

-- create products table
CREATE TABLE products ( 
product_id INT PRIMARY KEY,
product_name VARCHAR(255) NOT NULL,
category_id INT, 
supplier_id INT, 
unit_price DECIMAL (10, 2) NOT NULL,
FOREIGN KEY (category_id) REFERENCES categories(category_id),
FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

-- create orders table
CREATE TABLE orders ( 
order_id INT PRIMARY KEY, 
customer_id INT,
order_status VARCHAR(100) NOT NULL, 
order_date DATE NOT NULL, 
order_value DECIMAL NOT NULL, 
shipped_date DATE, 
supplier_id INT, 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id), 
CONSTRAINT chk_order_status CHECK (order_status IN ('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled')) 
);


-- create order details table
CREATE TABLE order_details (
order_detail_id INT PRIMARY KEY,
order_id INT, 
product_id INT, 
quantity_ordered INT, 
unit_price DECIMAL(10, 2), 
FOREIGN KEY (order_id) REFERENCES orders(order_id), 
FOREIGN KEY (product_id) REFERENCES products(product_id)
 );

-- create address table 
CREATE TABLE addresses ( 
address_id INT PRIMARY KEY, 
building_number VARCHAR(255), 
street_name VARCHAR(100), 
city VARCHAR(100), country VARCHAR(100), 
postcode VARCHAR(150), 
customer_id INT, 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id) 
);


-- adding data into customers with default value for contact number 
INSERT INTO customers (customer_id, business_name, last_name, first_name, contact_number, email) 
VALUES 
(1, 'Airbus', 'Smith', 'Jerry', DEFAULT, 'jerry.smith@example.com'), 
(2, 'Raytheon', 'Doe', 'Alice', DEFAULT, 'alice.doe@example.com'), 
(3, 'Norththorp Grunman', 'Johnson', 'Bob', DEFAULT, 'bob.johnson@example.com'), 
(4, 'GE Aviation', 'Williams', 'Emily', DEFAULT, 'emily.williams@example.com'),
(5, 'Honeywell', 'Anderson', 'Michael', DEFAULT, 'michael.anderson@example.com'), 
(6, 'Rolls-Royce', 'Martinez', 'Sophia', DEFAULT, 'sophia.martinez@example.com'), 
(7, 'L3Harris', 'Thompson', 'David', DEFAULT, 'david.thompson@example.com'), 
(8, 'Boeing', 'Garcia', 'Emma', DEFAULT, 'emma.garcia@example.com');


-- suppliers data 
INSERT INTO 
suppliers (supplier_id, supplier_name, contact_number, email) 
VALUES 
(1, 'USATCO', '123-456-7890', 'info@usatco.com'), 
(2, 'CHERRY', '987-654-3210', 'info@cherry.com');

-- categories data 
INSERT INTO categories 
(category_id, category_name, description) 
VALUES 
(1, 'Abrasive Tools', 'Tools designed for abrasive tasks.'), 
(2, 'Air Drills & Accessories', 'Includes various air drills and accessories.'), 
(3, 'Application Tools & Accessories', 'Tools and accessories for specific applications.'),
 (4, 'Assembly Tools', 'Tools used in assembly processes.'), 
(5, 'Cable, Wire & Tubing Tools', 'Tools designed for handling cables, wires, and tubing.'), 
(6, 'Cutting Tools', 'Tools specifically designed for cutting.'), 
(7, 'Hand Tools', 'Manual tools for various tasks.'), 
(8, 'Inspection Tools', 'Tools used for inspection purposes.'), 
(9, 'Material Removal Tools', 'Tools used for removing materials.'), 
(10, 'Riveting Tools', 'Tools for riveting tasks.'),
(11, 'Sheet Metal Forming Equipment', 'Equipment used in forming sheet metals.'), 
(12, 'Shop Tools', 'Tools commonly used in workshops.');

-- products data
INSERT INTO 
products (product_id, product_name, supplier_id, category_id, unit_price) 
VALUES 
(1, 'Abrasive Wheel', 1, 1, 25.00), 
(2, 'Air Drill Kit', 1, 2, 150.00), 
(3, 'Assembly Tool Set', 2, 4, 300.00), 
(4, 'Cable Cutter', 2, 5, 80.00), 
(5, 'Cutting Machine', 1, 6, 500.00), 
(6, 'Hand Saw', 1, 7, 45.00), 
(7, 'Inspection Camera', 2, 8, 200.00), 
(8, 'Drill Bit Set', 2, 2, 50.00);


-- orders data 
INSERT INTO orders 
(order_id, customer_id, order_status, order_date, order_value, shipped_date, supplier_id) 
VALUES 
(1, 3, 'Pending', '2024-06-15', 500.00, NULL, 1),
(2, 5, 'Delivered', '2024-01-05', 300.00, '2024-01-10', 2),
(3, 6, 'Shipped', '2024-06-14', 700.00, '2024-06-15', 1), 
(4, 2, 'Delivered', '2024-03-01', 1000.00, '2024-03-10', 2), 
(5, 8, 'Pending', '2024-06-16', 450.00, NULL, 1), 
(6, 7, 'Shipped', '2024-06-10', 600.00, '2024-06-18', 2),
(7, 4, 'Delivered', '2024-06-16', 800.00, '2024-06-17', 1), 
(8, 1, 'Processing', '2024-06-15', 350.00, NULL, 2);


-- order details data
INSERT INTO order_details
 (order_detail_id, order_id, product_id, quantity_ordered, unit_price) 
VALUES 
(1, 1, 1, 2, 25.00), 
(2, 1, 3, 1, 150.00), 
(3, 2, 4, 1, 80.00), 
(4, 2, 5, 1, 500.00), 
(5, 3, 6, 3, 45.00), 
(6, 3, 7, 2, 200.00), 
(7, 4, 8, 2, 50.00), 
(8, 4, 2, 1, 150.00);

-- address data 
INSERT INTO addresses 
(address_id, building_number, street_name, city, country, postcode, customer_id) 
VALUES 
(1, '123', 'Main Street', 'London', 'UK', 'SW1A 1AA', 1), 
(2, '456', 'High Street', 'Manchester', 'UK', 'M1 1AA', 2), 
(3, '789', 'Park Avenue', 'Birmingham', 'UK', 'B1 1AA', 3),
(4, '101', 'Church Road', 'Glasgow', 'UK', 'G1 1AA', 4),
(5, '234', 'Queen Street', 'Belfast','UK', 'BT1 1AA', 5), 
(6, '123', 'Main Street', 'Los Angeles', 'USA', '90001', 6), 
(7, '456', 'Oak Avenue', 'New York', 'USA', '10001', 7), 
(8, '789', 'Maple Lane', 'Chicago', 'USA', '60601', 8);

