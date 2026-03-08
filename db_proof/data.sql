USE gamecafe;

-- Aadil Qureshi's Employee Data
INSERT INTO Employee (Employee_id, Name, Role, HourlyWage) VALUES
(125, 'John Jacobs', 'Technician', 35),
(231, 'John Jacobs', 'Game Attendant', 35);

-- Aadil Qureshi's MenuItem Data
INSERT INTO MenuItem (Item_id, Name, Category, Price) VALUES
(561, 'Burger', 'Main Course', 9.99),
(289, 'Fries', 'Side Dish', 4.35);

-- Aadil Qureshi's Customer Data
INSERT INTO Customer (Customer_id, Name, email, Membership) VALUES
(161, 'John Doe', 'john.doe@example.com', TRUE),
(301, 'Peter Jones', 'peter.jones@example.com', FALSE);


-- Nikolas Enriquez's Station Data
INSERT INTO station (station_type, hourly_rate, availability) VALUES
('PC', 15, TRUE),
('VR', 25, FALSE),
('Console', 12, TRUE);

-- Nikolas Enriquez's Game Data
INSERT INTO game (title, genre, difficulty) VALUES
('Silksong', 'Metroidvania', 8),
('CounterStrike', 'FPS', 10),
('Balatro', 'Roguelike', 3);

-- Nikolas Enriquez's Station_Game Data
INSERT INTO station_game (station_id, game_id) VALUES
(1, 1), (1, 2), (1, 3),
(2, 2),
(3, 1), (3, 3);


-- Michael Venous's SESSION DATA
INSERT INTO Session (customer_id, station_id, start_time, end_time, total_cost) VALUES
(161, 1, '2026-03-05 10:00:00', '2026-03-05 12:00:00', 10.00),
(301, 2, '2026-03-06 11:00:00', NULL, NULL),
(161, 3, '2026-03-07 12:00:00', '2026-03-07 16:00:00', 20.00);

-- Alec Borque's Orders Data
INSERT INTO Orders (order_id, customer_id, employee_id, order_time, total_amount) VALUES
(2, 301, 231, '2026-03-02 14:00:00', 12.99),
(3, 161, 125, '2026-03-03 09:15:00', 24.50),
(4, 301, 125, '2026-03-04 18:30:00', 9.99);

-- Alec Borque's Order_Item Data
INSERT INTO Order_Item (order_id, item_id, quantity, subtotal) VALUES
(2, 289, 3, 13.05),
(3, 561, 1, 9.99),
(4, 289, 2, 8.70);

-- Alec Borque's Order_Status Data
INSERT INTO Order_Status (status_id, order_id, status, updated_at, notes) VALUES
(2, 2, 'Preparing', '2026-03-02 14:05:00', 'Order is being prepared'),
(3, 3, 'Delivered', '2026-03-03 09:45:00', 'Order completed'),
(4, 4, 'Pending', '2026-03-04 18:31:00', 'Waiting for staff');
