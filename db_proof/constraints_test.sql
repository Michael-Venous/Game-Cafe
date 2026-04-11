USE gamecafe;
 
-- ============================================================
-- CONSTRAINT TEST 1: NOT NULL violation on Employee for 'Name'
-- Constraint: Name VARCHAR(15) NOT NULL
-- Expected Error: ERROR 1364 (HY000): Field 'Name' doesn't have a default value
-- ============================================================
INSERT INTO Employee (Employee_id, Role, HourlyWage) VALUES (999, 'Manager', 20);


-- ============================================================
-- CONSTRAINT TEST 2: CHECK constraint violation on game
-- Constraint: CHECK (difficulty >= 1 AND difficulty <= 10)
-- Expected Error: ERROR 3819 (HY000): Check constraint 'game_chk_1' is violated.
-- ============================================================
INSERT INTO Game (title, genre, difficulty)
VALUES ('TestGame', 'RPG', 15);


-- ============================================================
-- CONSTRAINT TEST 3: UNIQUE / PRIMARY KEY violation on Customer
-- Constraint: Customer_id is PRIMARY KEY (must be unique)
-- Expected Error: ERROR 1062 (23000): Duplicate entry '161' for key 'Customer.PRIMARY'
-- ============================================================
INSERT INTO Customer (Customer_id, Name, email, Membership)
VALUES (161, 'Jane Smith', 'jane.smith@example.com', TRUE);
