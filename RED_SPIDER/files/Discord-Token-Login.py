import sys
import time
from selenium import webdriver
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


# Définir ou simuler toutes les fonctions et variables utilisées dans le script
def ErrorModule(e): print(f"ErrorModule: {e}")
def Title(text): print(f"=== {text} ===")
def Slow(text): time.sleep(1)  # Simuler un affichage lent
def Choice1TokenDiscord():
    # Pour l'exemple, demander à l'utilisateur d'entrer un token
    return input("Enter your Discord token: ")
def current_time_hour():
    return time.strftime("%H:%M:%S")
def Continue():
    input("Press Enter to continue...")
def Reset():
    print("Resetting session...")
    # Fermer le navigateur si ouvert
    global driver
    try:
        driver.quit()
    except:
        pass
def ErrorChoice():
    print("Invalid choice, please select a valid option.")
def OnlyLinux():
    print("This option is only available on Windows.")
def white(): return "\033[97m"
def blue(): return "\033[94m"
def red(): return "\033[91m"
def green(): return "\033[92m"
def current_time_hour():
    return time.strftime("%H:%M:%S")
# Variables de style
BEFORE = ""
AFTER = ""
INPUT = ""
reset = ""
blue_str = blue()

# Début du script
try:
    # Afficher le titre
    Title("Discord Token Login")
    
    # Simuler la bannière
    def discord_banner():
        print("Welcome to Discord Token Login Tool")
    Slow(discord_banner)
    
    # Obtenir le token
    token = Choice1TokenDiscord()
    
    # Afficher les options de navigateur
    print(f"""
 {BEFORE}01{AFTER}{white()} Chrome (Windows / Linux)
 {BEFORE}02{AFTER}{white()} Edge (Windows)
 {BEFORE}03{AFTER}{white()} Firefox (Windows)
    """)
    
    # Demander à l'utilisateur de choisir un navigateur
    browser = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Browser -> {reset}")

    # Initialiser le WebDriver selon le choix
    if browser in ['1', '01']:
        try:
            navigator = "Chrome"
            print(f"{BEFORE + current_time_hour() + AFTER} {blue_str} {navigator} Starting...{blue_str}")
            driver = webdriver.Chrome()
            print(f"{BEFORE + current_time_hour() + AFTER} {green()} {navigator} is ready!{blue_str}")
        except:
            print(f"{BEFORE + current_time_hour() + AFTER} {red()} {navigator} not installed or driver not up to date.")
            Continue()
            Reset()

    elif browser in ['2', '02']:
        if sys.platform.startswith("linux"):
            OnlyLinux()
        else:
            try:
                navigator = "Edge"
                print(f"{BEFORE + current_time_hour() + AFTER} {blue_str} {navigator} Starting...{blue_str}")
                driver = webdriver.Edge()
                print(f"{BEFORE + current_time_hour() + AFTER} {green()} {navigator} is ready!{blue_str}")
            except:
                print(f"{BEFORE + current_time_hour() + AFTER} {red()} {navigator} not installed or driver not up to date.")
                Continue()
                Reset()

    elif browser in ['3', '03']:
        if sys.platform.startswith("linux"):
            OnlyLinux()
        else:
            try:
                navigator = "Firefox"
                print(f"{BEFORE + current_time_hour() + AFTER} {blue_str} {navigator} Starting...{blue_str}")
                driver = webdriver.Firefox()
                print(f"{BEFORE + current_time_hour() + AFTER} {green()} {navigator} is ready!{blue_str}")
            except:
                print(f"{BEFORE + current_time_hour() + AFTER} {red()} {navigator} not installed or driver not up to date.")
                Continue()
                Reset()
    else:
        ErrorChoice()

    # Script pour injecter dans Discord
    script = """
        function login(token) {
            setInterval(() => {
                document.body.appendChild(document.createElement('iframe')).contentWindow.localStorage.token = `"${token}"`;
            }, 50);
            setTimeout(() => {
                location.reload();
            }, 2500);
        }
    """

    # Accéder à Discord
    driver.get("https://discord.com/login")
    print(f"{BEFORE + current_time_hour() + AFTER} {blue_str} Connecting with token...{blue_str}")

    # Exécuter le script pour se connecter avec le token
    driver.execute_script(script + f'\nlogin("{token}")')
    time.sleep(4)  # Attendre la connexion

    print(f"{BEFORE + current_time_hour() + AFTER} {green()} Token connected successfully!{blue_str}")
    print(f"{BEFORE + current_time_hour() + AFTER} {green()} Warning: Closing the browser will end the session.{blue_str}")

    # Continuer ou terminer
    Continue()

    # Fermeture du driver
    Reset()

except Exception as e:
    ErrorModule(e)