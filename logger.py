import sqlite3
import datetime
import os

# Use local AppData or same folder as the executable
db_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(db_dir, "idle_logs.db")

# Ensure the path is writable and the file can be created
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS logs
             (event_type TEXT, timestamp TEXT, duration REAL, reason TEXT)''')
conn.commit()

def log_event(event_type, reason=None):
    timestamp = datetime.datetime.now().isoformat()
    c.execute("INSERT INTO logs VALUES (?, ?, ?, ?)", (event_type, timestamp, 0, reason))
    conn.commit()
