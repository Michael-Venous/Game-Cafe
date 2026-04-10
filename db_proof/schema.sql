-- Create the database
CREATE DATABASE IF NOT EXISTS gamecafe;
USE gamecafe;

-- Aadil Qureshi's tables
CREATE TABLE Employee (
    Employee_id INT UNIQUE NOT NULL,
    Name VARCHAR(15) NOT NULL,
    Role VARCHAR(20) NOT NULL,
    HourlyWage SMALLINT UNSIGNED NOT NULL,
    PRIMARY KEY (Employee_id)
);

CREATE TABLE MenuItem (
    Item_id INT UNIQUE NOT NULL,
    Name VARCHAR(15) NOT NULL,
    Category VARCHAR(30) NOT NULL,
    Price DECIMAL(5, 2) UNSIGNED NOT NULL,
    PRIMARY KEY (Item_id)
);

CREATE TABLE Customer (
    Customer_id INT UNIQUE NOT NULL,
    Name VARCHAR(15) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    Membership BOOLEAN NOT NULL,
    PRIMARY KEY (Customer_id)
);

-- Nikolas Enriquez's tables
CREATE TABLE station (
    station_id INT NOT NULL AUTO_INCREMENT,
    station_type VARCHAR(7) NOT NULL,
    hourly_rate INT NOT NULL,
    availability BOOLEAN NOT NULL,
    CHECK (hourly_rate > 10),
    CHECK (station_type = 'PC' OR station_type = 'VR' OR station_type = 'Console'),
    PRIMARY KEY (station_id)
);

CREATE TABLE game (
    game_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(20) NOT NULL,
    genre VARCHAR(20) NOT NULL,
    difficulty INT NOT NULL,
    CHECK (difficulty >= 1 AND difficulty <= 10),
    PRIMARY KEY (game_id)
);


CREATE TABLE station_game (
    station_id INT NOT NULL,
    game_id INT NOT NULL,
    PRIMARY KEY (station_id, game_id),
    CONSTRAINT fk_station_id FOREIGN KEY (station_id) REFERENCES station(station_id),
    CONSTRAINT fk_game_id FOREIGN KEY (game_id) REFERENCES game(game_id)
);

-- Michael's table
CREATE TABLE Session (
    session_id INT NOT NULL AUTO_INCREMENT,
    customer_id INT NOT NULL,
    station_id INT NOT NULL,
    start_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time DATETIME,
    total_cost DECIMAL(10, 2),
    PRIMARY KEY (session_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(Customer_id),
    FOREIGN KEY (station_id) REFERENCES station(station_id)
);

-- Alec Borque's tables
CREATE TABLE Orders (
    order_id INT NOT NULL,
    customer_id INT,
    employee_id INT,
    order_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(6,2),
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(Customer_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(Employee_id)
);


CREATE TABLE Order_Item (
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    subtotal DECIMAL(5, 2) NOT NULL CHECK (subtotal >= 0),
    PRIMARY KEY (order_id, item_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (item_id) REFERENCES MenuItem(Item_id)
);

CREATE TABLE Order_Status (
    status_id INT NOT NULL,
    order_id INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notes VARCHAR(250),
    PRIMARY KEY (status_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

CREATE VIEW view_session_summary AS
SELECT
    se.session_id,
    c.Name         AS customer_name,
    c.email,
    st.station_type,
    se.start_time,
    se.end_time,
    se.total_cost,
    TIMESTAMPDIFF(MINUTE, se.start_time, se.end_time) AS duration_minutes
FROM Session se
JOIN Customer c  ON se.customer_id = c.Customer_id
JOIN station st  ON se.station_id  = st.station_id;

CREATE VIEW view_station_availability AS
SELECT
    s.station_id,
    s.station_type,
    s.hourly_rate,
    s.availability,
    COUNT(g.game_id) AS num_games
FROM station s
LEFT JOIN station_game sg ON s.station_id = sg.station_id
LEFT JOIN game g ON sg.game_id = g.game_id
GROUP BY s.station_id, s.station_type, s.hourly_rate, s.availability;
