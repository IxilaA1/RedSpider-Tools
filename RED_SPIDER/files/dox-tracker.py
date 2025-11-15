import webbrowser
import time
import os # Ajout pour la fonction Slow

    # 1. Le logo en texte ASCII généré (exemple)
logo_ascii = """
                                                         .+#%@@%#+.                                     
                                                    .#@@@@@@@@@@@@@@@@#.                                
                                                  +@@@@@@@@@@@@@@@@@@@@@@*                              
                                                .%@@@@@@@@@@@@@@@@@@@@@@@@%.                            
                                                %@@@@@@@@@@@@@@@@@@@@@@@@@@%                            

                                               %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                          
                                                -..........................-.                           
                                                %@@@@@@00@@@@@@@@@@@%@@@@@@%                            
                                                %@@@#     .%@@@@%.     *@@@%                            
                                                . :+00+--+%@#::#@%*--+00+: .                            
                                                                           .                            
                                                 :                        :                             
                                                  -                      =                              
                                                    -                  -                                
                                                       -=          --                                   
                                               -+#%@@@@@@=        =@@@@@@%#+-                           
                                            *@@@@@@@@@@@@=        =@@@@@@@@@@@@*                        
                                          *@@@@@@@@@@@@@@+        +@@@@@@@@@@@@@@#                      
                                         *@@@@@@@@@@@@@@@@%=    -%@@@@@@@@@@@@@@@@#                     
                                        -@@@@@@@@@@@@@@@@@@@%#*0@@@@@@@@@@@@@@@@@@@-                    
                                        -@@@@@@@@@@@@@@@@@@@%::%@@@@@@@@@@@@@@@@@@@-                    
                                        -@@@@@@@@@@@@@@@@@@@%::%@@@@@@@@@@@@@@@@@@@-                    
                                        -@@@@@@@@@@@@@@@@@@@%::%@@@@@@@@@@@@@@@@@@@-

"""

# 2. Nettoyer l'écran avant l'affichage (optionnel, mais propre)
# 'cls' pour Windows, 'clear' pour Linux/macOS
os.system('cls' if os.name == 'nt' else 'clear')

# 3. Afficher le logo
print(logo_ascii)

# 4. Ajouter une petite pause avant le reste du script (optionnel)
time.sleep(2)

# Définitions simulées pour que le code puisse s'exécuter
def ErrorModule(e):
    print(f"[ERREUR MODULE] {e}")

def Title(text):
    print(f"======== {text} ========")

def Slow(text):
    # Simule un affichage lent
    print(text)
    time.sleep(0.5)

def current_time_hour():
    # Simule l'heure actuelle
    return time.strftime("%H:%M")

def Censored(text):
    # Simule un message de censure/vérification
    print(f"[CENSURE] Recherche '{text}' acceptée.")

def Reset():
    # Simule un retour au menu principal
    print("[RESET] Retour au menu principal (Sortie ici pour la simulation).")
    exit()

def ErrorChoice():
    # Simule une erreur de choix
    print("[ERREUR CHOIX] Choix non valide.")

def Error(e):
    print(f"[ERREUR GLOBALE] Une erreur s'est produite : {e}")

# Variables de style simulées
dox_banner = "--- Dox Tracker v1.0 ---"
BEFORE = "["
AFTER = "]"
white = "" # Couleur blanche
INPUT = ">>>"
reset = "" # Réinitialisation de couleur
color = type('obj', (object,), {'RESET' : ""})

# Le code principal commence ici
try:
    Slow(f"""{dox_banner}
{BEFORE}00{AFTER} Retour
{BEFORE}01{AFTER}{white} Nom d'utilisateur
{BEFORE}02{AFTER}{white} Nom, Prénom
{BEFORE}03{AFTER}{white} Autre
    """)

    search_type = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Type de recherche -> {reset}")

    if search_type in ['00', '0']:
        Reset() # Quitte le programme dans la simulation

    if search_type in ['01', '1']:
        search = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Nom d'utilisateur -> {reset}")
        Censored(search)
            
    elif search_type in ['02', '2']:
        name = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Nom de famille -> {reset}")
        first_name = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Prénom -> {reset}")
        Censored(name)
        Censored(first_name)
        
    elif search_type in ['03', '3']:
        search = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Recherche -> {reset}")
        Censored(search)
    else:
        ErrorChoice()

    # Si un type de recherche valide a été sélectionné
    if search_type in ['1', '01','2','02','3','03']:
        print(f"""
{BEFORE}00{AFTER} Retour
{BEFORE}01{AFTER}{white} Facebook.com
{BEFORE}02{AFTER}{white} Youtube.com
{BEFORE}03{AFTER}{white} Twitter.com
{BEFORE}04{AFTER}{white} Tiktok.com
{BEFORE}05{AFTER}{white} Peekyou.com
{BEFORE}06{AFTER}{white} Tumblr.com
{BEFORE}07{AFTER}{white} PagesJaunes.fr
        """)
        
        while True:
            
            if search_type in ['1', '01','2','02','3','03']:
                choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Site -> {color.RESET}")

                if choice in ['0', '00']:
                    break # Sort de la boucle de sélection de site

                # Logique pour ouvrir le navigateur
                base_url = ""
                query = ""
                
                # Détermine la requête basée sur le type de recherche
                if search_type in ['01', '1', '3', '03']:
                    # Recherche par Nom d'utilisateur ou Autre
                    query = search
                elif search_type in ['02', '2']:
                    # Recherche par Nom, Prénom
                    if choice == '05' or choice == '5': # Peekyou utilise underscore
                         query = f"{name}_{first_name}"
                    elif choice == '07' or choice == '7': # PagesJaunes utilise un espace simple
                        query = f"{name} {first_name}"
                    else: # La plupart utilisent %20 ou +
                        query = f"{name}%20{first_name}" # Utilisation de %20 pour l'URL

                # Détermine l'URL de base et construit l'URL complète
                if choice in ['01', '1']:
                    base_url = "https://www.facebook.com/search/top/?init=quick&q="
                elif choice in ['02', '2']:
                    base_url = "https://www.youtube.com/results?search_query="
                elif choice in ['03', '3']:
                    base_url = "https://twitter.com/search?f=users&vertical=default&q="
                elif choice in ['04', '4']:
                    base_url = "https://www.tiktok.com/search?q="
                elif choice in ['05', '5']:
                    base_url = "https://www.peekyou.com/" # Pas de ?q= pour peekyou
                elif choice in ['06', '6']:
                    base_url = "https://www.tumblr.com/search/"
                elif choice in ['07', '7']:
                    base_url = "https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui="
                
                # Ouvrir le navigateur
                if base_url:
                    full_url = f"{base_url}{query}"
                    print(f"Ouverture de : {full_url}")
                    webbrowser.open(full_url)
                else:
                    ErrorChoice() # Si le choix n'est pas un site reconnu

except Exception as e:
    Error(e)