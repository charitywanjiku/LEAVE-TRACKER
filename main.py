import smtplib
from email.mime.text import MIMEText
import sqlite3

def send_email(full_name, department, reason, start_date, end_date, email_address, days_number):
    # Configuration
    mail_server = 'smtp.mailtrap.io'
    mail_port = 2525
    mail_username = '921198b40eda6e'
    mail_password = 'c19ea17cc955ea'
    sender_email = 'peter@mailtrap.io'
    recipient_email = 'paul@mailtrap.io'

    # Message Content
    leave_request_email = f"""
    Dear HR,
    Good day, I hope this message finds you well.
    
    I would like to request leave from the {department} department for {days_number} days.
    
    - Reason for Leave: {reason}
    - Start Date: {start_date}
    - End Date: {end_date}

    Kind regards,
    {full_name}
    {email_address}
    """

    # SMTP Connection
    try:
        server = smtplib.SMTP(mail_server, mail_port)
        server.starttls()
        server.login(mail_username, mail_password)
        
        # Email construction
        msg = MIMEText(leave_request_email)
        msg['Subject'] = f'Leave Request - {full_name}'
        msg['From'] = sender_email
        msg['To'] = recipient_email
        
        # Send Email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully!")
        server.quit()
    except Exception as e:
        print(f"Error: {e}")

def save_to_database(full_name, department, reason, start_date, end_date, email_address, days_number):
    try:
        connection = sqlite3.connect('leave_requests.db')
        cursor = connection.cursor()
        sql = "INSERT INTO requests (full_name, department, reason, start_date, end_date, email_address, days_number) VALUES (?, ?, ?, ?, ?, ?, ?)"
        val = (full_name, department, reason, start_date, end_date, email_address, days_number)
        cursor.execute(sql, val)
        connection.commit()
        print("Record inserted successfully into SQLite database")
    except sqlite3.Error as error:
        print(f"Failed to insert record into SQLite table: {error}")
    finally:
        if connection:
            connection.close()
            print("SQLite connection is closed")

def main():
    full_name = input("Enter your full name: ")
    department = input("Enter your department: ")
    reason = input("Enter reason for leave: ")
    start_date = input("Enter start date: ")
    end_date = input("Enter end date: ")
    email_address = input("Enter your email address: ")
    days_number = input("Enter number of days for leave: ")

    send_email(full_name, department, reason, start_date, end_date, email_address, days_number)
    save_to_database(full_name, department, reason, start_date, end_date, email_address, days_number)

if __name__ == "__main__":
    main()
