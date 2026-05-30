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

def export_to_csv(company_name, sheet_id):
    import csv
    sheet = connected_sheet(sheet_id)
    worksheets = sheet.worksheets()
    
    root_dir = get_application_path(__file__)
    export_dir = os.path.join(root_dir, 'src', 'sheet', 'csv_exports')
    os.makedirs(export_dir, exist_ok=True)
    
    filename = f"{company_name}-API-BASE - Consolidated.csv"
    filepath = os.path.join(export_dir, filename)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for ws in worksheets:
            # Write start sheet marker
            writer.writerow([f"--- START OF SHEET: {ws.title} ---"])
            
            # Write sheet rows
            rows = ws.get_all_values()
            writer.writerows(rows)
            
            # Write an empty line to match the samples
            writer.writerow([])
            
    return filepath

def send_csv_by_email(company_name, filepaths, recipient_email):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
    smtp_port = os.getenv("EMAIL_SMTP_PORT", "465")
    
    if not sender or not password:
        raise ValueError("EMAIL_SENDER and EMAIL_PASSWORD must be configured in your .env file.")
        
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient_email
    
    if isinstance(filepaths, list) and len(filepaths) > 1:
        msg['Subject'] = "PYTHON EXPORTANDO CSV - TODAS LAS MARCAS"
        brands_str = ", ".join(company_name) if isinstance(company_name, list) else company_name
        body = f"Hola,\n\nAdjunto encontrarás los reportes CSV consolidados para todas las marcas ({brands_str}).\n\nSaludos,\nAutomatización"
    else:
        actual_name = company_name[0] if isinstance(company_name, list) else company_name
        msg['Subject'] = f"PYTHON EXPORTANDO CSV - {actual_name}"
        body = f"Hola,\n\nAdjunto encontrarás el reporte CSV consolidado para {actual_name}.\n\nSaludos,\nAutomatización"
        if isinstance(filepaths, str):
            filepaths = [filepaths]
            
    msg.attach(MIMEText(body, 'plain'))
    
    for filepath in filepaths:
        filename = os.path.basename(filepath)
        with open(filepath, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            msg.attach(part)
            
    # Connect and send
    if smtp_port == "465":
        server = smtplib.SMTP_SSL(smtp_server, int(smtp_port))
    else:
        server = smtplib.SMTP(smtp_server, int(smtp_port))
        server.starttls()
        
    server.login(sender, password)
    server.sendmail(sender, recipient_email, msg.as_string())
    server.quit()

if __name__ == "__main__":
    connected_sheet()

