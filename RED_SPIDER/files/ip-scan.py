import socket
import ssl
import subprocess
import sys
import requests
import concurrent.futures
import time
import re
import os
from requests.exceptions import RequestException

   # 1. Le logo en texte ASCII généré (exemple)
logo_ascii = """
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                   >|a@@@@@@@@@|                                                
                                              }@@@@@@@@@@@@@@@@| 000M|                                          
                                          ;@@@@@@O  @@@@@@@@@@@|  j000000_                                      
                                       }@@@@@v   |@@@@@@@@@@@@@| 00J  |00000j                                   
                                     @@@@@_     @@@@@@@@@@@@@@@| 0000    ;00000^                                
                                  ;@@@@v       _@@@@@@@     >@@| 0000v      }0000_                              
                                ^@@@@_         @@@@@@@      ^O@| 00000        ;0000_                            
                                 @@@@;         @@@@@@@      ;p@| 00000         0000^                            
                                   @@@@p       >@@@@@@@^    >@@| 0000v      J0000;                              
                                     O@@@@|     M@@@@@@@@@@@@@@| 0000    >00000                                 
                                       ;@@@@@J^  }@@@@@@@@@@@@@| 00v  j00000}                                   
                                          >@@@@@@@_;@@@@@@@@@@@| ;M000000_                                      
                                              >@@@@@@@@@@@@@@@@| 00000}                                          
                                                   ^jpM@@@@@@@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@| 
"""

# 2. Nettoyer l'écran avant l'affichage (optionnel, mais propre)
# 'cls' pour Windows, 'clear' pour Linux/macOS
os.system('cls' if os.name == 'nt' else 'clear')

# 3. Afficher le logo
print(logo_ascii)

# 4. Ajouter une petite pause avant le reste du script (optionnel)
time.sleep(2)

# --- Utility Functions (Replacing missing framework calls) ---

# Basic ANSI Color Codes
RESET = "\033[0m"
WHITE = "\033[97m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"

def current_time_hour():
    """Returns the formatted time for logging."""
    return time.strftime("[%H:%M:%S]")

def log_info(message, status="INFO", color_msg=WHITE, color_status=BLUE):
    """Simplified logging function to replace custom print statements."""
    status_map = {
        "INFO": BLUE,
        "SUCCESS": GREEN,
        "WAIT": YELLOW,
        "ERROR": RED
    }
    status_color = status_map.get(status, BLUE)
    # Replicating the original formatting style: [TIME] [STATUS] MESSAGE
    print(f"{current_time_hour()} {status_color}[{status}]{RESET} {color_msg}{message}{RESET}")

def is_valid_ip(ip):
    """Simple check for valid IPv4 or IPv6 format."""
    ipv4_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    ipv6_pattern = r"^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^::|^[0-9a-fA-F]{1,4}::"
    
    if re.match(ipv4_pattern, ip):
        return True
    if re.match(ipv6_pattern, ip):
        # Note: This is a basic check. Real IPv6 validation is complex.
        return True
    return False

# --- Scanning Functions ---

def IpType(ip):
    """Determines and displays the IP type."""
    ip_type_str = "Unknown"
    if ':' in ip:
        ip_type_str = "IPv6"
    elif '.' in ip:
        ip_type_str = "IPv4"
    log_info(f"IP Type: {ip_type_str}", "INFO", RED)

def IpPing(ip):
    """Pings the IP address."""
    try:
        # Adjusted for cross-platform compatibility and reliability
        if sys.platform.startswith("win"):
            # -n 1 for count, -w 1000 for 1-second timeout (in ms)
            ping_cmd = ['ping', '-n', '1', '-w', '1000', ip]
        else:
            # -c 1 for count, -W 1 for 1-second timeout (in seconds)
            ping_cmd = ['ping', '-c', '1', '-W', '1', ip]
            
        # Increase timeout for the subprocess call itself to 2 seconds
        result = subprocess.run(ping_cmd, capture_output=True, text=True, timeout=2)
        
        ping_status = "Succeed" if result.returncode == 0 else "Fail"
        log_info(f"Ping: {ping_status}", "SUCCESS" if result.returncode == 0 else "ERROR", RED)
        
    except (subprocess.TimeoutExpired, FileNotFoundError):
        log_info(f"Ping: Fail (Timeout or command not found)", "ERROR", RED)
    except Exception:
        log_info(f"Ping: Fail (General Error)", "ERROR", RED)

def IpPort(ip):
    """Scans common ports using concurrent threads."""
    port_protocol_map = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 69: "TFTP",
        80: "HTTP", 110: "POP3", 123: "NTP", 143: "IMAP", 194: "IRC", 389: "LDAP",
        443: "HTTPS", 161: "SNMP", 3306: "MySQL", 5432: "PostgreSQL", 6379: "Redis",
        1521: "Oracle DB", 3389: "RDP"
    }
    
    def scan_port(ip_address, port):
        """Internal function to scan a single port."""
        try:
            # Use AF_INET for IPv4 sockets. Adjust for IPv6 if needed.
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5) # Reduced timeout for faster scanning
                result = sock.connect_ex((ip_address, port))
                if result == 0:
                    protocol = port_protocol_map.get(port, "Unknown")
                    log_info(f"Port: {port}{RED} Status: {WHITE}Open{RED} Protocol: {WHITE}{protocol}", "SUCCESS", RED)
        except Exception:
            pass # Suppress connection/timeout errors for closed ports

    log_info("Starting Port Scan...", "WAIT", RED)
    
    # Concurrent scanning using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # map() is cleaner than submit() and wait() for this simple task
        executor.map(lambda port: scan_port(ip, port), port_protocol_map.keys())

def IpDns(ip):
    """Performs a reverse DNS lookup."""
    try:
        # gethostbyaddr can raise socket.herror (name or service not known)
        dns, aliaslist, ipaddrlist = socket.gethostbyaddr(ip)
        log_info(f"DNS/Hostname: {dns}", "INFO", RED)
    except socket.herror:
        log_info("DNS/Hostname: None found", "INFO", RED)
    except Exception as e:
        log_info(f"DNS/Hostname Check Failed: {e}", "ERROR", RED)


def IpHostInfo(ip):
    """Retrieves geological and ISP information using ipinfo.io."""
    api_url = f"https://ipinfo.io/{ip}/json"
    log_info("Fetching Geo/ISP Information...", "WAIT", RED)

    try:
        # Added timeout for requests
        response = requests.get(api_url, timeout=5)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        api = response.json()
    except RequestException as e:
        log_info(f"Host Info API Request Failed: {e}", "ERROR", RED)
        api = {}

    # List of fields to display
    info_fields = {
        'country': "Host Country",
        'org': "Host ISP",
        'asn': "Host AS",
        'hostname': "Host Name"
    }
    
    # Process and display results
    for key, label in info_fields.items():
        value = api.get(key, 'None')
        if value and value != "None":
            log_info(f"{label}: {value}", "INFO", RED)

def SslCertificateCheck(ip):
    """Checks for an SSL certificate on port 443."""
    port = 443
    log_info(f"Checking SSL Certificate on port {port}...", "WAIT", RED)
    
    try:
        # 1. TCP connection
        with socket.create_connection((ip, port), timeout=2) as sock:
            # 2. SSL/TLS Handshake
            context = ssl.create_default_context()
            # For server_hostname, we use the IP address itself
            with context.wrap_socket(sock, server_hostname=ip) as ssock:
                cert = ssock.getpeercert()
                
                # Extract subject (Common Name) and issuer for a readable output
                subject = dict(cert['subject'])
                issuer = dict(cert['issuer'])
                common_name = next((v for k, v in subject.get('commonName', [])), 'N/A')
                issuer_cn = next((v for k, v in issuer.get('organizationName', [])), 'N/A')

                log_info(f"SSL Status: Found", "SUCCESS", RED)
                log_info(f"SSL Common Name: {common_name}", "INFO", RED)
                log_info(f"SSL Issuer Org: {issuer_cn}", "INFO", RED)
                
    except ConnectionRefusedError:
        log_info("SSL Certificate Check: Port 443 closed or refused connection.", "ERROR", RED)
    except ssl.SSLError as e:
        log_info(f"SSL Certificate Check Failed (SSL Error): {e}", "ERROR", RED)
    except Exception as e:
        log_info(f"SSL Certificate Check Failed: {e}", "ERROR", RED)

# --- Main Execution Block ---

def main():
    """Main function to run the IP scanner."""
    print(f"\n{YELLOW}--- IP Scanner ---{RESET}\n")

    while True:
        # Replacing the custom INPUT and reset variables
        ip = input(f"{current_time_hour()} {GREEN}[INPUT]{RESET} Enter Target IP -> {RESET}")
        if is_valid_ip(ip):
            break
        else:
            log_info("Invalid IP format. Please enter a valid IPv4 or IPv6 address.", "ERROR", RED)

    log_info(f"Target IP: {ip}", "INFO", RED)
    log_info("Information Recovery started...", "WAIT", RED)
    print("-" * 35)

    # Execution of scanning functions
    IpType(ip)
    IpPing(ip)
    IpDns(ip)
    IpHostInfo(ip)
    IpPort(ip) 
    SslCertificateCheck(ip)
    
    print("-" * 35)
    log_info("Scanning complete.", "SUCCESS", RED)
    # Replaced Continue() and Reset() with simple exit
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_info("Program interrupted by user (Ctrl+C). Exiting.", "ERROR", RED)
    except Exception as e:
        # Replaced the generic Error(e) call
        log_info(f"An unhandled error occurred: {e}", "ERROR", RED)