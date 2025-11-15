import sys # For clean exit on error
import phonenumbers
import time
import os
from phonenumbers import geocoder, carrier, timezone

   # 1. Le logo en texte ASCII généré (exemple)
logo_ascii = """
                                          ...:----:...                                              
                                     .:=#@@@@@@@@@@@@@@%*-..                                        
                                  .:#@@@@@@@%#*****#%@@@@@@@+..                                     
                               ..-@@@@@%-...... ........+@@@@@@..                                   
                               :%@@@@=..   .#@@@@@@@@#=....+@@@@*.                                  
                             .+@@@@=.      .*@@@%@@@@@@@@=...*@@@@:.                                
                            .#@@@%.                 .=@@@@@=. .@@@@-.                               
                           .=@@@#.                    .:%@@@*. -@@@%:.                              
                           .%@@@-                       .*@@*. .+@@@=.                              
                           :@@@#.                              .-@@@#.                              
                           -@@@#                                :%@@@.                              
                           :@@@#.                              .-@@@#.                              
                           .%@@@-.                             .+@@@=.                              
                           .+@@@#.                             -@@@%:.                              
                            .*@@@%.                          .:@@@@-.                               
                             .+@@@@=..                     ..*@@@@:.                                
                               :%@@@@-..                ...+@@@@*.                                  
                               ..-@@@@@%=...         ...*@@@@@@@@#.                                 
                                  .:*@@@@@@@%*++++**@@@@@@@@=:*@@@@#:.                              
                                     ..=%@@@@@@@@@@@@@@%#-.   ..*@@@@%:.                            
                                        .....:::::::....       ...+@@@@%:                           
                                                                  ..+@@@@%-.                        
                                                                    ..=@@@@%-.                      
                                                                      ..=@@@@@=.                    
                                                                         .=%@@@@=.                  
                                                                          ..-%@@@-.                 
                                                                             ....
"""

# 2. Nettoyer l'écran avant l'affichage (optionnel, mais propre)
# 'cls' pour Windows, 'clear' pour Linux/macOS
os.system('cls' if os.name == 'nt' else 'clear')

# 3. Afficher le logo
print(logo_ascii)

# 4. Ajouter une petite pause avant le reste du script (optionnel)
time.sleep(2)

# --- Placeholder Functions and Constants (Adjust if you have your own utility functions) ---
# NOTE: The original script used many external variables (BEFORE, INPUT, Title(), Slow(), etc.).
# These have been replaced with basic functions and strings to make the script standalone and executable.

def Title(text):
    print(f"\n--- {text} ---")

def Slow(text):
    print(text)

def Continue():
    input("\nPress ENTER to continue...")

def Reset():
    print("\n" + "="*70)

def Error(e):
    print(f"\n[FATAL ERROR] {e}")
    sys.exit(1)

def ErrorModule(e):
    print(f"\n[IMPORT ERROR] The 'phonenumbers' module may be missing: {e}")
    sys.exit(1)

# Style variables (simplified for the example)
BEFORE = "[>]"
AFTER = ""
INPUT = "[?]"
WAIT = "[...]"
INFO = "[!]"
INFO_ADD = "[*]"
# Using basic string for color reset
color = type('color', (object,), {'RESET': '\033[0m'})
reset = color.RESET
white = ""
red = ""

# A simple function to simulate current_time_hour()
def current_time_hour():
    import datetime
    return datetime.datetime.now().strftime("%H:%M:%S")
# -----------------------------------------------------------------------------------------


Title("Phone Number Lookup")

try:
    # Prompt the user for the number, encouraging international format (+CC...)
    phone_number = input(f"\n{BEFORE}{current_time_hour()}{AFTER} {INPUT} Phone Number (e.g., +442071234567) -> {color.RESET}")
    print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} Retrieving Information...{reset}")

    # The second argument to parse() is the default region (can be None or 'US', 'FR', etc.)
    # We set it to None to require the user to input the full international number.
    try:
        # Attempt to parse the number
        parsed_number = phonenumbers.parse(phone_number, None)
    except Exception as e:
        # Error if the format is so incorrect it cannot be parsed at all
        print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} Invalid Format or missing number! ({e})")
        Continue()
        Reset()
        sys.exit(0) # Exit the script if parsing fails

    if parsed_number:
        # --- Information Retrieval ---
        status = "Valid" if phonenumbers.is_valid_number(parsed_number) else "Invalid"
        
        # Get the country code using the parsed object, which is more reliable
        country_code = f"+{parsed_number.country_code}" if parsed_number.country_code else "Not Specified"
        
        # Get the region code from the number itself (e.g., 'GB', 'US', 'FR')
        region_code = phonenumbers.region_code_for_number(parsed_number)

        # Try to retrieve details, falling back to 'N/A' on error or if not found
        try: operator = carrier.name_for_number(parsed_number, "en") or "N/A"
        except: operator = "Error"
        
        # Use the PhoneNumberType object directly for comparison
        try: 
            num_type = phonenumbers.number_type(parsed_number)
            if num_type == phonenumbers.PhoneNumberType.MOBILE:
                type_number = "Mobile"
            elif num_type == phonenumbers.PhoneNumberType.FIXED_LINE:
                type_number = "Fixed Line"
            elif num_type == phonenumbers.PhoneNumberType.VOIP:
                type_number = "VoIP"
            else:
                type_number = "Other"
        except: type_number = "Error"

        try:
            timezones = timezone.time_zones_for_number(parsed_number)
            timezone_info = ", ".join(timezones) if timezones else "N/A"
        except: timezone_info = "Error"
        
        try: 
            # Use geocoder to get the location description
            country_description = geocoder.description_for_number(parsed_number, "en") or "N/A"
        except: country_description = "Error"
            
        try: formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        except: formatted_number = "Error"


        # --- Display Results ---
        Slow(f"""
{white}──────────────────────────────────────────────────────────────────────
 {INFO_ADD} Entered Number : {white}{phone_number}{red}
 {INFO_ADD} E.164 Format   : {white}{formatted_number}{red}
 {INFO_ADD} Status         : {white}{status}{red}
 {INFO_ADD} Country Code   : {white}{country_code}{red}
 {INFO_ADD} Country/Region : {white}{country_description} ({region_code}){red}
 {INFO_ADD} Operator       : {white}{operator}{red}
 {INFO_ADD} Number Type    : {white}{type_number}{red}
 {INFO_ADD} Timezone(s)    : {white}{timezone_info}{red}
{white}──────────────────────────────────────────────────────────────────────
""")
        Continue()
        Reset()

except Exception as e:
    Error(e)