import concurrent.futures
import time
import socket
import sys
import os

# --- Basic Constants and Functions to Simulate Your Environment ---

   # 1. Le logo en texte ASCII généré (exemple)
logo_ascii = """
                                                 @@@@@@@@@@@@@@@@@@@                                 
                                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                         
                                    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                    
                                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                
                             @@@@@@@@@@@@@@@@@@                       @@@@@@@@@@@@@@@@@@             
                           @@@@@@@@@@@@@@                                   @@@@@@@@@@@@@@@          
                        @@@@@@@@@@@@@              @@@@@@@@@@@@@@@              @@@@@@@@@@@@@        
                       @@@@@@@@@@@          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@          @@@@@@@@@@@       
                       @@@@@@@@         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@         @@@@@@@@       
                        @@@@@        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        @@@@@        
                                  @@@@@@@@@@@@@@@                   @@@@@@@@@@@@@@@                  
                                @@@@@@@@@@@@@                           @@@@@@@@@@@@@                
                               @@@@@@@@@@            @@@@@@@@@@@            @@@@@@@@@@               
                                @@@@@@@         @@@@@@@@@@@@@@@@@@@@@         @@@@@@@                
                                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@                            
                                          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                          
                                         @@@@@@@@@@@             @@@@@@@@@@@                         
                                        @@@@@@@@@                   @@@@@@@@@                        
                                         @@@@@@        @@@@@@@        @@@@@@                         
                                                    @@@@@@@@@@@@@                                    
                                                   @@@@@@@@@@@@@@@                                   
                                                  @@@@@@@@@@@@@@@@@                                  
                                                  @@@@@@@@@@@@@@@@@                                  
                                                   @@@@@@@@@@@@@@@                                   
                                                    @@@@@@@@@@@@@                                    
                                                       @@@@@@@     
"""

# 2. Nettoyer l'écran avant l'affichage (optionnel, mais propre)
# 'cls' pour Windows, 'clear' pour Linux/macOS
os.system('cls' if os.name == 'nt' else 'clear')

# 3. Afficher le logo
print(logo_ascii)

# 4. Ajouter une petite pause avant le reste du script (optionnel)
time.sleep(2)

# Define basic colors for output clarity (if needed)
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    # Use these strings to simulate your original variables
    BEFORE = "" 
    AFTER = " "
    ADD = "[SUCCESS]"
    ERROR = "[ERROR]"
    INPUT = "[INPUT]"

# Replacement for undefined functions
def current_time_hour():
    return time.strftime("[%H:%M:%S]")

def Error(e):
    print(f"{current_time_hour()} {Colors.RED}[FATAL ERROR]{Colors.RESET} : {e}", file=sys.stderr)
    sys.exit(1)

def ErrorNumber():
    print(f"{current_time_hour()} {Colors.RED}[INPUT ERROR]{Colors.RESET} : Please enter a valid number for the port and bytes.")
    
def Title(text):
    print(f"\n--- {text} ---")

# --- TCP Ping Function (Port Connection Attempt) ---

Title("Ip Pinger")
print("Operation Mode: Repetitive TCP connection attempt (Port Scan).")

def PingIp(hostname, port, bytes_to_send=64):
    """
    Attempts to establish a TCP connection to hostname:port and send a small packet.
    """
    try:
        # Use socket.SOCK_STREAM for a TCP connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Set a timeout for a quick "ping"
            sock.settimeout(1) 
            start_time = time.time()
            
            # Attempt connection
            sock.connect((hostname, port))
            
            # Send data (simulates the packet, though not strictly needed for connection time)
            data = b'\x00' * bytes_to_send
            sock.sendall(data)
            
            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000  # in milliseconds
            
            # Success output
            output = (
                f"{Colors.BEFORE}{current_time_hour()}{Colors.AFTER} {Colors.ADD} "
                f"Hostname: {Colors.WHITE}{hostname}{Colors.RESET} "
                f"time: {Colors.WHITE}{elapsed_time:.2f}ms{Colors.RESET} "
                f"port: {Colors.WHITE}{port}{Colors.RESET} "
                f"bytes: {Colors.WHITE}{bytes_to_send}{Colors.RESET} "
                f"status: {Colors.GREEN}succeed{Colors.RESET}"
            )
            print(output)
            
    except socket.timeout:
        # Failure due to timeout
        output = (
            f"{Colors.BEFORE}{current_time_hour()}{Colors.AFTER} {Colors.ERROR} "
            f"Hostname: {Colors.WHITE}{hostname}{Colors.RESET} "
            f"time: {Colors.WHITE}0ms{Colors.RESET} "
            f"port: {Colors.WHITE}{port}{Colors.RESET} "
            f"bytes: {Colors.WHITE}{bytes_to_send}{Colors.RESET} "
            f"status: {Colors.RED}fail (Timeout){Colors.RESET}"
        )
        print(output)
        
    except ConnectionRefusedError:
         # Connection refused (port closed or filtered)
        output = (
            f"{Colors.BEFORE}{current_time_hour()}{Colors.AFTER} {Colors.ERROR} "
            f"Hostname: {Colors.WHITE}{hostname}{Colors.RESET} "
            f"time: {Colors.WHITE}0ms{Colors.RESET} "
            f"port: {Colors.WHITE}{port}{Colors.RESET} "
            f"bytes: {Colors.WHITE}{bytes_to_send}{Colors.RESET} "
            f"status: {Colors.YELLOW}fail (Refused){Colors.RESET}"
        )
        print(output)
        
    except Exception as e:
        # Other errors (e.g., host unknown)
        output = (
            f"{Colors.BEFORE}{current_time_hour()}{Colors.AFTER} {Colors.ERROR} "
            f"Hostname: {Colors.WHITE}{hostname}{Colors.RESET} "
            f"time: {Colors.WHITE}0ms{Colors.RESET} "
            f"port: {Colors.WHITE}{port}{Colors.RESET} "
            f"bytes: {Colors.WHITE}{bytes_to_send}{Colors.RESET} "
            f"status: {Colors.RED}fail ({e}){Colors.RESET}"
        )
        print(output)


# --- Main Script Logic ---
try:
    # 1. Hostname Input
    hostname = input(f"{Colors.BEFORE}{current_time_hour()}{Colors.AFTER} {Colors.INPUT} Ip -> {Colors.RESET}")
    
    # 2. Port Input
    port_input = input(f"{Colors.BEFORE}{current_time_hour()}{Colors.AFTER} {Colors.INPUT} Port (enter for default 80) -> {Colors.RESET}")
    try:
        port = int(port_input) if port_input else 80
    except ValueError:
        ErrorNumber()
        sys.exit(1)
        
    # 3. Bytes Input
    bytes_input = input(f"{Colors.BEFORE}{current_time_hour()}{Colors.AFTER} {Colors.INPUT} Bytes (enter for default 64) -> {Colors.RESET}")
    try:
        bytes_to_send = int(bytes_input) if bytes_input else 64
    except ValueError:
        ErrorNumber()
        sys.exit(1)

    print(f"\n{current_time_hour()} [INFO] Starting Pinger on {hostname}:{port} (Repeating every 2 seconds).")
    
    # Executor for parallel tasks
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            # Submit the task to the executor
            executor.submit(PingIp, hostname, port, bytes_to_send)
            
            # Wait between pings (changed from 0.1 to 2.0 for reasonable usage)
            time.sleep(2) 

except KeyboardInterrupt:
    print(f"\n{current_time_hour()} [INFO] Stopped by user.")
    sys.exit(0)
    
except Exception as e:
    Error(e)