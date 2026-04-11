import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME", "gamecafe"),
}

LINE = "─" * 70

def clear():
    print("\n" * 2)


def header(title):
    print(f"\n{LINE}")
    print(f"  {title}")
    print(LINE)


def pause():
    input("\nPress Enter to continue...")


def prompt(label, required=True):
    while True:
        val = input(f"  {label}: ").strip()
        if val or not required:
            return val
        print("  (Field is required, please try again)")


def confirm(msg="Are you sure? (y/n): "):
    return input(msg).strip().lower() == "y"

def print_table(headers, rows):
    if not rows:
        print("  (no records found)")
        return
    if isinstance(rows, str): # Catch DB errors
        print(f"  {rows}")
        return

    widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0))
              for i, h in enumerate(headers)]
    fmt = "  " + "  ".join(f"{{:<{w}}}" for w in widths)
    sep = "  " + "  ".join("-" * w for w in widths)
    print(fmt.format(*headers))
    print(sep)
    for row in rows:
        # Convert None values to "NULL" or "Active"
        clean_row = [val if val is not None else "Active" for val in row]
        print(fmt.format(*clean_row))

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_all_sessions():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT session_id, customer_id, station_id, start_time, end_time, total_cost FROM Session")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Error as e:
        return f"Error: {e}"

def create_active_session(customer_id, station_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Session (customer_id, station_id) VALUES (%s, %s)",
            (customer_id, station_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Error as e:
        return f"Error: {e}"

#  EMPLOYEE MENU
def view_employees():
    header("All Employees")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT Employee_id, Name, Role, HourlyWage FROM Employee ORDER BY Employee_id")
        rows = cur.fetchall()
        print_table(["ID", "Name", "Role", "Hourly Wage ($)"], rows)
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()


def search_employee():
    header("Search Employee by ID")
    eid = prompt("Employee ID")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT Employee_id, Name, Role, HourlyWage FROM Employee WHERE Employee_id = %s", (eid,))
        rows = cur.fetchall()
        print_table(["ID", "Name", "Role", "Hourly Wage ($)"], rows)
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()


def add_employee():
    header("Add New Employee")
    eid  = prompt("Employee ID (integer)")
    name = prompt("Name (max 15 chars)")
    role = prompt("Role (max 20 chars)")
    wage = prompt("Hourly Wage (integer)")
    print(f"\n  Adding: ID={eid}, Name={name}, Role={role}, Wage={wage}")
    if not confirm():
        print("  Cancelled."); pause(); return
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Employee (Employee_id, Name, Role, HourlyWage) VALUES (%s, %s, %s, %s)",
            (eid, name, role, wage)
        )
        conn.commit()
        print("  Employee added successfully.")
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()

def update_employee_wage():
    header("Update Employee Hourly Wage")
    eid  = prompt("Employee ID")
    wage = prompt("New Hourly Wage (integer)")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE Employee SET HourlyWage = %s WHERE Employee_id = %s", (wage, eid))
        conn.commit()
        if cur.rowcount:
            print(f"  Wage updated for employee {eid}.")
        else:
            print("  No employee found with that ID.")
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()


def delete_employee():
    header("Delete Employee")
    eid = prompt("Employee ID to delete")
    if not confirm(f"  Delete employee {eid}? (y/n): "):
        print("  Cancelled."); pause(); return
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM Employee WHERE Employee_id = %s", (eid,))
        conn.commit()
        if cur.rowcount:
            print(f"  Employee {eid} deleted.")
        else:
            print("  No employee found with that ID.")
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()

#  MENU ITEM MENU
def view_menuitems():
    header("All Menu Items")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT Item_id, Name, Category, Price FROM Menu_Item ORDER BY Item_id")
        rows = cur.fetchall()
        print_table(["Item ID", "Name", "Category", "Price ($)"], rows)
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()


def search_menuitem():
    header("Search Menu Item by ID")
    iid = prompt("Item ID")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT Item_id, Name, Category, Price FROM Menu_Item WHERE Item_id = %s", (iid,))
        rows = cur.fetchall()
        print_table(["Item ID", "Name", "Category", "Price ($)"], rows)
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()


def add_menuitem():
    header("Add New Menu Item")
    iid      = prompt("Item ID (integer)")
    name     = prompt("Name (max 15 chars)")
    category = prompt("Category (max 30 chars)")
    price    = prompt("Price (e.g. 9.99)")
    print(f"\n  Adding: ID={iid}, Name={name}, Category={category}, Price={price}")
    if not confirm():
        print("  Cancelled."); pause(); return
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Menu_Item (Item_id, Name, Category, Price) VALUES (%s, %s, %s, %s)",
            (iid, name, category, price)
        )
        conn.commit()
        print("  Menu item added successfully.")
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()


def update_menuitem_price():
    header("Update Menu Item Price")
    iid   = prompt("Item ID")
    price = prompt("New Price (e.g. 12.99)")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE Menu_Item SET Price = %s WHERE Item_id = %s", (price, iid))
        conn.commit()
        if cur.rowcount:
            print(f"  Price updated for item {iid}.")
        else:
            print("  No item found with that ID.")
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()


def delete_menuitem():
    header("Delete Menu Item")
    iid = prompt("Item ID to delete")
    if not confirm(f"  Delete item {iid}? (y/n): "):
        print("  Cancelled."); pause(); return
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM Menu_Item WHERE Item_id = %s", (iid,))
        conn.commit()
        if cur.rowcount:
            print(f"  Item {iid} deleted.")
        else:
            print("  No item found with that ID.")
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()

#  CUSTOMER MENU
def view_customers():
    header("All Customers")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT Customer_id, Name, email, Membership FROM Customer ORDER BY Customer_id")
        rows = cur.fetchall()
        display = [(cid, name, email, "Yes" if mem else "No") for cid, name, email, mem in rows]
        print_table(["Customer ID", "Name", "Email", "Member?"], display)
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()


def search_customer():
    header("Search Customer by ID")
    cid = prompt("Customer ID")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT Customer_id, Name, email, Membership FROM Customer WHERE Customer_id = %s", (cid,))
        rows = cur.fetchall()
        display = [(c, n, e, "Yes" if m else "No") for c, n, e, m in rows]
        print_table(["Customer ID", "Name", "Email", "Member?"], display)
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()


def add_customer():
    header("Add New Customer")
    cid        = prompt("Customer ID (integer)")
    name       = prompt("Name (max 15 chars)")
    email      = prompt("Email (max 50 chars)")
    membership = prompt("Has membership? (y/n)").lower() == "y"
    print(f"\n  Adding: ID={cid}, Name={name}, Email={email}, Member={'Yes' if membership else 'No'}")
    if not confirm():
        print("  Cancelled."); pause(); return
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Customer (Customer_id, Name, email, Membership) VALUES (%s, %s, %s, %s)",
            (cid, name, email, membership)
        )
        conn.commit()
        print("  Customer added successfully.")
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()


def toggle_membership():
    header("Toggle Customer Membership")
    cid = prompt("Customer ID")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT Membership FROM Customer WHERE Customer_id = %s", (cid,))
        row = cur.fetchone()
        if not row:
            print("  No customer found with that ID.")
        else:
            new_status = not row[0]
            cur.execute("UPDATE Customer SET Membership = %s WHERE Customer_id = %s", (new_status, cid))
            conn.commit()
            print(f"  Membership set to {'Yes' if new_status else 'No'} for customer {cid}.")
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()


def delete_customer():
    header("Delete Customer")
    cid = prompt("Customer ID to delete")
    if not confirm(f"  Delete customer {cid}? (y/n): "):
        print("  Cancelled."); pause(); return
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM Customer WHERE Customer_id = %s", (cid,))
        conn.commit()
        if cur.rowcount:
            print(f"  Customer {cid} deleted.")
        else:
            print("  No customer found with that ID.")
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()

def view_session_summary():
    header("Session Summary (via view)")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT session_id, customer_name, email, station_type,
                   start_time, end_time, total_cost, duration_minutes
            FROM view_session_summary
            ORDER BY session_id
        """)
        rows = cur.fetchall()
        print_table(
            ["ID", "Customer", "Email", "Station", "Start", "End", "Cost ($)", "Min"],
            rows
        )
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()


def view_station_availability():
    header("Station Availability (via view)")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT station_id, station_type, hourly_rate,
                   availability, num_games
            FROM view_station_availability
            ORDER BY station_id
        """)
        rows = cur.fetchall()
        # Convert availability boolean to readable text
        display = [
            (sid, stype, rate, "Available" if avail else "In Use", games)
            for sid, stype, rate, avail, games in rows
        ]
        print_table(
            ["Station ID", "Type", "Rate ($/hr)", "Status", "# Games"],
            display
        )
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()


#  ANALYTICS / QUERIES MENU


def run_query_2():
    header("Query 2: Sessions with no end time")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Session WHERE end_time IS NULL")
        rows = cur.fetchall()
        print_table(["Session ID", "Customer ID", "Station ID", "Start Time", "End Time", "Total Cost"], rows)
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()

def run_query_3():
    header("Query 3: Customer Total Sessions")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.Name, COUNT(s.session_id) AS total_sessions
            FROM Customer c JOIN Session s ON c.Customer_id = s.customer_id
            GROUP BY c.Name
        """)
        rows = cur.fetchall()
        print_table(["Customer Name", "Total Sessions"], rows)
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()

def run_query_4():
    header("Query 4: Games Available per Station")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.station_id, s.station_type, g.title, g.genre, g.difficulty
            FROM Station s
            JOIN Station_Game sg ON s.station_id = sg.station_id
            JOIN Game g ON sg.game_id = g.game_id
        """)
        rows = cur.fetchall()
        print_table(["Station ID", "Type", "Game Title", "Genre", "Difficulty"], rows)
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()

def run_query_5():
    header("Query 5: Customer Total Spending")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.Name, COUNT(o.order_id) AS total_orders, SUM(o.total_amount) AS total_spent
            FROM Customer c
            JOIN Orders o ON c.Customer_id = o.customer_id
            GROUP BY c.Customer_id, c.Name
        """)
        rows = cur.fetchall()
        print_table(["Customer Name", "Total Orders", "Total Spent ($)"], rows)
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()

def run_query_6():
    header("Query 6: Active Session Details")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.Name AS customer_name, s.station_type, sess.start_time
            FROM Session sess
            JOIN Customer c ON sess.customer_id = c.Customer_id
            JOIN Station s ON sess.station_id = s.station_id
            WHERE sess.end_time IS NULL
        """)
        rows = cur.fetchall()
        print_table(["Customer Name", "Station Type", "Start Time"], rows)
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()

def run_query_7():
    header("Query 7: Full Order Breakdown")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.Name AS customer, e.Name AS employee, mi.Name AS item, oi.quantity, oi.subtotal
            FROM Orders o
            JOIN Customer c ON o.customer_id = c.Customer_id
            JOIN Employee e ON o.employee_id = e.Employee_id
            JOIN Order_Item oi ON o.order_id = oi.order_id
            JOIN Menu_Item mi ON oi.item_id = mi.Item_id
        """)
        rows = cur.fetchall()
        print_table(["Customer", "Employee", "Item", "Quantity", "Subtotal ($)"], rows)
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()

def run_query_8():
    header("Query 8: Revenue per Station")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.station_id, s.station_type, COUNT(sess.session_id) AS total_sessions, SUM(sess.total_cost) AS total_revenue
            FROM Station s
            LEFT JOIN Session sess ON s.station_id = sess.station_id
            GROUP BY s.station_id, s.station_type
        """)
        rows = cur.fetchall()
        print_table(["Station ID", "Type", "Total Sessions", "Total Revenue ($)"], rows)
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()

def run_query_9():
    header("Query 9: Order Status & Notes")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT o.order_id, c.Name AS customer, o.total_amount, os.status, os.updated_at, os.notes
            FROM Orders o
            JOIN Customer c ON o.customer_id = c.Customer_id
            JOIN Order_Status os ON o.order_id = os.order_id
            ORDER BY os.updated_at DESC
        """)
        rows = cur.fetchall()
        print_table(["Order ID", "Customer", "Total Amount ($)", "Status", "Updated At", "Notes"], rows)
        cur.close(); conn.close()
    except Error as e:
        print(f"  DB Error: {e}")
    pause()
