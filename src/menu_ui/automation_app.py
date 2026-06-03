import tkinter as tk
from tkinter import ttk
from datetime import datetime
from dotenv import load_dotenv
import os
import threading
import traceback

from src.sheet.sheet_data import profile_specs, spanish_months
from src.sheet.api_connection import export_to_csv, send_csv_by_email
from src.utils.config_handlers import  get_application_path

# Load environment variables from .env file
root_dir = get_application_path(__file__)
env_path = os.path.join(root_dir, ".env")
load_dotenv(dotenv_path=env_path)

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
        
        # Platform Colors
        self.fb_blue = "#1877f2"
        self.yt_red = "#ff0000"
        self.tt_black = "#010101"
        self.ig_pink = "#e1306c"

        # State
        self.current_platform = "Instagram"
        self.pages = {}
        self.platform_widgets = {}
        self.is_exporting = False
        
        # Export mode: "email" (Send by email) or "local" (Save locally)
        self.export_mode = "email"

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

        # Initialize common data
        self.companies = list(map(lambda comp: comp.get("name"), profile_specs))
        self.months = spanish_months
        
        # Settings Icon in top right
        self.settings_btn = tk.Label(header,
                                        text="⚙",
                                        font=('Segoe UI', 18),
                                        bg='#3498db',
                                        fg=self.white,
                                        padx=10,
                                        pady=5,
                                        cursor='hand2')
        self.settings_btn.pack(side='right', padx=20)
        self.settings_btn.bind("<Button-1>", self.show_platform_menu)
        
        # Hover effect for Settings Icon
        self.settings_btn.bind("<Enter>", lambda e: self.settings_btn.config(bg='#2980b9'))
        self.settings_btn.bind("<Leave>", lambda e: self.settings_btn.config(bg='#3498db'))

        # Export CSV Button (placed to the left of the settings icon)
        button_text = "📧 Enviar por Email" if self.export_mode == "email" else "📥 Exportar CSV"
        self.export_btn = tk.Label(header,
                                   text=button_text,
                                   font=('Segoe UI', 12, 'bold'),
                                   bg=self.button_green,
                                   fg=self.white,
                                   padx=15,
                                   pady=5,
                                   cursor='hand2')
        self.export_btn.pack(side='right', padx=(0, 10))
        self.export_btn.bind("<Button-1>", lambda e: self.start_export_thread())
        
        # Hover effects for Export CSV Button
        self.export_btn.bind("<Enter>", lambda e: self.export_btn.config(bg='#27ae60') if not self.is_exporting else None)
        self.export_btn.bind("<Leave>", lambda e: self.export_btn.config(bg=self.button_green) if not self.is_exporting else None)
        
        # --- Main Content Container ---
        self.main_container = tk.Frame(self.root, bg=self.white)
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)

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
        
        # Create Pages
        self.create_pages()
        
        # Initial Page
        self.show_page("Instagram")
    
    def create_pages(self):
        """Initialize frames for each platform"""
        platforms = [
            ("Instagram", self.button_green),
            ("Facebook", self.fb_blue),
            ("YouTube", self.yt_red),
            ("TikTok", self.tt_black)
        ]
        
        for platform, color in platforms:
            page_frame = tk.Frame(self.main_container, bg=self.white)
            self.pages[platform] = page_frame
            self.setup_platform_content(page_frame, platform, color)

    def setup_platform_content(self, parent, platform, color):
        """Setup unified UI for any platform"""
        # Title
        title_label = tk.Label(parent,
                              text=f"Automatización {platform}",
                              font=('Segoe UI', 28, 'bold'),
                              fg=color,
                              bg=self.white)
        title_label.pack(pady=(50, 10))

        # Description
        desc_label = tk.Label(parent,
                             text=f"Selecciona el mes que quieres registrar para {platform}",
                             font=('Segoe UI', 14),
                             fg=self.text_light,
                             bg=self.white)
        desc_label.pack(pady=(0, 40))

        options_container = tk.Frame(parent, bg=self.white)
        options_container.pack(fill='both', expand=True)

        # Combobox (companies dropdown)
        company_var = tk.StringVar()
        company_combo = ttk.Combobox(
            options_container, 
            textvariable=company_var, 
            values=self.companies, 
            state="readonly",
            width=20,
            font=("Segoe UI", 12)
        )
        company_combo.set(self.companies[0])
        company_combo.pack(pady=20, padx=20)

        # Combobox (Months dropdown)
        month_var = tk.StringVar()
        month_combo = ttk.Combobox(
            options_container, 
            textvariable=month_var, 
            values=self.months, 
            state="readonly",
            width=20,
            font=("Segoe UI", 12)
        )
        month_combo.set(self.months[datetime.now().month - 2])
        month_combo.pack(pady=20, padx=20)

        # Generate Report Button
        def on_click():
            if platform == "Instagram":
                self.start_report_thread()
            else:
                print(f"{platform} automation not implemented yet")
                self.update_status(f"✓ {platform} UI funcionando", color)

        generate_btn = tk.Button(parent,
                                    text=f"Generar Reporte {platform}",
                                    command=on_click,
                                    bg=color,
                                    fg=self.white,
                                    font=('Segoe UI', 16, 'bold'),
                                    relief='flat',
                                    padx=30,
                                    pady=15,
                                    activebackground=color, # Could be slightly darker
                                    activeforeground=self.white,
                                    cursor='hand2')
        generate_btn.pack(pady=20)

        # Store widgets for later access
        self.platform_widgets[platform] = {
            'company_var': company_var,
            'month_var': month_var,
            'generate_btn': generate_btn
        }

    def show_page(self, platform_name):
        """Switch the visible platform page"""
        for page in self.pages.values():
            page.pack_forget()
        
        self.pages[platform_name].pack(fill='both', expand=True)
        self.current_platform = platform_name
        self.update_status(f"Viendo: Automatización {platform_name}")

    def show_platform_menu(self, event):
        """Show a popup menu to select platform"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Instagram", command=lambda: self.show_page("Instagram"))
        menu.add_command(label="Facebook", command=lambda: self.show_page("Facebook"))
        menu.add_command(label="YouTube", command=lambda: self.show_page("YouTube"))
        menu.add_command(label="TikTok", command=lambda: self.show_page("TikTok"))
        menu.post(event.x_root, event.y_root)

    def update_status(self, message, color=None):
        """Update the status label text and color"""
        if color is None:
            color = self.text_light
        self.status_label.config(text=message, fg=color)

    def start_report_thread(self):
        """Start the report generation in a separate thread to keep UI responsive"""
        # Disable button and show loading state
        platform = self.current_platform
        btn = self.platform_widgets[platform]['generate_btn']
        
        btn.config(state="disabled")
        self.update_status(f"Procesando {platform}... Por favor espere", self.text_dark)
        self.progress.pack(side="left", padx=10)
        self.progress.start(10)
        
        # Run the actual work in a background thread
        thread = threading.Thread(target=self.generate_report)
        thread.daemon = True
        thread.start()

    def generate_report(self):
        """Handle report generation logic"""
        try:
            platform = "Instagram" # Hardcoded for now as per user's current logic
            widgets = self.platform_widgets[platform]
            month_val = widgets['month_var'].get()
            company_val = widgets['company_var'].get()

            selected_month_number = {"name": month_val, "number": self.months.index(month_val) + 1}
            blog_id = {"name": company_val, "code": os.getenv(f"BLOG_ID_{company_val}"), "sheet-id": [comp.get("id") for comp in profile_specs if comp.get("name") == company_val][0]}

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
        
        platform = "Instagram"
        btn = self.platform_widgets[platform]['generate_btn']
        btn.config(state="normal")
        
        color = self.success_green if success else self.error_red
        self.update_status(message, color)
        
        # Reset status to default after 5 seconds
        self.root.after(5000, lambda: self.update_status(f"Viendo: Automatización {self.current_platform}"))

    def start_export_thread(self):
        """Start the CSV export process in a separate background thread"""
        if self.is_exporting:
            return
            
        company_val = self.platform_widgets[self.current_platform]['company_var'].get()
        month_val = self.platform_widgets[self.current_platform]['month_var'].get()
        
        # Open the selection modal dialog
        dialog = ExportOptionDialog(self.root, company_val, self.export_mode)
        selection = dialog.result
        
        if selection is None:
            return # Cancelled
            
        self.is_exporting = True
        self.export_btn.config(state="disabled", bg='#95a5a6')  # Disabled gray color
        
        if selection == "all":
            # Export all active brands (excluding TESTING-SHEET-TOYOTA)
            brands = [comp.get("name") for comp in profile_specs if comp.get("name") != "TESTING-SHEET-TOYOTA"]
            action_verb = "Enviando" if self.export_mode == "email" else "Exportando"
            self.update_status(f"{action_verb} todas las marcas (6)... Por favor espere", self.text_dark)
        else:
            # Export only current brand
            brands = [company_val]
            action_verb = "Enviando" if self.export_mode == "email" else "Exportando"
            action_noun = "por email" if self.export_mode == "email" else "a CSV"
            self.update_status(f"{action_verb} CSV de {company_val} {action_noun}... Por favor espere", self.text_dark)
        
        self.progress.pack(side="left", padx=10)
        self.progress.start(10)
        
        thread = threading.Thread(target=self.export_csv_data, args=(brands, selection == "all", month_val))
        thread.daemon = True
        thread.start()

    def export_csv_data(self, brands, is_all_mode, month_val):
        """Perform the CSV export in the background"""
        try:
            filepaths = []
            
            # Export each selected brand
            for brand in brands:
                sheet_id = [comp.get("id") for comp in profile_specs if comp.get("name") == brand][0]
                filepath = export_to_csv(brand, sheet_id, month_val)
                filepaths.append(filepath)
            
            if self.export_mode == "email":
                # Send the generated CSV by email
                recipient = os.getenv("EMAIL_RECIPIENT")
                send_csv_by_email(brands, filepaths, recipient)
                if is_all_mode:
                    msg = f"✓ Reportes de todas las marcas enviados a {recipient} exitosamente"
                else:
                    msg = f"✓ CSV de {brands[0]} enviado a {recipient} exitosamente"
            else:
                if is_all_mode:
                    msg = f"✓ Reportes de todas las marcas ({len(brands)}) exportados exitosamente"
                else:
                    msg = f"✓ CSV de {brands[0]} exportado exitosamente"
            
            # On success
            self.root.after(0, lambda: self.on_export_complete(True, msg))
            
        except Exception as e:
            # On error
            action_name = "enviar" if self.export_mode == "email" else "exportar"
            error_msg = f"✗ Error al {action_name} CSV: {str(e)}"
            self.root.after(0, lambda: self.on_export_complete(False, error_msg))
            traceback.print_exc()

    def on_export_complete(self, success, message):
        """Clean up UI after CSV export finishes"""
        self.progress.stop()
        self.progress.pack_forget()
        
        self.is_exporting = False
        self.export_btn.config(state="normal", bg=self.button_green)
        
        color = self.success_green if success else self.error_red
        self.update_status(message, color)
        
        # Reset status to default after 5 seconds
        self.root.after(5000, lambda: self.update_status(f"Viendo: Automatización {self.current_platform}"))


class ExportOptionDialog(tk.Toplevel):
    def __init__(self, parent, current_brand, export_mode):
        super().__init__(parent)
        self.title("Opción de Exportación")
        self.geometry("450x220")
        self.configure(bg='#f0f2f5')
        self.resizable(False, False)
        
        # Center in parent
        self.transient(parent)
        self.grab_set()
        
        # Style tokens
        bg_color = '#f0f2f5'
        card_bg = '#ffffff'
        text_color = '#2c3e50'
        btn_blue = '#3498db'
        btn_green = '#2ecc71'
        btn_gray = '#95a5a6'
        
        # Main container card
        card = tk.Frame(self, bg=card_bg, padx=20, pady=20)
        card.pack(fill='both', expand=True, padx=15, pady=15)
        
        action_verb = "enviar por email" if export_mode == "email" else "exportar a CSV"
        label_text = f"¿Qué deseas {action_verb}?"
        
        title_label = tk.Label(card, text=label_text, font=('Segoe UI', 14, 'bold'), fg=text_color, bg=card_bg)
        title_label.pack(pady=(0, 15))
        
        self.result = None # Stores "current", "all", or None
        
        # Button frame
        btn_frame = tk.Frame(card, bg=card_bg)
        btn_frame.pack(fill='x', pady=10)
        
        # Button 1: Current brand
        btn1_text = f"Solo {current_brand}"
        btn1 = tk.Button(btn_frame, text=btn1_text, font=('Segoe UI', 11, 'bold'), bg=btn_blue, fg='white',
                         activebackground='#2980b9', activeforeground='white', relief='flat', padx=10, pady=8,
                         cursor='hand2', command=self.on_current)
        btn1.pack(side='left', expand=True, fill='x', padx=5)
        
        # Button 2: All brands
        btn2_text = "Todas las Marcas (6)"
        btn2 = tk.Button(btn_frame, text=btn2_text, font=('Segoe UI', 11, 'bold'), bg=btn_green, fg='white',
                         activebackground='#27ae60', activeforeground='white', relief='flat', padx=10, pady=8,
                         cursor='hand2', command=self.on_all)
        btn2.pack(side='left', expand=True, fill='x', padx=5)
        
        # Button 3: Cancel
        btn3 = tk.Button(btn_frame, text="Cancelar", font=('Segoe UI', 11), bg=btn_gray, fg='white',
                         activebackground='#7f8c8d', activeforeground='white', relief='flat', padx=10, pady=8,
                         cursor='hand2', command=self.on_cancel)
        btn3.pack(side='left', expand=True, fill='x', padx=5)
        
        # Center window relative to parent
        parent.update_idletasks()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        
        x = parent_x + (parent_w - 450) // 2
        y = parent_y + (parent_h - 220) // 2
        self.geometry(f"450x220+{x}+{y}")
        
        self.wait_window()

    def on_current(self):
        self.result = "current"
        self.destroy()
        
    def on_all(self):
        self.result = "all"
        self.destroy()
        
    def on_cancel(self):
        self.result = None
        self.destroy()