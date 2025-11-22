import sys
import os

def setup_and_run():
    """Exécute les commandes d'installation et lance l'outil RedTiger selon le système d'exploitation."""
    
    # -------------------------------------------------------------------------
    # NOTE: La fonction OpenSites et les imports de liens ont été supprimés.
    # -------------------------------------------------------------------------

    if sys.platform.startswith("win"):
        # Configuration pour Windows
        os.system("cls")
        print("Installation des modules python requis pour l'outil RedTiger:\n")
        
        # Mise à jour de pip et installation des dépendances
        os.system("python -m pip install --upgrade pip")
        os.system("python -m pip install -r requirements.txt")
        
        # Lancement de l'outil
        print("\nLancement de RedTiger.py...")
        os.system("python RedTiger.py")

    elif sys.platform.startswith("linux"):
        # Configuration pour Linux
        os.system("clear")
        print("Installation des modules python requis pour l'outil RedTiger:\n")
        
        # Mise à jour de pip et installation des dépendances
        os.system("pip3 install --upgrade pip")
        os.system("pip3 install -r requirements.txt")
        
        # Lancement de l'outil
        print("\nLancement de RedTiger.py...")
        os.system("python3 RedTiger.py")
    
    else:
        print(f"Système d'exploitation non pris en charge: {sys.platform}")

# Point d'entrée principal du script
if __name__ == "__main__":
    try:
        setup_and_run()
    except Exception as e:
        # Gère toute autre erreur critique
        input(f"Une erreur critique est survenue: {e}\nAppuyez sur Entrée pour quitter...")