import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS or _MEIPASS2
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_application_path(calling_file):
    """ Get path to the folder containing the executable, works for dev and for PyInstaller """
    # If running as .exe, sys.executable is the full path to the .exe
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    # If running in VS Code, use the current folder
    else:
        # DEV: We find the root by looking for 'main.py' starting from the calling file
        current_path = os.path.abspath(calling_file)
        
        # Loop upwards until we find the folder containing 'main.py'
        while not os.path.exists(os.path.join(os.path.dirname(current_path), "main.py")):
            prev_path = current_path
            current_path = os.path.dirname(current_path)
            # Safety break if we hit the drive root (C:\) without finding main.py
            if current_path == prev_path: 
                return os.path.dirname(os.path.abspath(calling_file))
        
        return os.path.dirname(current_path)