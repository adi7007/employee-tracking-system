
from PyQt5 import QtWidgets
import sys
from logger import log_event

REASONS = ["Tea", "Lunch", "Washroom", "Other"]

def show_break_reason_popup():
    app = QtWidgets.QApplication(sys.argv)
    reason, ok = QtWidgets.QInputDialog.getItem(None, "Break Reason", "Why were you away?", REASONS, 0, False)
    if ok and reason:
        log_event('Reason', reason)

