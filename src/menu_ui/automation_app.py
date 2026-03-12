import tkinter as tk
from tkinter import ttk
from datetime import datetime
from dotenv import load_dotenv
import os
import threading
import traceback

from src.metricool.sheet_data import companies, spanish_months

# Load environment variables from .env file
load_dotenv()

class AutomationApp:
    def __init__(self, root, actions):
        self.root = root
        self.root.title("Automatización con Python")
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f2f5')

         # Colors
        self.header_bg = "#2c3e50"
        self.text_dark = "#2c3e50"
        self.text_light = "#7f8c8d"
        self.button_green = "#2ecc71"
        self.white = "#ffffff"
        self.error_red = "#e74c3c"
        self.success_green = "#27ae60"

        # actions
        self.actions = actions
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.header_bg, height=60)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        
        # Current date in Header left
        current_date = datetime.now().strftime("%d/%m/%Y")
        date_label = tk.Label(header, 
                                   text=current_date, 
                                   font=('Segoe UI', 12, "bold"),
                                   fg=self.white,
                                   bg=self.header_bg)
        date_label.pack(side='left', padx=20)
        
        # Settings Icon in top right
        settings_btn = tk.Label(header,
                                        text="⚙",
                                        font=('Segoe UI', 18),
                                        bg='#3498db',
                                        fg=self.white,
                                        padx=10,
                                        pady=5,
                                        cursor='hand2')
        settings_btn.pack(side='right', padx=20)
        
        # --- Main Content ---
        main_container = tk.Frame(self.root, bg=self.white)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(main_container,
                              text="Automatización con Python",
                              font=('Segoe UI', 28, 'bold'),
                              fg=self.text_dark,
                              bg=self.white)
        title_label.pack(pady=(50, 10))

        # Description
        desc_label = tk.Label(main_container,
                             text="Selecciona el mes que quieres registrar",
                             font=('Segoe UI', 14),
                             fg=self.text_light,
                             bg=self.white)
        desc_label.pack(pady=(0, 40))

        options_container = tk.Frame(main_container, bg=self.white)
        options_container.pack(fill='both', expand=True)

        # Combobox (companies dropdown)

        self.companies = companies

        self.company_var = tk.StringVar()
        self.company_combo = ttk.Combobox(
            options_container, 
            textvariable=self.company_var, 
            values=self.companies, 
            state="readonly",
            width=20,
            font=("Segoe UI", 12)
        )
        self.company_combo.set(self.companies[0]) # Default to first option
        self.company_combo.pack( pady=20, padx=20)


        # Combobox (Months dropdown)
        self.months = spanish_months

        self.month_var = tk.StringVar()
        self.month_combo = ttk.Combobox(
            options_container, 
            textvariable=self.month_var, 
            values=self.months, 
            state="readonly",
            width=20,
            font=("Segoe UI", 12)
        )
        self.month_combo.set(self.months[datetime.now().month - 2]) # Default to Previous month
        self.month_combo.pack( pady=20, padx=20)


        # Generate Report Button

        self.generate_btn = tk.Button(main_container,
                                    text="Generar Reporte",
                                    command=self.start_report_thread,
                                    bg=self.button_green,
                                    fg=self.white,
                                    font=('Segoe UI', 16, 'bold'),
                                    relief='flat',
                                    padx=30,
                                    pady=15,
                                    activebackground='#27ae60',
                                    activeforeground=self.white,
                                    cursor='hand2')
        self.generate_btn.pack(pady=20)

         # --- Footer / Status Bar ---
        footer_frame = tk.Frame(self.root, bg="#f0f2f5")
        footer_frame.pack(side="bottom", fill="x", padx=20, pady=10)

        # Status label (Bottom Left)
        self.status_label = tk.Label(
            footer_frame, 
            text="Viendo: Página Principal", 
            bg="#f0f2f5", 
            fg=self.text_light, 
            font=("Segoe UI", 9)
        )
        self.status_label.pack(side="left")

        # Progress bar (Hidden by default)
        self.progress = ttk.Progressbar(
            footer_frame, 
            orient="horizontal", 
            length=150, 
            mode="indeterminate"
        )
    
    def update_status(self, message, color=None):
        """Update the status label text and color"""
        if color is None:
            color = self.text_light
        self.status_label.config(text=message, fg=color)

    def start_report_thread(self):
        """Start the report generation in a separate thread to keep UI responsive"""
        # Disable button and show loading state
        self.generate_btn.config(state="disabled")
        self.update_status("Procesando datos... Por favor espere", self.text_dark)
        self.progress.pack(side="left", padx=10)
        self.progress.start(10)
        
        # Run the actual work in a background thread
        thread = threading.Thread(target=self.generate_report)
        thread.daemon = True
        thread.start()

    def generate_report(self):
        """Handle report generation logic"""
        try:
            selected_month_number = {"name": self.month_var.get(), "number": self.months.index(self.month_var.get()) + 1}
            blog_id = {"name": self.company_var.get(), "code": os.getenv(f"BLOG_ID_{self.company_var.get()}")}

            # Execute the action provided in the constructor
            self.actions['create_report'](selected_month_number, blog_id)
            
            # If successful, update UI (must use root.after for thread safety)
            self.root.after(0, lambda: self.on_report_complete(True, "✓ Reporte generado exitosamente"))
            
        except Exception as e:
            # If failed, update UI with error
            error_msg = f"✗ Error: {str(e)}"
            self.root.after(0, lambda: self.on_report_complete(False, error_msg))
            traceback.print_exc()
            print(e)

    def on_report_complete(self, success, message):
        """Clean up UI after report generation finishes"""
        self.progress.stop()
        self.progress.pack_forget()
        self.generate_btn.config(state="normal")
        
        color = self.success_green if success else self.error_red
        self.update_status(message, color)
        
        # Reset status to default after 5 seconds
        self.root.after(5000, lambda: self.update_status("Viendo: Página Principal"))