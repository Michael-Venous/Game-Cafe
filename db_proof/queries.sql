-- Query 1: All of the information from the Customer table
SELECT * FROM Customer;


-- Query 2: All sessions where there is no end time
SELECT * FROM Session WHERE end_time IS NULL;


-- Query 3: The name of the Customer and the total amount of sessions that they have
SELECT c.Name, COUNT(s.session_id) AS total_sessions
FROM Customer c JOIN Session s ON c.Customer_id = s.customer_id
GROUP BY c.Name;

-- Query 4: All games that are going to be available at each station with station type
SELECT s.station_id, s.station_type, g.title, g.genre, g.difficulty
FROM station s
JOIN station_game sg ON s.station_id = sg.station_id
JOIN game g ON sg.game_id = g.game_id;

-- Query 5: Total amount of spending per customer across all orders
SELECT c.Name, COUNT(o.order_id) AS total_orders, SUM(o.total_amount) AS total_spent
FROM Customer c
JOIN Orders o ON c.Customer_id = o.customer_id
GROUP BY c.Customer_id, c.Name;

-- Query 6: All active sessions (no end time yet) with customer name and station type
SELECT c.Name AS customer_name, s.station_type, sess.start_time
FROM Session sess
JOIN Customer c ON sess.customer_id = c.Customer_id
JOIN station s ON sess.station_id = s.station_id
WHERE sess.end_time IS NULL;

-- Query 7: Full order breakdown showing each customer, employee, item and quantity
SELECT c.Name AS customer, e.Name AS employee, mi.Name AS item, oi.quantity, oi.subtotal
FROM Orders o
JOIN Customer c ON o.customer_id = c.Customer_id
JOIN Employee e ON o.employee_id = e.Employee_id
JOIN Order_Item oi ON o.order_id = oi.order_id
JOIN MenuItem mi ON oi.item_id = mi.Item_id;

-- Query 8: Total amount of revenue that is generated per station
SELECT s.station_id, s.station_type, COUNT(sess.session_id) AS total_sessions, SUM(sess.total_cost) AS total_revenue
FROM station s
LEFT JOIN Session sess ON s.station_id = sess.station_id
GROUP BY s.station_id, s.station_type;

-- Query 9: All orders with their current status and any notes
SELECT o.order_id, c.Name AS customer, o.total_amount, os.status, os.updated_at, os.notes
FROM Orders o
JOIN Customer c ON o.customer_id = c.Customer_id
JOIN Order_Status os ON o.order_id = os.order_id
ORDER BY os.updated_at DESC;

CREATE TRIGGER before_updated_at_update
BEFORE UPDATE ON Order_Status
FOR EACH ROW
SET NEW.updated_at = NOW();
