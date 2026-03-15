import tkinter as tk
import sys
import os

# Priority to external src folder:
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

if application_path not in sys.path:
    sys.path.insert(0, application_path)

# Ensure the external sheet_data.py is loaded instead of the bundled one
if getattr(sys, 'frozen', False):
    import importlib.util
    external_sheet_data = os.path.join(application_path, 'src', 'sheet', 'sheet_data.py')
    if os.path.exists(external_sheet_data):
        spec = importlib.util.spec_from_file_location("src.sheet.sheet_data", external_sheet_data)
        if spec is not None and spec.loader is not None:
            module = importlib.util.module_from_spec(spec)
            sys.modules["src.sheet.sheet_data"] = module
            spec.loader.exec_module(module)

# Modules
from src.menu_ui.automation_app import AutomationApp
from src.metricool.actions import create_report

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