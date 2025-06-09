
import smtplib
from email.message import EmailMessage
import sqlite3

def send_report():
    conn = sqlite3.connect("idle_logs.db")
    c = conn.cursor()
    c.execute("SELECT * FROM logs")
    logs = c.fetchall()

    msg = EmailMessage()
    msg.set_content("\n".join(str(log) for log in logs))
    msg["Subject"] = "Weekly Idle Report"
    msg["From"] = "sender@example.com"
    msg["To"] = "admin@example.com"

    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login("sender@example.com", "your_password")
        server.send_message(msg)
