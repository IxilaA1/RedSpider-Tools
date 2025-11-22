import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import sys

# --- Configuration des Couleurs et Apparence ---
ECRAN_BG = "#FF9900"    # Orange Vif du Flipper
ECRAN_TEXT = "#000000"  # Texte Noir
TEXTE_SELECTION = "#FFFFFF" # Texte Blanc pour l'élément sélectionné
POLICE_MENU = ("Fixedsys", 12) 
POLICE_TITRE = ("Fixedsys", 16, "bold") 
TAILLE_FENETRE = "500x300" 

# Chemin vers le dossier des fichiers (juste à côté du script)
FILES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")

# Logo Dauphin ASCII Art
DOLPHIN_LOGO = """
  _   _ 
 /\\_/ \ 
/ o_o  \\
\  .-. /
 '--' 
"""

class FlipperScreenSim:
    def __init__(self, master):
        self.master = master
        
        # --- Variables Personnalisables ---
        self.appareil_titre = "Flipper Sim"
        self.utilisateur_nom = "DefaultUser"
        
        # --- Données du Menu (Catégorie, Nom d'affichage, Nom de fichier à exécuter) ---
        self.menu_items = [
            ("SUB-GHZ", "Analyse", "subghz_config.sub"),
            ("RFID", "Clé Bureau", "rfid_dump.txt"),
            ("NFC", "Carte Bleue", "nfc_data.nfc"),
            ("GPIO", "Run Script", "test_script.py"),
            ("BAD USB", "Keyboard Spam", "badusb_script.txt"),
            ("SYSTÈME", "Afficher Logs", "sys_log.log"),
            ("SYSTÈME", "Quitter", None) # Action interne
        ]
        self.selection_index = 0
        self.en_mode_console = False # Pour gérer l'affichage de la sortie d'exécution

        # --- Configuration de la fenêtre ---
        master.overrideredirect(True)
        master.geometry(TAILLE_FENETRE)
        master.configure(bg=ECRAN_BG)
        
        # Positionnement de la fenêtre (Centrer)
        self._center_window()

        # --- Widgets du Menu Principal ---
        self.frame_menu = tk.Frame(master, bg=ECRAN_BG)
        self.frame_menu.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.labels = []
        self._setup_menu_widgets()

        # --- Widgets de la Console d'Exécution ---
        self.console_text = tk.StringVar(value="")
        self.console_label = tk.Label(master, 
                                     textvariable=self.console_text, 
                                     font=POLICE_MENU, 
                                     bg=ECRAN_TEXT, 
                                     fg=ECRAN_TEXT, # Sera mis à jour
                                     justify=tk.LEFT,
                                     anchor="nw")
        # Ne pas pack la console tout de suite
        
        # --- Gestion des Touches du Clavier ---
        master.bind('<Up>', lambda event: self.naviguer(-1))
        master.bind('<Down>', lambda event: self.naviguer(1))
        master.bind('<Return>', self.action_selectionnee) 
        master.bind('<Right>', self.action_selectionnee) 
        master.bind('<Left>', self.revenir_au_menu)
        master.bind('q', lambda event: self.quitter())

        self.update_affichage()

    def _center_window(self):
        """Centre la fenêtre sur l'écran."""
        master = self.master
        master.update_idletasks()
        width = master.winfo_width()
        height = master.winfo_height()
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        master.geometry(f'+{x}+{y}')

    def _setup_menu_widgets(self):
        """Crée le titre, le logo et les entrées du menu."""
        
        # 1. Zone Titre/Logo
        frame_header = tk.Frame(self.frame_menu, bg=ECRAN_BG)
        frame_header.pack(fill='x', pady=5)
        
        logo_label = tk.Label(frame_header, text=DOLPHIN_LOGO, font=("Courier", 8), bg=ECRAN_BG, fg=ECRAN_TEXT, anchor="w", justify=tk.LEFT)
        logo_label.pack(side=tk.LEFT, padx=10)
        
        title_block = tk.Label(frame_header, 
                               text=f"{self.appareil_titre}\nUtilisateur: {self.utilisateur_nom}", 
                               font=POLICE_TITRE, 
                               bg=ECRAN_BG, 
                               fg=ECRAN_TEXT, 
                               anchor="nw",
                               justify=tk.LEFT)
        title_block.pack(side=tk.LEFT, padx=5)

        # Ligne de séparation
        tk.Frame(self.frame_menu, height=1, bg=ECRAN_TEXT).pack(fill='x', pady=5, padx=5)
        
        # 2. Zone des Éléments de Menu
        for i, (cat, name, file) in enumerate(self.menu_items):
            display_text = f"[{cat.ljust(8)}] {name.ljust(15)} {file if file else ''}"
            label = tk.Label(self.frame_menu, 
                             text=display_text, 
                             font=POLICE_MENU, 
                             bg=ECRAN_BG, 
                             fg=ECRAN_TEXT,
                             anchor="w",
                             height=1)
            label.pack(fill='x', padx=10, pady=1)
            self.labels.append(label)

    def naviguer(self, direction):
        """Déplace la sélection dans le menu."""
        if self.en_mode_console:
            self.update_status("Console active. Appuyez sur Gauche pour revenir.")
            return

        # Enlève le style de l'ancienne sélection
        self.labels[self.selection_index].config(bg=ECRAN_BG, fg=ECRAN_TEXT)
        
        # Calcule le nouvel index
        nouvel_index = (self.selection_index + direction) % len(self.menu_items)
        self.selection_index = nouvel_index
        
        # Met à jour le style de la nouvelle sélection
        self.labels[self.selection_index].config(bg=ECRAN_TEXT, fg=TEXTE_SELECTION)
        
        self.update_status(f"Sélection : {self.menu_items[self.selection_index][1]}")

    def update_affichage(self):
        """Initialise le style d'affichage."""
        if self.labels:
            self.labels[self.selection_index].config(bg=ECRAN_TEXT, fg=TEXTE_SELECTION)
        self.update_status("Menu Prêt. Utilisez les flèches.")

    def action_selectionnee(self, event=None):
        """Gère l'action pour l'élément sélectionné."""
        if self.en_mode_console:
            self.update_status("Console active. Appuyez sur Gauche pour revenir.")
            return

        cat, name, file = self.menu_items[self.selection_index]
        
        if file is None and name == "Quitter":
            self.quitter()
            
        elif file is not None:
            self.executer_fichier(file)
            
        else:
            self.show_message(f"Action non définie pour {name}", 2000)

    def executer_fichier(self, filename):
        """Tente d'exécuter le fichier et affiche la sortie dans la console."""
        filepath = os.path.join(FILES_FOLDER, filename)
        
        # Vérification de l'existence du fichier
        if not os.path.exists(filepath):
            self.show_message(f"Erreur: Fichier introuvable:\n{filename}", 3000)
            return

        # 1. Passer en mode console
        self._toggle_console_mode(True)
        self.console_text.set(f"EXECUTANT: {filename}\n{'='*20}\n")

        try:
            # 2. Déterminer la commande
            extension = os.path.splitext(filename)[1].lower()
            
            if extension == '.py':
                command = [sys.executable, filepath] # Utilise l'interpréteur python actuel
            elif extension in ['.txt', '.log', '.sub', '.nfc']:
                # Lecture simple des fichiers texte/données pour affichage
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                self.console_text.set(self.console_text.get() + content)
                self.console_text.set(self.console_text.get() + f"\n\nFIN DE LECTURE. (Appuyez sur Gauche)")
                return # Sortie pour les fichiers de lecture

            elif extension == '.bat':
                command = [filepath] # Sous Windows
            else:
                # Tentative d'exécution générique (peut échouer si non exécutable)
                command = [filepath] 

            # 3. Exécution avec subprocess
            self.console_text.set(self.console_text.get() + f"Lancement via: {command[0]}\n")
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=5, # Timeout de 5 secondes pour éviter le blocage
                shell=False # Plus sûr et préférable
            )

            # 4. Affichage de la sortie
            output = f"\n[SORTIE]\n{result.stdout}\n[ERREUR]\n{result.stderr}\n"
            if result.returncode != 0:
                output += f"\nErreur: Code {result.returncode}"
            
            self.console_text.set(self.console_text.get() + output)

        except FileNotFoundError:
            self.console_text.set(self.console_text.get() + "\nERREUR: Commande ou Interpréteur non trouvé.")
        except subprocess.TimeoutExpired:
            self.console_text.set(self.console_text.get() + "\nERREUR: L'exécution a expiré (Timeout 5s).")
        except Exception as e:
            self.console_text.set(self.console_text.get() + f"\nERREUR INCONNUE: {e}")
            
        self.console_text.set(self.console_text.get() + "\n\n--- TERMINÉ --- (Appuyez sur Gauche)")

    def _toggle_console_mode(self, activate):
        """Active ou désactive le mode console."""
        self.en_mode_console = activate
        if activate:
            self.frame_menu.pack_forget()
            self.console_label.config(fg=TEXTE_SELECTION) # Texte Blanc
            self.console_label.pack(fill='both', expand=True, padx=10, pady=10)
        else:
            self.console_label.pack_forget()
            self.frame_menu.pack(fill='both', expand=True, padx=5, pady=5)
            self.update_affichage()

    def revenir_au_menu(self, event=None):
        """Revient au menu principal depuis la console."""
        if self.en_mode_console:
            self._toggle_console_mode(False)
            self.update_status("Retour au menu principal.")
        else:
            self.update_status("Vous êtes déjà au menu principal.")


    def show_message(self, message, duration_ms):
        """Affiche un message temporaire pour les erreurs/infos."""
        self._toggle_console_mode(True) # Utiliser la zone console comme popup
        self.console_text.set(message)
        self.console_label.config(fg=ECRAN_TEXT) # Texte Noir pour le popup
        
        self.master.after(duration_ms, lambda: self._toggle_console_mode(False))


    def update_status(self, message):
        """Simule la mise à jour d'un statut en console Python."""
        print(f"[STATUS]: {message}")

    def quitter(self):
        """Quitte l'application proprement."""
        print("[STATUS]: Arrêt du Flipper Sim.")
        self.master.quit()
        sys.exit()

# --- Lancement de l'Application ---
if __name__ == "__main__":
    # S'assurer que le dossier files existe
    if not os.path.exists(FILES_FOLDER):
        os.makedirs(FILES_FOLDER)
        print(f"[INFO]: Dossier 'files' créé à : {FILES_FOLDER}")
        print("[INFO]: Placez-y des scripts ou des fichiers texte pour les tester.")

    root = tk.Tk()
    app = FlipperScreenSim(root)
    root.mainloop()