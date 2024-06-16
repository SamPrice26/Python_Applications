-- use aet db
USE aet;

-- retrieving data queries 

-- query product with the most sales and total profit 
SELECT 
p.product_id, 
p.product_name, 
SUM(od.quantity_ordered) AS total_sales,
SUM(od.quantity_ordered * p.unit_price) AS total_price
FROM products p 
JOIN order_details od ON p.product_id = od.product_id 
GROUP BY 
p.product_id, p.product_name 
ORDER BY 
total_sales DESC 
LIMIT 1; 

-- query customer with the highest purchase amount 
SELECT 
c.customer_id, 
c.business_name, 
SUM(od.quantity_ordered * od.unit_price) AS total_purchase_amount 
FROM 
customers c 
JOIN 
orders o ON c.customer_id = o.customer_id 
JOIN 
order_details od ON o.order_id = od.order_id 
GROUP BY
 c.customer_id, c.business_name 
ORDER BY
 total_purchase_amount DESC 
LIMIT 1; 


-- query customer with highest orders amount
SELECT 
    c.customer_id,
    c.business_name,
    SUM(od.quantity_ordered) AS total_quantity_ordered
FROM 
    customers c
LEFT JOIN 
    orders o ON c.customer_id = o.customer_id
LEFT JOIN 
    order_details od ON o.order_id = od.order_id
GROUP BY 
    c.customer_id, c.business_name
ORDER BY 
    total_quantity_ordered DESC
LIMIT 1;

-- query most profitable month based on sales 
SELECT 
MONTHNAME(o.order_date) AS order_month, 
SUM(od.quantity_ordered * od.unit_price) AS total_sales 
FROM 
orders o 
JOIN order_details od ON o.order_id = od.order_id 
GROUP BY 
order_month 
ORDER BY 
total_sales DESC 
LIMIT 1; 

-- query customers who haven't ordered in over 2 months
SELECT 
    c.customer_id, 
    c.business_name, 
    MAX(o.order_date) AS last_order_date
FROM 
    customers c 
LEFT JOIN
    orders o ON c.customer_id = o.customer_id 
GROUP BY
    c.customer_id, c.business_name 
HAVING 
    MAX(o.order_date) < DATE_SUB(NOW(), INTERVAL 2 MONTH);
    
-- using IN to filter customers using specific order id
SELECT c.*
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id = 6;

-- stored procedure to retrieve order statuses for a customer 

 DELIMITER //

CREATE PROCEDURE GetOrderStatusForCustomer (
    IN customer_id_param INT
)
BEGIN
    SELECT 
        o.order_id, 
        o.order_status, 
        o.order_date, 
        o.order_value, 
        o.shipped_date 
    FROM 
        orders o 
    WHERE 
        o.customer_id = customer_id_param;
END //

DELIMITER ;

SHOW PROCEDURE STATUS WHERE Name = 'GetOrderStatusForCustomer';

-- checking order status of different customers using id
CALL GetOrderStatusForCustomer(6); 
CALL GetOrderStatusForCustomer(3);
CALL GetOrderStatusForCustomer(4); 


-- query to delete discontinued product from db, however

-- Add column 'discontinued' to the 'products' table 
ALTER TABLE products 
ADD COLUMN discontinued 
TINYINT(1) NOT NULL DEFAULT 0; 

-- updating a product to mark it as discontinued 
UPDATE products 
SET discontinued = 1 
WHERE product_id = 8; 

-- delete from order details
DELETE FROM order_details 
WHERE product_id = 8;

-- delete discontinued product with product_id = 8 
DELETE FROM 
products WHERE product_id = 8;














