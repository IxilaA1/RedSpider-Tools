import subprocess
import re
import os
import sys

def display_wifi_passwords_windows():
    """
    Executes netsh commands to list Wi-Fi profiles and display
    their contents, including the security key, directly in the terminal.
    
    This version includes fallbacks for different encodings and regex formats.
    """
    if os.name != 'nt':
        print("Error: This script is only for Windows.")
        return
        
    print("\n--- Starting Wi-Fi Name and Key Display ---\n")

    # Determine the most likely encoding for the current console.
    # We will try cp437 first, then the system default encoding (sys.stdout.encoding).
    # cp437 is standard for netsh, but sometimes the system default works better.
    primary_encoding = 'cp437'
    fallback_encoding = sys.stdout.encoding if sys.stdout.encoding else 'utf-8'

    # --- 1. List all Wi-Fi profiles ---
    try:
        profiles_data = subprocess.run(
            ['netsh', 'wlan', 'show', 'profile'],
            capture_output=True,
            text=True,
            check=True,
            encoding=primary_encoding
        )
        output = profiles_data.stdout
    except UnicodeDecodeError:
        print(f"--- Retrying with fallback encoding: {fallback_encoding} ---")
        try:
            # Fallback attempt
            profiles_data = subprocess.run(
                ['netsh', 'wlan', 'show', 'profile'],
                capture_output=True,
                text=True,
                check=True,
                encoding=fallback_encoding
            )
            output = profiles_data.stdout
        except Exception as e:
            print(f"FATAL ERROR: Could not decode netsh output with either encoding. Error: {e}")
            return
    except subprocess.CalledProcessError as e:
        print(f"Error running 'netsh wlan show profile'. Make sure you are running as ADMINISTRATOR.")
        return
    except FileNotFoundError:
        print("Error: 'netsh' command not found.")
        return

    # Use a simplified regex to catch the profile names
    # This regex looks for any line containing a colon followed by a profile name.
    profile_names = re.findall(r":\s*([^\n\r]+)", output)
    
    # Filter the results to only include lines that look like a profile list (e.g., exclude header/footer)
    final_profiles = [name.strip() for name in profile_names if len(name.strip()) > 1 and name.strip() != ""]

    if not final_profiles:
        print("Warning: No Wi-Fi profiles found. Please ensure the terminal is running as Administrator.")
        return

    # --- 2. Iterate through each profile and get the key ---
    for profile_name in final_profiles:
        
        try:
            details_data = subprocess.run(
                ['netsh', 'wlan', 'show', 'profile', profile_name, 'key=clear'],
                capture_output=True,
                text=True,
                check=True,
                encoding=primary_encoding  # Use primary encoding again
            )
            details_output = details_data.stdout
        except UnicodeDecodeError:
            try:
                # Fallback for details output
                details_data = subprocess.run(
                    ['netsh', 'wlan', 'show', 'profile', profile_name, 'key=clear'],
                    capture_output=True,
                    text=True,
                    check=True,
                    encoding=fallback_encoding
                )
                details_output = details_data.stdout
            except Exception as e:
                print(f"Could not get details for '{profile_name}' due to encoding issue.")
                continue
        except subprocess.CalledProcessError as e:
            # This usually happens if the profile requires a different key handling (rare)
            details_output = e.output.strip()
            
        # Use a flexible regex to find the security key content
        key_match = re.search(r"(?:Contenu de la clé|Key Content)\s*:\s*(.*)", details_output, re.IGNORECASE)
        
        key = key_match.group(1).strip() if key_match else "N/A (Key not found or requires elevation)"

        # --- 3. Display the result in the terminal ---
        print("-" * 40)
        print(f"Wi-Fi Name (SSID) : {profile_name}")
        print(f"  Password Key    : {key}")
        print("-" * 40)

    print("\n--- Display Finished. No data was transmitted or saved externally. ---")


if __name__ == "__main__":
    display_wifi_passwords_windows()
