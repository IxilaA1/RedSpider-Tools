import sys
import os
import webbrowser

# Liens directs
TELEGRAM_URL = ""
GUNSLOL_URL = ""

def open_sites():
    try:
        webbrowser.open(TELEGRAM_URL)
        webbrowser.open(GUNSLOL_URL)
    except Exception:
        pass

def clear_screen():
    os.system("cls" if sys.platform.startswith("win") else "clear")

def main():
    try:
        # Se déplacer dans le dossier du script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        clear_screen()
        print(f"Working directory: {script_dir}\n")
        print("Installing the python modules required for the RedTiger Tool:\n")
        
        if sys.platform.startswith("win"):
            os.system("python -m pip install --upgrade pip")
            os.system("python -m pip install -r requirements.txt")
            open_sites()
            os.system("python RED_SPIDER.py")
        
        elif sys.platform.startswith("linux"):
            os.system("pip3 install --upgrade pip")
            os.system("pip3 install -r requirements.txt")
            open_sites()
            os.system("python3 RED_SPIDER.py")
        
        else:
            print(f"Unsupported platform: {sys.platform}")
    
    except Exception as e:
        input(f"Error: {e}")

if __name__ == "__main__":
    main()
