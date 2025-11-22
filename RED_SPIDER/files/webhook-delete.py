import requests
import time
import sys
import os # Useful for setting console title on some systems

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


# --- PLACEHOLDER FUNCTIONS AND VARIABLES ---
# YOU MUST REPLACE THESE WITH YOUR ACTUAL IMPLEMENTATIONS!

class Color:
    """A placeholder class for text color constants."""
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    
color = Color()
BEFORE = f"[{color.YELLOW}Time{color.RESET}] "
AFTER = ""
INPUT = f"[{color.GREEN}INPUT{color.RESET}]"
INFO = f"[{color.GREEN}INFO{color.RESET}]"
ERROR = f"[{color.RED}ERROR{color.RESET}]"

def current_time_hour():
    """Placeholder for getting the current time in HH:MM:SS format."""
    return time.strftime("%H:%M:%S")

def Title(text):
    """Placeholder function to set the console title or print a banner."""
    if os.name == 'nt': # Windows
        os.system(f"title {text}")
    print(f"\n{color.YELLOW}--- {text} ---{color.RESET}")

def CheckWebhook(url):
    """
    Placeholder function to validate if the URL is a correct webhook format.
    Replace 'True' with your actual validation logic.
    """
    if "discord.com/api/webhooks" in url:
        return True
    return False

def ErrorWebhook():
    """Placeholder function to handle and display a webhook error message."""
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid Webhook URL or deletion failed (e.g., 404 Not Found).")
    Continue()

def Continue():
    """Placeholder function to prompt the user to continue."""
    input(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Press ENTER to continue...{color.RESET}")

def Reset():
    """Placeholder function to exit the script (assuming 'Reset' means end/exit)."""
    sys.exit()

def Error(e):
    """Placeholder function to handle and display a general exception."""
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} An unexpected error occurred: {e}{color.RESET}")
    sys.exit()
    
# --- MAIN SCRIPT LOGIC ---

Title("Discord Webhook Delete")

try:
    # 1. Get the Webhook URL from the user
    webhook_url = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook URL -> {color.RESET}")
    
    # 2. Validate the URL format
    if CheckWebhook(webhook_url) == False:
        ErrorWebhook() 
        
    else:
        # 3. Attempt to delete the webhook
        try:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Attempting to delete webhook...")
            
            response = requests.delete(webhook_url)
            response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
            
            # 4. Success
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Webhook successfully Deleted.")
            Continue() 
            Reset() 
            
        except requests.exceptions.RequestException as e:
            # Catches errors specific to the request (e.g., connection error, timeout, HTTP 404/400)
            ErrorWebhook() # Handles deletion failures (e.g., 404 Not Found, 400 Bad Request)
            
except Exception as e:
    # Catches general errors (e.g., issues with custom functions)
    Error(e)