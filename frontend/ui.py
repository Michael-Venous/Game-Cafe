import sys
import os

# This allows the frontend to import your backend logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend import session_logic

LINE = "─" * 70

def print_table(headers, rows):
    """Helper function from Aadil's code to format terminal output cleanly."""
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
        print("  GAME CAFE - SESSION MANAGEMENT (Milestone 2)")
        print(LINE)
        print("  1. View all Sessions")
        print("  2. Start a new Session")
        print("  0. Exit")
        choice = input("\n  Select an option: ").strip()

        if choice == "1":
            view_sessions()
        elif choice == "2":
            start_new_session()
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
