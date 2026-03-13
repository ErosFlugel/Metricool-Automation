
import tkinter as tk

# Modules
from src.menu_ui.automation_app import AutomationApp
from src.metricool.actions_2 import create_report_2
# from src.metricool.api_requests import get_charts_metadata

# Get chart info for further updates and changes
# get_charts_metadata("INSERT THE SHEET ID HERE")

root = tk.Tk()

# Add actions as properties
actions = {
    'create_report': create_report_2
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