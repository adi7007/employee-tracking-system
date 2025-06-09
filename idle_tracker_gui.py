import tkinter as tk
from tkinter import simpledialog
import csv
import os
import ctypes
import time
import threading
import psutil
from datetime import datetime
from config import IDLE_TIMEOUT

LOG_FILE_CSV = os.path.join(os.path.dirname(__file__), "idle_log_data.csv")
BREAK_REASONS = ["Lunch", "Washroom", "Tea", "Other"]

# Initialize CSV if it doesn't exist
if not os.path.exists(LOG_FILE_CSV):
    with open(LOG_FILE_CSV, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "EventType", "Duration", "Reason"])

def log_to_csv(event_type, duration="", reason=""):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE_CSV, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, event_type, duration, reason])
            file.flush()
            os.fsync(file.fileno())
    except Exception as e:
        print(f"[ERROR] Failed to log event: {e}")

def get_idle_duration():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0
    return 0

def is_screen_locked():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'LogonUI.exe':
            return True
    return False

def prompt_reason(app=None):
    if app is None:
        app = tk.Tk()
        app.withdraw()
        reason = simpledialog.askstring("Break Reason", "Why were you away? (Lunch, Washroom, Tea, Other)")
        app.destroy()
    else:
        from PyQt5 import QtWidgets
        reason, ok = QtWidgets.QInputDialog.getItem(None, "Break Reason", "Why were you away?", BREAK_REASONS, 0, False)
        if ok and reason:
            return reason
        reason = "Other"
    if reason not in BREAK_REASONS:
        reason = "Other"
    return reason

def monitor():
    last_state = "active"
    idle_start = None
    lock_start = None

    while True:
        idle_time = get_idle_duration()
        locked = is_screen_locked()

        # Idle detection
        if idle_time >= IDLE_TIMEOUT and last_state == "active":
            idle_start = datetime.now()
            log_to_csv("idle_start")
            last_state = "idle"

        elif idle_time < 5 and last_state == "idle":
            idle_end = datetime.now()
            duration = str(idle_end - idle_start).split('.')[0] if idle_start else ""
            log_to_csv("idle_end", duration=duration)
            last_state = "active"

        # Lock detection
        if locked and last_state != "locked":
            lock_start = datetime.now()
            log_to_csv("lock")
            last_state = "locked"

        elif not locked and last_state == "locked":
            lock_end = datetime.now()
            duration = str(lock_end - lock_start).split('.')[0] if lock_start else ""
            reason = prompt_reason()
            log_to_csv("unlock", duration=duration, reason=reason)
            last_state = "active"

        time.sleep(5)

# Start monitoring in background thread
threading.Thread(target=monitor, daemon=True).start()

# Run a dummy GUI loop to keep app alive
app = tk.Tk()
app.title("Idle Tracker")
label = tk.Label(app, text="Idle Tracker Running in Background")
label.pack(padx=20, pady=20)
app.mainloop()
