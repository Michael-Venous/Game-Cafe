import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend import session_logic

LINE = "─" * 70

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
        # Convert None values to "NULL" or "Active" for better readability
        clean_row = [val if val is not None else "Active" for val in row]
        print(fmt.format(*clean_row))

def view_sessions():
    print(f"\n{LINE}\n  ALL GAME CAFE SESSIONS\n{LINE}")
    rows = session_logic.get_all_sessions()
    print_table(["Session ID", "Customer ID", "Station ID", "Start Time", "End Time", "Total Cost ($)"], rows)
    input("\nPress Enter to continue...")

def start_new_session():
    print(f"\n{LINE}\n  START NEW SESSION\n{LINE}")
    customer_id = input("  Enter Customer ID (e.g., 161 or 301): ").strip()
    station_id = input("  Enter Station ID (e.g., 1, 2, or 3): ").strip()

    result = session_logic.create_active_session(customer_id, station_id)
    if result is True:
        print("\n  Success! Session started.")
    else:
        print(f"\n  Failed to start session. {result}")
    input("\nPress Enter to continue...")

def main():
    while True:
        print(f"\n{LINE}")
        print("  GAME CAFE")
        print(LINE)
        print("  1. View all Sessions")
        print("  2. Start a new Session")
        print("  3. EMPLOYEE TABLE")
        print("  4. MENU ITEMS TABLE")
        print("  5. CUSTOMERS TABLE")
        print("  6. VIEWS")
        print("  7. REPORTS / ANALYTICS")
        print("  0. Exit")
        choice = input("\n  Select an option: ").strip()

        if choice == "1":
            view_sessions()
        elif choice == "2":
            start_new_session()
        elif choice == "3":
            print("  1. View all menu items")
            print("  2. Search item by ID")
            print("  3. Add new menu item")
            print("  4. Update item price")
            print("  5. Delete menu item")
            print("  0. Exit")
            secondChoice = input("\n  Select an option: ").strip()
            if secondChoice == "1":
                session_logic.view_employees()
            elif secondChoice == "2":
                session_logic.search_employee()
            elif secondChoice == "3":
                session_logic.add_employee()
            elif secondChoice == "4":
                session_logic.update_employee_wage()
            elif secondChoice == "5":
                session_logic.delete_employee()
            elif secondChoice == "0":
                pass
            else:
                print("  Invalid option.")
        elif choice == "4":
            print("  1. View all menu items")
            print("  2. Search item by ID")
            print("  3. Add new menu item")
            print("  4. Update item price")
            print("  5. Delete menu item")
            print("  0. Exit")
            secondChoice = input("\n  Select an option: ").strip()
            if secondChoice == "1":
                session_logic.view_menuitems()
            elif secondChoice == "2":
                session_logic.search_menuitem()
            elif secondChoice == "3":
                session_logic.add_menuitem()
            elif secondChoice == "4":
                session_logic.update_menuitem_price()
            elif secondChoice == "5":
                session_logic.delete_menuitem()
            elif secondChoice == "0":
                pass
            else:
                print("  Invalid option.")
        elif choice == "5":
            print("  1. View all customers")
            print("  2. Search customer by ID")
            print("  3. Add new customer")
            print("  4. Toggle membership status")
            print("  5. Delete customer")
            print("  0. Exit")
            secondChoice = input("\n  Select an option: ").strip()
            if secondChoice == "1":
                session_logic.view_customers()
            elif secondChoice == "2":
                session_logic.search_customer()
            elif secondChoice == "3":
                session_logic.add_customer()
            elif secondChoice == "4":
                session_logic.toggle_membership()
            elif secondChoice == "5":
                session_logic.delete_customer()
            elif secondChoice == "0":
                pass
            else:
                print("  Invalid option.")
        elif choice == "6":
            print("  1. Session Summary")
            print("  2. Station Availability")
            print("  0. Back")
            secondChoice = input("\n  Select an option: ").strip()
            if secondChoice == "1":
                session_logic.view_session_summary()
            elif secondChoice == "2":
                session_logic.view_station_availability()
            elif secondChoice == "0":
                pass
            else:
                print("  Invalid option.")
        elif choice == "7":
            print("  1. Query 2: Active Sessions (No end time)")
            print("  2. Query 3: Customer Total Sessions")
            print("  3. Query 4: Games Available per Station")
            print("  4. Query 5: Customer Total Spending")
            print("  5. Query 6: Active Session Details")
            print("  6. Query 7: Full Order Breakdown")
            print("  7. Query 8: Revenue per Station")
            print("  8. Query 9: Order Status & Notes")
            print("  0. Back")
            secondChoice = input("\n  Select an option: ").strip()
            if secondChoice == "1":
                session_logic.run_query_2()
            elif secondChoice == "2":
                session_logic.run_query_3()
            elif secondChoice == "3":
                session_logic.run_query_4()
            elif secondChoice == "4":
                session_logic.run_query_5()
            elif secondChoice == "5":
                session_logic.run_query_6()
            elif secondChoice == "6":
                session_logic.run_query_7()
            elif secondChoice == "7":
                session_logic.run_query_8()
            elif secondChoice == "8":
                session_logic.run_query_9()
            elif secondChoice == "0":
                pass
            else:
                print("  Invalid option.")
        elif choice == "0":
            print("\n  Goodbye!\n")
            break
        else:
            print("  Invalid option.")

if __name__ == "__main__":
    # Ensure the mysql-connector-python package is installed
    try:
        import mysql.connector
    except ImportError:
        print("Error: Please run 'pip install mysql-connector-python' first.")
        sys.exit(1)

    main()
