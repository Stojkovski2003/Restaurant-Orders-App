from pyisemail import is_email
import re
import sqlite3
from random import randint
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import time

with sqlite3.connect('C:/Users/stefan/Desktop/Programiranje/restaurant_orders_app/employees.db', check_same_thread=False) as conn:
    c = conn.cursor()
    c.execute("SELECT username FROM employees")
    username_list = [username for t in c.fetchall() for username in t]
    c.execute("SELECT email FROM employees")
    email_list = [email for t in c.fetchall() for email in t]

    def register_employee():
        employee_info = {
            "username" : None,
            "email" : None,
            "password" : None
        }

        def register_email():
            while True:
                email = input("Enter an email: ")
                if email in email_list:
                    print("Email already in use.")
                elif not is_email(email, check_dns=True):
                    print("Invalid email.")
                else:
                    employee_info["email"] = email
                    break

        def register_password():
            while True:
                password = input("Enter a password: ")
                if len(password) < 8:
                    print("Password must be at least 8 characters long.")
                elif re.search('[0-9]',password) is None:
                    print("Password must contain at least one number.")
                elif re.search('[A-Z]',password) is None: 
                    print("Password must contain at least one capital letter.")
                else:
                    employee_info["password"] = password
                    break 
        
        def register_username():
            while True:
                username = input("Enter a username: ")
                if username in username_list:
                    print("Username already taken.")
                else:
                    employee_info["username"] = username
                    break
        
        register_email()
        register_username()
        register_password()

        c.execute("INSERT INTO employees VALUES (:username, :email, :password)",
        {'username' : employee_info["username"], 'email' : employee_info["email"], 'password' : employee_info["password"]})


    def login_employee():
        def change_username():
            while True:
                email = input("Enter email: ")
                if email not in email_list:
                    print("User with this email does not exist.")
                else:
                    c.execute(f"SELECT password FROM employees WHERE email = {email}")
                    break
            while True:
                password = input("Enter password: ")
                if password != c.fetchone()[0]:
                    print("Incorrect password.")
                else:
                    break
            new_username = input("Enter new username: ")
            c.execute(f"UPDATE employees SET username = {new_username} WHERE email = {email}")

        def change_password():
            while True:
                email = input("Enter email: ")
                if email not in email_list:
                    print("User with this email does not exist.")
                else:
                    reset_code = randint(100000, 999999)
                    code_expiration = time.time()
                    server=smtplib.SMTP('smtp.office365.com',587)
                    server.starttls()
                    server.login('peppyspizzeria@outlook.com', 'peppy_pizza_1')
                    msg=MIMEMultipart()
                    msg['From'] = 'peppyspizzeria@outlook.com'
                    msg['Subject'] = "Password Reset Code"
                    msg.attach(MIMEText(f"Your code is {reset_code}",'plain'))
                    msg['To'] = email
                    server.send_message(msg, 'peppyspizzeria@outlook.com', email)
                    server.quit()
                    break
            while True:
                if int(input("Enter code: ")) != reset_code:
                    print("Incorrect code.")
                else:
                    if time.time() - code_expiration > 300:
                        print("Code expired.")
                        break
                    else:
                        new_password = input("Enter new password: ")
                        c.execute("UPDATE employees SET password = :password WHERE email = :email",
                        {'email' : email, 'password' : new_password})
                        print("Password reset successful.")
                        break

        def log_in():
            while True:
                email = input("Enter email: ")
                if email not in email_list:
                    print("User with this email does not exist.")
                else:
                    c.execute(f"SELECT password FROM employees WHERE email = {email}")
                    break
            while True:
                password = input("Enter password: ")
                if password != c.fetchone()[0]:
                    print("Incorrect password.")
                else:
                    break
            return True
        
        choice = input("Would you like to: \n1)Log In\n2)Change Username\n3)Change Password\n")
        if choice == "1":
            log_in()
        elif choice == "2":
            change_username()
        elif choice == "3":
            change_password()

    # register_employee()
    login_employee()