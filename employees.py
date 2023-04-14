from pyisemail import is_email
import re
import sqlite3

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


    def login_employee(email, password):
        pass

    register_employee()