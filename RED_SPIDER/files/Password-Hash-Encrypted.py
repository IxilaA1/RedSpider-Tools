import bcrypt
import hashlib
import base64
import time
import os
from hashlib import pbkdf2_hmac

   # 1. Le logo en texte ASCII généré (exemple)
logo_ascii = """
                                                       j@@@@@^                                 
                           _@v   p@@@@j           j@@@@@@@@@@@@@@@;          |@@@@M   v@}      
                          @@@@@} >@@@@    v@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@p    @@@@_ _@@@@@     
                          >@@@v    @@     v@@@@@@@@@@@@      p@@@@@@@@@@@a     @@    j@@@_     
                           ^@@     @@@@   |@@@@@@@@@@^ @@@@@@; @@@@@@@@@@p   p@@@     M@;      
                           ^@@            >@@@@@@@@@@ p@@@@@@@ M@@@@@@@@@j            M@;      
                           ^@@@@@@@@@@@}   @@@@@@@@|            >@@@@@@@@;   @@@@@@@@@@@;      
                                           }@@@@@@@|    O@@@    >@@@@@@@M                      
                          |@@@@             @@@@@@@|     M@     >@@@@@@@^            @@@@j     
                          @@@@@@@@@@@@@@@>   @@@@@@|    O@@@    >@@@@@@    @@@@@@@@@@@@@@@     
                            ^                 @@@@@v            }@@@@@^                ^       
                                 p@@@@@@@@@^   M@@@@@@@@@@@@@@@@@@@@@    @@@@@@@@@p            
                                 p@_            ^@@@@@@@@@@@@@@@@@@>            >@a            
                                @@@@O              @@@@@@@@@@@@@@              J@@@@           
                               ;@@@@@                 J@@@@@@p                 @@@@@>          
                                  ;              p@              p@>  M@@_       ;             
                                          @@@@p  p@_  ;      j_  a@@@@@@@@j                    
                                         ^@@@@@@@@@   v@_   O@}       M@@_                     
                                            ;         p@|   O@}      }}                        
                                                    >@@@@@  O@@@@@@@@@@@J                      
                                                     p@@@j         ;@@@@^ 
"""

# 2. Nettoyer l'écran avant l'affichage (optionnel, mais propre)
# 'cls' pour Windows, 'clear' pour Linux/macOS
os.system('cls' if os.name == 'nt' else 'clear')

# 3. Afficher le logo
print(logo_ascii)

# 4. Ajouter une petite pause avant le reste du script (optionnel)
time.sleep(2)


# --- PLACEHOLDER/MISSING IMPORTS/HELPER FUNCTIONS (You need to define these for the script to run) ---

# Define placeholders for custom variables and functions used in the original script
WHITE_COLOR = '\033[97m' # Placeholder for 'white' color code
RESET_COLOR = '\033[0m'  # Placeholder for 'reset' color code
BEFORE_PROMPT = '[>>]'  # Placeholder for 'BEFORE' prompt prefix
AFTER_PROMPT = '[<<]'   # Placeholder for 'AFTER' prompt suffix
INPUT_PROMPT = '[?]'    # Placeholder for 'INPUT' icon
ERROR_MSG = '[X]'       # Placeholder for 'ERROR' icon
ADD_MSG = '[+]'         # Placeholder for 'ADD' icon
ENCRYPTED_BANNER = '--- PASSWORD ENCRYPTION TOOL ---' # Placeholder for 'encrypted_banner'

def handle_module_error(e):
    """Handles errors during module import."""
    print(f"Module Import Error: {e}")

def set_title(title):
    """Sets the script's title (e.g., in a terminal window)."""
    print(f"\n--- {title} ---\n") # Simple print for demonstration

def display_slow(text):
    """Displays text slowly."""
    print(text)

def get_current_time_hour():
    """Gets the current time for the prompt prefix."""
    import datetime
    return datetime.datetime.now().strftime("%H:%M")

def handle_invalid_choice():
    """Handles an invalid encryption choice."""
    print(f"{BEFORE_PROMPT}{get_current_time_hour()}{AFTER_PROMPT} {ERROR_MSG} Invalid choice. Please select from 1-6.")
    # In a real script, this might exit or loop back

def wait_for_continue():
    """Waits for user input to continue."""
    input("\nPress Enter to continue...")

def restart_script():
    """Function to reset/restart the main loop (not implemented here)."""
    print("Restarting script...")
    # You'd typically use a loop or call the main function again

def handle_error(e):
    """General error handler."""
    print(f"\n{BEFORE_PROMPT}{get_current_time_hour()}{AFTER_PROMPT} {ERROR_MSG} An unexpected error occurred: {e}")

# --- END OF PLACEHOLDER FUNCTIONS ---

try:
    import bcrypt
    import hashlib
    import base64
    from hashlib import pbkdf2_hmac
except Exception as e:
    handle_module_error(e)

set_title(f"Password Encrypted")
try:
    display_slow(f"""{ENCRYPTED_BANNER}
 {BEFORE_PROMPT}01{AFTER_PROMPT}{WHITE_COLOR} BCRYPT
 {BEFORE_PROMPT}02{AFTER_PROMPT}{WHITE_COLOR} MD5
 {BEFORE_PROMPT}03{AFTER_PROMPT}{WHITE_COLOR} SHA-1
 {BEFORE_PROMPT}04{AFTER_PROMPT}{WHITE_COLOR} SHA-256
 {BEFORE_PROMPT}05{AFTER_PROMPT}{WHITE_COLOR} PBKDF2 (SHA-256)
 {BEFORE_PROMPT}06{AFTER_PROMPT}{WHITE_COLOR} Base64 Encode
    """)

    choice = input(f"{BEFORE_PROMPT + get_current_time_hour() + AFTER_PROMPT} {INPUT_PROMPT} Encryption Method -> {RESET_COLOR}")

    if choice not in ['1', '01', '2', '02', '3', '03', '4', '04', '5', '05', '6', '06']:
        handle_invalid_choice()
        exit() # Added exit to stop execution after error if the original 'ErrorChoice' did so

    password = input(f"{BEFORE_PROMPT + get_current_time_hour() + AFTER_PROMPT} {INPUT_PROMPT} Password to Encrypt -> {WHITE_COLOR}")

    def encrypt_password(choice, password):
        """Encrypts the given password using the selected method."""
        # Note: The PBKDF2 salt is hardcoded for demonstration purposes only.
        # Use a strong, unique, and randomly generated salt in production!
        encrypt_methods = {
            '1': lambda p: bcrypt.hashpw(p.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            '2': lambda p: hashlib.md5(p.encode('utf-8')).hexdigest(),
            '3': lambda p: hashlib.sha1(p.encode('utf-8')).hexdigest(),
            '4': lambda p: hashlib.sha256(p.encode('utf-8')).hexdigest(),
            '5': lambda p: pbkdf2_hmac('sha256', p.encode('utf-8'), "this_is_a_salt".encode('utf-8'), 100000).hex(),
            '6': lambda p: base64.b64encode(p.encode('utf-8')).decode('utf-8')
        }
        
        try:
            # Strips leading zeros from choice (e.g., '01' becomes '1')
            normalized_choice = choice.lstrip('0')
            return encrypt_methods.get(normalized_choice, lambda p: None)(password)
        except Exception as e:
            print(f"{BEFORE_PROMPT + get_current_time_hour() + AFTER_PROMPT} {ERROR_MSG} Error during encryption: {e}")
            return None

    encrypted_password = encrypt_password(choice, password)
    
    if encrypted_password:
        print(f"{BEFORE_PROMPT + get_current_time_hour() + AFTER_PROMPT} {ADD_MSG} Encrypted Password: {WHITE_COLOR}{encrypted_password}{RESET_COLOR}")
        wait_for_continue()
        restart_script()

except Exception as e:
    handle_error(e)