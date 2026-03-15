import gspread
from google.oauth2.service_account import Credentials
import os
from src.utils.config_handlers import get_application_path

def connected_sheet(sheet_id):
    SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
    SHEET_ID = sheet_id

    # CREDS_FILE = os.path.join(os.path.dirname(__file__ ), 'credentials.json')
    # 1. Get the path to your installation directory
    root_dir = get_application_path(__file__)
    CREDS_FILE = os.path.join(root_dir, 'src', 'sheet', 'credentials.json')

    # Autenticación
    if not os.path.exists(CREDS_FILE):
        raise FileNotFoundError(f"No se encontró el archivo de credenciales en: {CREDS_FILE}")
    
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPE)
    client = gspread.authorize(creds)

    #Seleccionar sheet Worksheet para trabajar
    wsheet = client.open_by_key(SHEET_ID)

    return wsheet

if __name__ == "__main__":
    connected_sheet()