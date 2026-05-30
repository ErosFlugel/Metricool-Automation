import tkinter as tk
from tkinter import ttk
from datetime import datetime
from dotenv import load_dotenv
import os
import threading
import traceback

from src.sheet.sheet_data import profile_specs, spanish_months
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