import requests
import sys
import os
import time
import datetime # Used for the current_time_hour placeholder

   # 1. Le logo en texte ASCII généré (exemple)
logo_ascii = """
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                   >|a@@@@@@@@@|                                                
                                              }@@@@@@@@@@@@@@@@| 000M|                                          
                                          ;@@@@@@O  @@@@@@@@@@@|  j000000_                                      
                                       }@@@@@v   |@@@@@@@@@@@@@| 00J  |00000j                                   
                                     @@@@@_     @@@@@@@@@@@@@@@| 0000    ;00000^                                
                                  ;@@@@v       _@@@@@@@     >@@| 0000v      }0000_                              
                                ^@@@@_         @@@@@@@      ^O@| 00000        ;0000_                            
                                 @@@@;         @@@@@@@      ;p@| 00000         0000^                            
                                   @@@@p       >@@@@@@@^    >@@| 0000v      J0000;                              
                                     O@@@@|     M@@@@@@@@@@@@@@| 0000    >00000                                 
                                       ;@@@@@J^  }@@@@@@@@@@@@@| 00v  j00000}                                   
                                          >@@@@@@@_;@@@@@@@@@@@| ;M000000_                                      
                                              >@@@@@@@@@@@@@@@@| 00000}                                          
                                                   ^jpM@@@@@@@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@| 
"""

# 2. Nettoyer l'écran avant l'affichage (optionnel, mais propre)
# 'cls' pour Windows, 'clear' pour Linux/macOS
os.system('cls' if os.name == 'nt' else 'clear')

# 3. Afficher le logo
print(logo_ascii)

# 4. Ajouter une petite pause avant le reste du script (optionnel)
time.sleep(2)

# --- Custom/Placeholder Definitions ---
# IMPORTANT: Replace these placeholders with your actual function/variable definitions 
# (e.g., from a separate 'custom_modules' file or a 'colorama' setup).

class Colors:
    RESET = '\033[0m'
    WHITE = '\033[97m'
    RED = '\033[91m'

# Placeholders for custom functions/variables
BEFORE = "[ "
AFTER = " ]"
INFO = "INFO"
WAIT = "WAIT"
INPUT_PROMPT = "INPUT"
INFO_ADD = "INFO"
white = Colors.WHITE
red = Colors.RED
reset = Colors.RESET
color = Colors() # Instance for color.RESET

def current_time_hour():
    return datetime.datetime.now().strftime("%H:%M:%S")

def ErrorModule(e):
    # Function to handle module-related errors
    print(f"Module Error: {e}")

def Title(title_text):
    # Function to display a title
    print(f"\n--- {title_text} ---\n")

def ChoiceUserAgent():
    # Placeholder: Should return a random User-Agent string
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"

def ErrorUsername():
    # Function to handle username not found/API lookup errors
    print(f"{BEFORE}{current_time_hour()}{AFTER} ERROR: Username not found or an API error occurred.")

def Error(e):
    # Function to handle general exceptions
    print(f"{BEFORE}{current_time_hour()}{AFTER} GENERAL ERROR: {e}")

def Continue():
    # Function to wait for user input
    input("\nPress Enter to continue...")

def Reset():
    # Function for script cleanup/reset if needed
    print("\n--- Process Finished ---\n")

# --------------------------------------

Title("Roblox User Info")

try:
    # --- Setup ---
    user_agent = ChoiceUserAgent()
    headers = {"User-Agent": user_agent}

    print(f"\n{BEFORE}{current_time_hour()}{AFTER} {INFO} Selected User-Agent: {white}{user_agent}{color.RESET}")
    
    # Prompt the user for the Roblox username
    username_input = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT_PROMPT} Enter Username -> {color.RESET}")
    
    print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} Information Retrieval In Progress...{reset}")

    # --- API Request 1: Get User ID from Username ---
    try:
        # Request to resolve username to user ID
        lookup_response = requests.post(
            "https://users.roblox.com/v1/usernames/users",
            headers=headers,
            json={
                "usernames": [username_input],
                "excludeBannedUsers": True
            }
        )
        
        lookup_response.raise_for_status() # Check for HTTP errors (4xx/5xx)
        
        lookup_data = lookup_response.json()

        # Check if user data was returned
        if not lookup_data.get('data'):
            ErrorUsername()
            # FIX: Use sys.exit() to stop script execution when username is not found
            sys.exit() 
            
        user_id = lookup_data['data'][0]['id']

        # --- API Request 2: Get detailed User Info from User ID ---
        info_response = requests.get(f"https://users.roblox.com/v1/users/{user_id}", headers=headers)
        
        info_response.raise_for_status() # Check for HTTP errors (4xx/5xx)
        
        user_api_data = info_response.json()

        # --- Data Extraction ---
        userid = user_api_data.get('id', "N/A")
        display_name = user_api_data.get('displayName', "N/A")
        username = user_api_data.get('name', "N/A")
        # Replace newlines in description for clean display
        description = user_api_data.get('description', "N/A").replace('\n', ' ') 
        created_at = user_api_data.get('created', "N/A")
        is_banned = user_api_data.get('isBanned', "N/A")
        external_app_display_name = user_api_data.get('externalAppDisplayName', "N/A")
        has_verified_badge = user_api_data.get('hasVerifiedBadge', "N/A")

        # --- Output ---
        print(f"""
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} Username           : {white}{username}{red}
 {INFO_ADD} User ID            : {white}{userid}{red}
 {INFO_ADD} Display Name       : {white}{display_name}{red}
 {INFO_ADD} Description        : {white}{description}{red}
 {INFO_ADD} Created At         : {white}{created_at}{red}
 {INFO_ADD} Banned             : {white}{is_banned}{red}
 {INFO_ADD} External App Name  : {white}{external_app_display_name}{red}
 {INFO_ADD} Verified Badge     : {white}{has_verified_badge}{red}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        """)
        
        Continue()
        Reset()
        
    # Catch specific API/Lookup errors
    except requests.exceptions.RequestException as req_e:
        print(f"{BEFORE}{current_time_hour()}{AFTER} API ERROR: {req_e}")
        ErrorUsername() 
    except KeyError:
        # Handles cases where data structure is unexpected (e.g., 'data' missing)
        ErrorUsername() 

# Catch all other general errors
except Exception as e:
    Error(e)