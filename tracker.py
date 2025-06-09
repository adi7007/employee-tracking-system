from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
import sys
import ctypes
from ctypes import Structure, c_uint, POINTER, sizeof, byref
from logger import log_event
from ui import show_break_reason_popup

IDLE_THRESHOLD = 10  # seconds

class LASTINPUTINFO(Structure):
    _fields_ = [('cbSize', c_uint), ('dwTime', c_uint)]

def get_idle_duration():
    lii = LASTINPUTINFO()
    lii.cbSize = sizeof(LASTINPUTINFO)
    if ctypes.windll.user32.GetLastInputInfo(byref(lii)):
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0
    else:
        return 0

class IdleApp(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.idle_timer = QTimer()
        self.idle_timer.timeout.connect(self.check_idle)
        self.idle_timer.start(5000)  # check every 5 seconds
        self.was_idle = False

    def check_idle(self):
        idle = get_idle_duration()
        if idle > IDLE_THRESHOLD and not self.was_idle:
            print("[DEBUG] Idle detected")
            log_event("Idle")
            self.was_idle = True
        elif idle < 5 and self.was_idle:
            print("[DEBUG] User back, showing popup")
            log_event("Unlock")
            show_break_reason_popup()
            self.was_idle = False

def start_tracking():
    app = IdleApp(sys.argv)
    sys.exit(app.exec_())
