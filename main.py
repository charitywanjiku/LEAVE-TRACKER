
import sqlite3
from tabulate import tabulate

def create_tables():
    try:
        connection = sqlite3.connect('leave_tracker.db')
        cursor = connection.cursor()
        
        # Create Employees Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            full_name TEXT NOT NULL,
                            email TEXT NOT NULL,
                            department TEXT NOT NULL
                         )''')

        # Create Leave Requests Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS leave_requests (
                            request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            employee_id INTEGER NOT NULL,
                            reason TEXT NOT NULL,
                            start_date DATE NOT NULL,
                            end_date DATE NOT NULL,
                            status TEXT NOT NULL,
                            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
                         )''')

        # Create Leave Types Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS leave_types (
                            leave_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            leave_type_name TEXT NOT NULL,
                            description TEXT
                         )''')

        connection.commit()
        print("Tables created successfully.")
    except sqlite3.Error as error:
        print(f"Failed to create tables: {error}")
    finally:
        if connection:
            connection.close()

def save_leave_request(employee_id, reason, start_date, end_date):
    try:
        connection = sqlite3.connect('leave_tracker.db')
        cursor = connection.cursor()

        # Insert leave request
        cursor.execute('''INSERT INTO leave_requests (employee_id, reason, start_date, end_date, status)
                          VALUES (?, ?, ?, ?, ?)''', (employee_id, reason, start_date, end_date, 'pending'))

        connection.commit()
        print("Leave request sent successfully.")
    except sqlite3.Error as error:
        print(f"Failed to send leave request: {error}")
    finally:
        if connection:
            connection.close()

def save_leave_type(leave_type_name, description):
    try:
        connection = sqlite3.connect('leave_tracker.db')
        cursor = connection.cursor()

        # Insert leave type
        cursor.execute('''INSERT INTO leave_types (leave_type_name, description)
                          VALUES (?, ?)''', (leave_type_name, description))

        connection.commit()
        print("Leave type saved successfully.")
    except sqlite3.Error as error:
        print(f"Failed to save leave type: {error}")
    finally:
        if connection:
            connection.close()

def view_leave_requests():
    try:
        connection = sqlite3.connect('leave_tracker.db')
        cursor = connection.cursor()

        # Retrieve leave requests
        cursor.execute('''SELECT * FROM leave_requests''')
        leave_requests = cursor.fetchall()

        # Display leave requests
        if leave_requests:
            headers = ["Request ID", "Employee ID", "Reason", "Start Date", "End Date", "Status"]
            print(tabulate(leave_requests, headers=headers, tablefmt="pretty"))
        else:
            print("No leave requests found.")
    except sqlite3.Error as error:
        print(f"Failed to view leave requests: {error}")
    finally:
        if connection:
            connection.close()

def grant_leave(request_id):
    try:
        connection = sqlite3.connect('leave_tracker.db')
        cursor = connection.cursor()

        # Update status to 'leave successfully granted'
        cursor.execute('''UPDATE leave_requests 
                          SET status = 'leave successfully granted'
                          WHERE request_id = ?''', (request_id,))

        connection.commit()
        print("Leave successfully granted.")
    except sqlite3.Error as error:
        print(f"Failed to grant leave: {error}")
    finally:
        if connection:
            connection.close()

def delete_leave_request(request_id):
    try:
        connection = sqlite3.connect('leave_tracker.db')
        cursor = connection.cursor()

        # Delete leave request
        cursor.execute('''DELETE FROM leave_requests 
                          WHERE request_id = ?''', (request_id,))

        connection.commit()
        print("Leave request deleted successfully.")
    except sqlite3.Error as error:
        print(f"Failed to delete leave request: {error}")
    finally:
        if connection:
            connection.close()

def main():
    create_tables()

    print("Welcome to the Leave Tracker CLI")
    print("1. Manage Leave Types")
    print("2. View Existing Leave Requests")
    print("3. Send Leave Request")
    print("4. Grant Leave")
    print("5. Delete Leave Request")
    print("6. Exit")

    choice = input("Enter your choice: ")
    print(f"You chose option {choice}")

    try:
        if choice == "1":
            print("Leave Types Menu:")
            print("1. Add Leave Type")
            # Add more options for managing leave types (e.g., view, update, delete)
            
            leave_type_choice = input("Enter your choice: ")
            if leave_type_choice == "1":
                leave_type_name = input("Enter leave type name: ")
                description = input("Enter description: ")
                save_leave_type(leave_type_name, description)
                # Add code for other leave type management options
        elif choice == "2":
            view_leave_requests()
        elif choice == "3":
            print("Send Leave Request:")
            full_name = input("Enter your full name: ")
            email = input("Enter your email: ")
            department = input("Enter your department: ")
            reason = input("Enter reason for leave: ")
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")

            # Assuming employee_id is obtained based on the provided details (for simplicity)
            employee_id = 1  # Example: Assigning a dummy employee ID

            save_leave_request(employee_id, reason, start_date, end_date)
        elif choice == "4":
            print("Grant Leave:")
            request_id = input("Enter the request ID to grant leave: ")
            grant_leave(request_id)
        elif choice == "5":
            print("Delete Leave Request:")
            request_id = input("Enter the request ID to delete: ")
            delete_leave_request(request_id)
        elif choice == "6":
            print("Exiting the Leave Tracker CLI. Goodbye!")
        else:
            print("Invalid choice. Please enter a valid option.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
