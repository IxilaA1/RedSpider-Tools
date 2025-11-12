# -*- coding: utf-8 -*-
import subprocess
import shlex
import time
import sys

def type_text(text, delay=0.03):
    """Displays text with a character-by-character typing effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush() # Force immediate character display
        time.sleep(delay)
    # For prompts (input), we don't add a newline here
    

def lookup_url_ipinfo():
    """
    Prompts for a URL, executes 'curl ipinfo.io/<url>' to find its geographic info, and pauses.
    All done with a fast typing animation.
    """
    # 1. Typing animation for the URL input prompt
    prompt_text = "Enter the URL to look up (e.g., www.google.com): "
    type_text(prompt_text, delay=0.03)
    
    # Get the URL input
    url_address = input()
    
    # *** KEY CHANGE: The command uses ipinfo.io with the provided URL ***
    # ipinfo.io will attempt to resolve the URL to an IP and return its data.
    command = f"curl ipinfo.io/{url_address}"

    # Do not print the command here
    
    type_text("-" * 50 + "\n", delay=0.01) # Very fast separator line

    try:
        # 2. Typing animation for the waiting message
        type_text(f"Attempting to resolve IP info for: {url_address}...\n", delay=0.04) 
        time.sleep(0.4) # Short pause before execution for effect

        # Executes the command to get IP data from the URL
        # We add '-s' to suppress the progress meter from curl.
        subprocess.run(shlex.split(f"curl -s {url_address}"), check=True)
    
    except subprocess.CalledProcessError as e:
        type_text(f"\nError executing curl or retrieving info: {e}\n", delay=0.03)
    except FileNotFoundError:
        type_text("\nError: 'curl' command not found. Ensure it is installed and in your PATH.\n", delay=0.03)
    except Exception as e:
        type_text(f"\nAn unexpected error occurred: {e}\n", delay=0.03)

    type_text("-" * 50 + "\n", delay=0.01) # Very fast separator line
    
    # 3. Typing animation for the exit pause
    try:
        type_text("Press ENTER to exit...", delay=0.03)
        input()
    except EOFError:
        pass

if __name__ == "__main__":
    lookup_url_ipinfo()