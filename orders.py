import sqlite3
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

def create_order():
    name = input("Enter customer name: ")
    email = input("Enter customer email: ")
    number = input("Enter customer phone number: ")
    date = datetime.datetime.now()
    conn = sqlite3.connect('C:/Users/stefan/Desktop/Programiranje/restaurant_orders_app/orders.db',
                             detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute("SELECT id FROM orders ORDER BY id DESC;")
    id = c.fetchone()[0] + 1
    c.execute("INSERT INTO orders VALUES (:id, :customer_name, :customer_email, :customer_phone_number, :order_sent, :order_datetime)",
    {'id' : id, 'customer_name' : name, 'customer_email' : email, 'customer_phone_number' : number, 'order_sent' : 0, 'order_datetime' : date})
    conn.commit()
    c.close()
    conn.close()

def send_order():
    order_id = int(input("Enter order id: "))
    conn = sqlite3.connect('C:/Users/stefan/Desktop/Programiranje/restaurant_orders_app/orders.db',
                             detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute(f"SELECT order_sent FROM orders WHERE id = {order_id}")
    if c.fetchone()[0] == True:
        print("Order already sent.")
    else:
        c.execute(f"SELECT customer_email FROM orders WHERE id = {order_id}")
        email = c.fetchone()[0]
        server=smtplib.SMTP('smtp.office365.com',587)
        server.starttls()
        server.login('peppyspizzeria@outlook.com', 'peppy_pizza_1')
        msg=MIMEMultipart()
        msg['From'] = 'peppyspizzeria@outlook.com'
        msg['Subject'] = "Peppy's Pizzeria Order"
        msg.attach(MIMEText("Your order has been sent.",'plain'))
        msg['To'] = email
        server.send_message(msg, 'peppyspizzeria@outlook.com', email)
        server.quit()
        c.execute(f"UPDATE orders SET order_sent = 1 WHERE id = {order_id}")
    conn.commit()
    c.close()
    conn.close()
    print("Order sent and customer notified.")
        
def cancel_order():
    pass

send_order()