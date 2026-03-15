import tkinter as tk
import sys
import os

# Modules
from src.menu_ui.automation_app import AutomationApp
from src.metricool.actions import create_report

# Priority to external src folder:
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

if application_path not in sys.path:
    sys.path.insert(0, application_path)

# Get chart info for further updates and changes
# get_charts_metadata("INSERT THE SHEET ID HERE")

root = tk.Tk()

# Add actions as properties
actions = {
    'create_report': create_report
}

app = AutomationApp(root, actions)

# Center window on screen
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')

root.mainloop()