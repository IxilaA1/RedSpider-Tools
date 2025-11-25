# -*- coding: utf-8 -*-
# We keep this encoding line to prevent errors if the user's input contains special characters.

import requests
import time
import os
import sys
import ipaddress # New module for robust IP validation
from requests.exceptions import ConnectionError, Timeout, HTTPError

   # 1. Le logo en texte ASCII généré (exemple)
logo_ascii = """
                                      :**+ :::+*@@.                                                         
                              +: @ = =.  :#@@@@@@@@                 :     .=*@@#     -                      
                 @@@@-. :=: +@@.:% *=@@:   @@@@@@          :#=::     .:@=@@@@@@@@@@@@@@@@@@@@--.-:          
             .#@@@@@@@@@@@@@@@@@@:# .@@   #@@    :@-     +@@:@@@+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*        
             #*   :%@@@@@@@@@@:   .@@#*              ..  ##@ *#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-:- %=         
                   *@@@@@@@@@@@@%@@@@@@@            = @=+@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+   #.        
                   #@@@@@@@@@##@@@@@= =#              #@@@#@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=            
                  @@@@@@@@@@@#+#@@=                 :@@@-.#-*#@.  .@@.=%@@@@%@@@@@@@@@@@@@@@@@=  +          
                 :@@@@@@@@@@@@@@:                   :@@    # - @@@@@@@ =@@@*#*@@@@@@@@@@@@@=.=-  #:         
                  :@@@@@@@@@@@+                     @@@@@@@: :    @@@@@@@@@@@@@@@@@@@@@@@@@@@               
                   #@@@@@    @                     #%@@@@@@@@@@@@@@@@@:@@@@@@@@@@@@#@@@@@@@@@:              
                     @@@     .                    @@@@@@@@@@@@@@@@-%@@@%@#   @@@@@@#=@#@@@@@==              
                     =@@##@   =:*.                @@@@@@*@@@@@@@@@@-=@@@@.    +@@@:  %#@@#=   :             
                         .=@.                     #@@@@@@@@#@@@@@@@@+#:        %@      *%@=                 
                            . @@@@@@               @#@@*@@@@@@@@@@@@@@@=        :-     -       =.           
                             :@@@@@@@#=                   @@@@@@@@@@@@-               :+%  .@=              
                            -@@@@@@@@@@@@                 @+@@@@*+@@#                   @. @@.#   # :       
                             @@@@@@@@@@@@@@@               @@@@@*@@@                     :=.        @@@.    
                              @@@@@@@@@@@@@                #@@@@@@%@.                             :  :      
                               *@@@@@@@@@@%               :@@@@@@@@@ @@.                      .@@@@=:@      
                                :@@@@@@@@@                 #@@@@@@   @:                    .#@@@@@@@@@@     
                                :@@@@%@@                   .@@@@@-   .                     @@@@@@@@@@@@*    
                                :@@@@@@.                    *@@@-                          @@@@#@@@@@@@     
                                .@@@@@                                                           =@@@:    @=
                                 =@@                                                              =    #+   
                                  @%               
"""

# 2. Nettoyer l'écran avant l'affichage (optionnel, mais propre)
# 'cls' pour Windows, 'clear' pour Linux/macOS
os.system('cls' if os.name == 'nt' else 'clear')

# 3. Afficher le logo
print(logo_ascii)

# 4. Ajouter une petite pause avant le reste du script (optionnel)
time.sleep(2)

# --- CONFIGURATION ---
TIMEOUT_SECONDS = 5  # How long to wait before giving up (in seconds)
DEFAULT_PROTOCOL = 'http://' # We'll default to http:// for IP addresses
# ---------------------

def is_valid_ip(address):
    """Checks if the given string is a valid IPv4 or IPv6 address."""
    try:
        # Use the ipaddress library to check for a valid IP address
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False

def check_website_status(url, timeout):
    """Checks the status and response time of a website."""

    # Remove any trailing slashes or spaces the user might have added
    target = url.strip().rstrip('/')
    
    # 1. Check if the input is an IP address
    if is_valid_ip(target):
        # If it's an IP, ensure we add the protocol for the request to work
        if not target.startswith(('http://', 'https://')):
            url_to_check = DEFAULT_PROTOCOL + target
            print(f"INFO: Input is an IP address. Trying with protocol: {url_to_check}")
        else:
            url_to_check = target
    
    # 2. Check if the input is a domain/URL
    elif not target.startswith(('http://', 'https://')):
        # If it's a domain (like google.com) and has no protocol, default to HTTPS
        url_to_check = 'https://' + target
        print(f"INFO: Automatically trying URL as: {url_to_check}")
    else:
        # If it already has a protocol, use it as is
        url_to_check = target
        
    print(f"\n--- Starting Health Check ---")
    print(f"Target URL: {url_to_check}")
    print(f"Timeout set to: {timeout} seconds")
    
    # Simple "loading" message instead of animated bar
    print("Checking website status...")
    
    try:
        # Start the timer
        start_time = time.time()
        
        # Send a GET request
        response = requests.get(url_to_check, timeout=timeout)
        
        # Stop the timer
        end_time = time.time()
        
        # Calculate the total time
        response_time = end_time - start_time
        
        print("\n[RESULT]")
        
        # Check if the HTTP status code is good (200 means OK)
        if response.status_code == 200:
            print("STATUS: The website is CONNECTED and running WELL.")
            print(f"HTTP Status Code: {response.status_code} (OK)")
        else:
            print(f"STATUS: The website is CONNECTED but returned an ERROR.")
            print(f"HTTP Status Code: {response.status_code} (Problem! Check the error code)")
            
        # Print the response time
        print(f"Response Time: {response_time:.2f} seconds.")

        # --- Simple Health/DDoS Indicators ---
        if response_time > 3.0:
            print("\nWARNING: This time is very SLOW! A slow response can be a sign of **HIGH LOAD** or an attack like DDoS.")
        elif response_time > 1.0:
            print("\nNOTE: The time is a bit slow. The server might be busy (high traffic).")
        else:
            print("\nNOTE: The time is very fast. The server is likely very healthy and handling traffic easily.")
            
    except Timeout:
        print("\nCRITICAL FAILURE:")
        print(f"STATUS: TIMEOUT! The website took longer than {timeout} seconds to answer.")
        print(f"This is a strong sign of a MAJOR PROBLEM or a DDoS attack that is overloading the server.")
    except ConnectionError:
        print("\nCRITICAL FAILURE:")
        print("STATUS: NOT CONNECTED! The website address is unreachable.")
        print("The site is likely DOWN (off or completely overloaded/broken).")
    except HTTPError as e:
        print(f"\nCRITICAL FAILURE: An HTTP error occurred: {e}")
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: An unexpected error occurred: {e}")
    
    print("\n--- Check Complete ---")


# --- Main program flow to ask for the URL ---
if __name__ == "__main__":
    
    # Check if the required library is installed
    try:
        import ipaddress
    except ImportError:
        print("\n**ERROR**: The 'ipaddress' module is required. Please install it using: pip install ipaddress")
        sys.exit(1)
        
    # Ask the user for the URL or IP
    target_input = input("Please enter the website URL (google.com) or IP address (192.168.1.1): ")
    
    # Check if the input is empty
    if not target_input:
        print("\nERROR: No URL or IP entered. Exiting program.")
        sys.exit(1)
        
    # Run the check!
    check_website_status(target_input, TIMEOUT_SECONDS)