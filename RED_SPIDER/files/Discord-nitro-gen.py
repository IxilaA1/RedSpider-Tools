import random
import string
import json
import requests
import threading
import time
import sys
import os # For clean error handling

# --- Configuration (These must be defined for the script to run) ---
# Replace these with actual values or logic from the original environment
# Setting placeholders for undefined custom variables:
BEFORE = "[INFO]"
AFTER = ""
INPUT = ">"
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
WHITE = "\033[97m"
BEFORE_GREEN = f"{GREEN}[SUCCESS]{RESET}"
AFTER_GREEN = ""
GEN_VALID = "VALID"
GEN_INVALID = "INVALID"
COLOR_WEBHOOK = 0x5865F2 # Discord Embed Color (blue)
USERNAME_WEBHOOK = "Nitro Checker"
AVATAR_WEBHOOK = "https://i.imgur.com/your-avatar.png" # Replace with a suitable image URL

    # 1. Le logo en texte ASCII généré (exemple)
logo_ascii = """
                                              @@@@                @%@@                                      
                                       @@@@@@@@@@@@               @@@@@@@@@@%                               
                                  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                          
                                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                         
                                %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                        
                               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                       
                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                      
                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                     
                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                    
                           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                   
                          %@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@%                  
                          %@@@@@@@@@@@@@@@@        %@@@@@@@@@@@%@        @@@@@@@@@@@@@@@@@                  
                          %@@@@@@@@@@@@@@@          @@@@@@@@@@@@          @@@@@@@@@@@@@@@%                  
                         %@@@@@@@@@@@@@@@@          @@@@@@@@@@@%          %@@@@@@@@@@@@@@@@                 
                         @@@@@@@@@@@@@@@@@%         @@@@@@@@@@@%         %@@@@@@@@@@@@@@@@@                 
                         @@@@@@@@@@@@@@@@@@@      %@@@@@@@@@@@@@@@      @@@@@@@@@@@@@@@@@@%                 
                         %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                 
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                 
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                 
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                 
                           @%@@@@@@@@@@@@@%@@   @@@@%@@@@@@@@@%%%@%@@  @@@@@@@@@@@@@@@@@@                   
                              @@%@@@@@@@@@@@@@                        @%@@@@@@@@@@@%@@                      
                                   @%@@@@@@@                            @@@@@@%%@                           
                                         @@                              @@             

"""

# 2. Nettoyer l'écran avant l'affichage (optionnel, mais propre)
# 'cls' pour Windows, 'clear' pour Linux/macOS
os.system('cls' if os.name == 'nt' else 'clear')

# 3. Afficher le logo
print(logo_ascii)

# 4. Ajouter une petite pause avant le reste du script (optionnel)
time.sleep(2)

def current_time_hour():
    """Placeholder for custom time function."""
    return time.strftime("%H:%M:%S")

def set_title(title):
    """Placeholder for custom title function."""
    print(f"--- {title} ---")

def display_banner():
    """Placeholder for custom slow banner function."""
    print("Discord Nitro Generator/Checker Initialized.")

def error_message(e):
    """Standardized error display."""
    print(f"\n{RED}### FATAL ERROR ###{RESET}")
    print(f"Error: {e}")
    sys.exit(1)

def error_number():
    """Error for invalid thread number input."""
    print(f"{RED}[ERROR]{RESET} Invalid number of threads entered. Exiting.")
    sys.exit(1)

def check_webhook(url):
    """Placeholder for custom webhook check function."""
    print(f"[INFO] Checking Webhook URL: {url}...")
    # Add actual webhook validation logic here if needed
    
# --- Main Script Logic ---

try:
    set_title("Discord Nitro Generator")

    display_banner()
    
    webhook_enabled = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Webhook? (y/n) -> {RESET}").lower()
    
    webhook_url = None
    if webhook_enabled in ['y', 'yes']:
        webhook_url = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Webhook URL -> {RESET}")
        check_webhook(webhook_url)

    try:
        threads_number = int(input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Threads Number -> {RESET}"))
    except ValueError:
        error_number()

    def send_webhook(url_nitro):
        """Sends a notification to the specified Discord webhook."""
        if not webhook_url:
            return

        payload = {
            'embeds': [{
                'title': 'Nitro Valid!',
                'description': f"**Nitro:**\n```{url_nitro}```",
                'color': COLOR_WEBHOOK,
                'footer': {
                    "text": USERNAME_WEBHOOK,
                    "icon_url": AVATAR_WEBHOOK,
                }
            }],
            'username': USERNAME_WEBHOOK,
            'avatar_url': AVATAR_WEBHOOK
        }

        headers = {
            'Content-Type': 'application/json'
        }

        try:
            requests.post(webhook_url, data=json.dumps(payload), headers=headers, timeout=5)
        except requests.exceptions.RequestException as e:
            print(f"{RED}[WEBHOOK ERROR]{RESET} Failed to send webhook: {e}")

    def nitro_check():
        """Generates a code and checks its validity against Discord's API."""
        # Discord Nitro codes are 16 alphanumeric characters
        CODE_LENGTH = 16
        code_nitro = ''.join(random.choices(string.ascii_letters + string.digits, k=CODE_LENGTH))
        url_nitro = f'https://discord.gift/{code_nitro}'
        
        # NOTE: This API endpoint is known to be rate-limited or disabled
        API_ENDPOINT = f'https://discordapp.com/api/v6/entitlements/gift-codes/{code_nitro}?with_application=false&with_subscription_plan=true'
        
        try:
            response = requests.get(API_ENDPOINT, timeout=5) # Increased timeout for stability
            
            if response.status_code == 200:
                if webhook_enabled in ['y', 'yes']:
                    send_webhook(url_nitro)
                
                print(f"{BEFORE_GREEN}{current_time_hour()}{AFTER_GREEN} {GEN_VALID} Status: {WHITE}Valid{GREEN} Nitro: {WHITE}{url_nitro}{RESET}")
            else:
                # 404 (Not Found) usually means invalid/expired
                print(f"{BEFORE}{current_time_hour()}{AFTER} {GEN_INVALID} Status: {WHITE}Invalid{RED} Nitro: {WHITE}{url_nitro}{RESET}")
        
        except requests.exceptions.Timeout:
            print(f"{RED}[TIMEOUT]{RESET} API Request Timed Out for: {url_nitro}")
        except requests.exceptions.RequestException as e:
             # Handle other request-related errors (e.g., DNS, connection refused)
             print(f"{RED}[REQUEST ERROR]{RESET} An error occurred: {e}")


    def start_threads():
        """Creates and starts the worker threads."""
        threads = []
        try:
            for _ in range(threads_number):
                t = threading.Thread(target=nitro_check)
                t.start()
                threads.append(t)
        except Exception as e:
            # Catch errors during thread creation/start
            error_message(f"Error during thread creation: {e}")

        for thread in threads:
            # Wait for all threads to complete (this only happens if 'nitro_check' finishes)
            thread.join()

    # The original script uses a 'while True' loop around 'request()',
    # which means it runs the threads, waits for them to finish, and then restarts.
    # For a checker, it often means the process is continuous.
    print(f"\n{GREEN}[STARTING]{RESET} Beginning check loop with {threads_number} threads...")
    while True:
        start_threads()
        
except Exception as e:
    # Catch any major exceptions in the main execution block
    error_message(e)