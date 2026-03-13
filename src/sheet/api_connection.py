import gspread
from google.oauth2.service_account import Credentials
import os

def connected_sheet(sheet_id):
    SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
    SHEET_ID = sheet_id

    CREDS_FILE = os.path.join(os.path.dirname(__file__ ), 'credentials.json')

    # Autenticación
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPE)
    client = gspread.authorize(creds)

    #Seleccionar sheet Worksheet para trabajar
    wsheet = client.open_by_key(SHEET_ID)

    return wsheet

if __name__ == "__main__":
    connected_sheet()