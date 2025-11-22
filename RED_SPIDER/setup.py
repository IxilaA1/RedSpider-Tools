import sys
import os

# Define the URL links directly in the script
TELEGRAM_URL = 'https://t.me/example_telegram'  # REPLACE WITH THE REAL LINK
GUNSLOL_URL = 'https://www.guns.lol'  # REPLACE WITH THE REAL LINK

def OpenSites():
    """Opens the specified websites in the default browser."""
    try:
        import webbrowser
        print("Opening websites...")
        
        # Open the links defined above
        webbrowser.open(TELEGRAM_URL)
        webbrowser.open(GUNSLOL_URL)
        
    except ImportError:
        # If there's an issue importing 'webbrowser', skip
        print("Warning: The 'webbrowser' module could not be imported. The sites will not be opened.")
    except Exception as e:
        print(f"Error while opening sites: {e}")


def setup_and_run():
    """Executes installation commands and launches the RedTiger tool based on the OS."""
    
    if sys.platform.startswith("win"):
        # Configuration for Windows
        os.system("cls")
        print("Installing the python modules required for the RedTiger Tool:\n")
        
        # Update pip and install dependencies
        os.system("python -m pip install --upgrade pip")
        os.system("python -m pip install -r requirements.txt")
        
        OpenSites()
        
        # Launch the tool
        os.system("python RED_SPIDER.py")

    elif sys.platform.startswith("linux"):
        # Configuration for Linux
        os.system("clear")
        print("Installing the python modules required for the RedTiger Tool:\n")
        
        # Update pip and install dependencies
        os.system("pip3 install --upgrade pip")
        os.system("pip3 install -r requirements.txt")
        
        OpenSites()
        
        # Launch the tool
        os.system("python3 RED_SPIDER.py")
    
    else:
        print(f"Unsupported operating system: {sys.platform}")

# Main entry point of the script
if __name__ == "__main__":
    try:
        setup_and_run()
    except Exception as e:
        # Handles any other critical error that might occur
        input(f"A critical error occurred: {e}\nPress Enter to exit...")