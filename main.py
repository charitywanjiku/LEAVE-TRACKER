
import sqlite3
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

        connection.commit()
        print("Tables created successfully.")
    except sqlite3.Error as error:
        print(f"Failed to create tables: {error}")
    finally:
        if connection:
            connection.close()

def save_to_database(full_name, email_address, department, reason, start_date, end_date):
    try:
        connection = sqlite3.connect('leave_tracker.db')
        cursor = connection.cursor()

        # Insert employee
        cursor.execute('''INSERT INTO employees (full_name, email, department)
                          VALUES (?, ?, ?)''', (full_name, email_address, department))
        employee_id = cursor.lastrowid

        # Insert leave request
        cursor.execute('''INSERT INTO leave_requests (employee_id, reason, start_date, end_date, status)
                          VALUES (?, ?, ?, ?, ?)''', (employee_id, reason, start_date, end_date, 'pending'))

        connection.commit()
        print("Leave request saved to database successfully.")
    except sqlite3.Error as error:
        print(f"Failed to save leave request to database: {error}")
    finally:
        if connection:
            connection.close()

def delete_leave_request(request_id):
    try:
        connection = sqlite3.connect('leave_tracker.db')
        cursor = connection.cursor()

        # Delete leave request
        cursor.execute('''DELETE FROM leave_requests WHERE request_id = ?''', (request_id,))
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
    print("1. Send Leave Request")
    print("2. Delete Leave Request")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        full_name = input("Enter your full name: ")
        email_address = input("Enter your email address: ")
        department = input("Enter your department: ")
        reason = input("Enter reason for leave: ")
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")

        save_to_database(full_name, email_address, department, reason, start_date, end_date)
    elif choice == "2":
        request_id = input("Enter the request ID to delete: ")
        delete_leave_request(request_id)
    elif choice == "3":
        print("Exiting the Leave Tracker CLI. Goodbye!")
    else:
        print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()

