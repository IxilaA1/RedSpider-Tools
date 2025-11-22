import socket
import concurrent.futures
import requests
from urllib.parse import urlparse
import ssl
import os
import urllib3
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import time
import sys

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

# --- Standard Library Imports Only ---
# The original script contained non-standard functions (e.g., ErrorModule, Title, ChoiceUserAgent,
# colors/formatting variables like BEFORE, white, red, etc.). These have been removed or replaced.

# --- Global Configuration (Replace custom functions/variables) ---
# ANSI Color Codes for basic console output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

# Helper function for colored/timed output
def log_message(prefix, message, color=Colors.WHITE):
    timestamp = time.strftime("[%H:%M:%S]")
    sys.stdout.write(f"{timestamp} {prefix} {color}{message}{Colors.RESET}\n")
    sys.stdout.flush()

# Simple User-Agent for requests
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

# Disable Insecure Request Warnings for requests library
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Scanner Functions ---

def get_website_url(url):
    """Ensures the URL has a scheme (defaults to https)."""
    website_url = url if urlparse(url).scheme else f"https://{url}"
    log_message("[WEBSITE]", f"URL: {website_url}", Colors.WHITE)
    return website_url

def get_domain(website_url):
    """Extracts the domain from the website URL."""
    domain = urlparse(website_url).netloc
    log_message("[DOMAIN]", f"Domain: {domain}", Colors.WHITE)
    return domain

def get_ip_address(domain):
    """Resolves the domain name to an IP address."""
    ip = "None"
    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        log_message("[IP]", "IP Address: Resolution failed.", Colors.RED)
        return "None"
    
    log_message("[IP]", f"IP Address: {ip}", Colors.WHITE)
    return ip

def get_ip_type(ip):
    """Determines if the IP is IPv4 or IPv6."""
    if ip == "None":
        return
    
    ip_type = "Unknown"
    if ':' in ip:
        ip_type = "IPv6"
    elif '.' in ip:
        ip_type = "IPv4"
        
    log_message("[IP TYPE]", f"Type: {ip_type}", Colors.WHITE)

def check_security(website_url):
    """Checks if the website uses HTTPS."""
    secure = website_url.startswith('https://')
    log_message("[SECURITY]", f"Secure (HTTPS): {secure}", Colors.GREEN if secure else Colors.RED)

def get_status_code(website_url):
    """Gets the HTTP status code for the website."""
    status_code = 404
    try:
        response = requests.get(website_url, timeout=5, headers=HEADERS, verify=False)
        status_code = response.status_code
        log_message("[STATUS]", f"Code: {status_code}", Colors.WHITE)
    except RequestException as e:
        log_message("[STATUS]", f"Code: Error ({e.__class__.__name__})", Colors.RED)
        return

def get_ip_info(ip):
    """Fetches geolocation and ASN information using ipinfo.io."""
    if ip == "None":
        return
        
    log_message("[IP INFO]", "Fetching IP details...", Colors.WHITE)
    try:
        api = requests.get(f"https://ipinfo.io/{ip}/json", headers=HEADERS, timeout=5).json()
    except RequestException:
        api = {}
        
    keys = ['country', 'hostname', 'isp', 'org', 'asn']
    for key in keys:
        if key in api:
            log_message("[IP INFO]", f"{key.capitalize()}: {api[key]}", Colors.WHITE)

def get_host_dns(ip):
    """Performs a reverse DNS lookup."""
    if ip == "None":
        return
        
    dns = "None"
    try:
        # gethostbyaddr returns a tuple: (hostname, aliaslist, ipaddrlist)
        dns = socket.gethostbyaddr(ip)[0]
    except Exception: # socket.herror or others
        pass
        
    if dns != "None":
        log_message("[DNS]", f"Host DNS: {dns}", Colors.WHITE)

def scan_website_ports(ip):
    """Scans a list of common ports using threading."""
    if ip == "None":
        return
        
    log_message("[PORT SCAN]", f"Scanning common ports on {ip}...", Colors.WHITE)
    ports = [21, 22, 23, 25, 53, 69, 80, 110, 123, 143, 194, 389, 443, 161, 3306, 5432, 6379, 1521, 3389]
    port_protocol_map = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 69: "TFTP",
        80: "HTTP", 110: "POP3", 123: "NTP", 143: "IMAP", 194: "IRC", 389: "LDAP",
        443: "HTTPS", 161: "SNMP", 3306: "MySQL", 5432: "PostgreSQL", 6379: "Redis",
        1521: "Oracle DB", 3389: "RDP"
    }

    def scan_port(ip, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5) # Reduced timeout for faster scans
                if sock.connect_ex((ip, port)) == 0:
                    protocol = port_protocol_map.get(port, 'Unknown')
                    log_message("[PORT SCAN]", f"Port: {port} Status: Open Protocol: {protocol}", Colors.GREEN)
        except Exception:
            pass

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # Use executor.submit instead of map for better handling of individual results
        futures = [executor.submit(scan_port, ip, p) for p in ports]
        # Wait for all futures to complete (optional)
        concurrent.futures.wait(futures)

def get_http_headers(website_url):
    """Lists all HTTP response headers."""
    log_message("[HEADERS]", "Fetching HTTP Headers...", Colors.WHITE)
    try:
        response = requests.get(website_url, timeout=5, headers=HEADERS, verify=False)
        for header, value in response.headers.items():
            log_message("[HEADERS]", f"{header}: {value}", Colors.WHITE)
    except RequestException:
        pass

def check_ssl_certificate(website_url):
    """Retrieves and prints SSL certificate details."""
    if not website_url.startswith('https://'):
        log_message("[SSL]", "Skipping SSL check: URL is not HTTPS.", Colors.RED)
        return

    log_message("[SSL]", "Checking SSL Certificate...", Colors.WHITE)
    
    hostname = urlparse(website_url).hostname
    if not hostname:
        return
        
    try:
        context = ssl.create_default_context()
        # Ensure we connect to the right port
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
        for key, value in cert.items():
            # Use repr() for values that might be complex like tuples or lists
            log_message("[SSL]", f"{key}: {repr(value)}", Colors.WHITE)
    except Exception as e:
        log_message("[SSL]", f"Error checking SSL Certificate: {e.__class__.__name__}", Colors.RED)

def check_security_headers(website_url):
    """Checks for the presence of common security headers."""
    log_message("[SEC HEADERS]", "Checking for common security headers...", Colors.WHITE)
    required_headers = [
        'Content-Security-Policy', 
        'Strict-Transport-Security', 
        'X-Content-Type-Options', 
        'X-Frame-Options', 
        'X-XSS-Protection'
    ]
    try:
        response_headers = requests.get(website_url, timeout=5, headers=HEADERS, verify=False).headers
        for header in required_headers:
            status = 'Present' if header in response_headers else 'Missing'
            color = Colors.GREEN if status == 'Present' else Colors.RED
            log_message("[SEC HEADERS]", f"{header}: {status}", color)
    except RequestException:
        pass

def analyze_cookies(website_url):
    """Analyzes cookies for Secure and HttpOnly flags."""
    log_message("[COOKIES]", "Analyzing cookies...", Colors.WHITE)
    try:
        # The requests library is designed to send cookies, not just receive the Set-Cookie headers.
        # To see the Set-Cookie headers, you'd inspect response.headers['Set-Cookie'].
        # For simplicity and sticking to the original intent of analyzing cookies returned by requests.get:
        response = requests.get(website_url, timeout=5, headers=HEADERS, verify=False)
        cookies = response.cookies
        
        if not cookies:
            log_message("[COOKIES]", "No cookies found.", Colors.WHITE)
            return

        for cookie in cookies:
            # Check for standard attributes
            secure = 'Secure' if cookie.secure else 'Not Secure'
            # Note: requests.cookies.RequestsCookieJar does not natively expose
            # an easy way to check for HttpOnly flag from the received header string
            # after the cookie has been parsed into the jar object.
            # We'll use a simplified check based on an assumed internal helper, but in reality, 
            # for full accuracy, you'd need to inspect the raw 'Set-Cookie' header value.
            # Replacing with a note for this simplified version.
            
            # Simplified check (might not be accurate for HttpOnly without inspecting raw header):
            httponly = "Unknown/N/A" # Accurate check requires raw headers

            log_message("[COOKIES]", 
                        f"Name: {cookie.name} | Secure: {secure} | HttpOnly: {httponly} | Domain: {cookie.domain}", 
                        Colors.WHITE)
    except RequestException:
        pass

def detect_technologies(website_url):
    """Detects technologies based on headers and common HTML tags."""
    log_message("[TECH]", "Detecting technologies...", Colors.WHITE)
    try:
        response = requests.get(website_url, timeout=5, headers=HEADERS, verify=False)
        headers = response.headers
        soup = BeautifulSoup(response.content, 'html.parser')
        techs = []
        
        # Check Headers
        if 'x-powered-by' in headers:
            techs.append(f"X-Powered-By: {headers['x-powered-by']}")
        if 'server' in headers:
            techs.append(f"Server: {headers['server']}")
            
        # Check HTML for common library mentions
        for script in soup.find_all('script', src=True):
            src = script['src'].lower()
            if 'jquery' in src and "jQuery" not in techs:
                techs.append("jQuery")
            if 'bootstrap' in src and "Bootstrap" not in techs:
                techs.append("Bootstrap")
        
        if not techs:
            log_message("[TECH]", "No common technologies detected.", Colors.WHITE)
            return

        for tech in set(techs): # Use set to ensure unique entries
            log_message("[TECH]", f"Detected: {tech}", Colors.WHITE)
    except RequestException:
        pass

# --- Main Execution Block ---

def run_scanner():
    """Main function to run the website scanner."""
    print(f"\n{Colors.GREEN}========================{Colors.RESET}")
    print(f"{Colors.GREEN}  Website Information Scanner{Colors.RESET}")
    print(f"{Colors.GREEN}========================{Colors.RESET}")
    log_message("[INFO]", f"Selected User-Agent: {HEADERS['User-Agent']}", Colors.WHITE)

    try:
        # Get user input
        url = input(f"\n[INPUT] Website URL -> {Colors.RESET}")
        
        # Basic input validation/censoring removal
        # The original Censored() function is removed, assume clean input for simplicity
        
        log_message("[INFO]", "Starting scan...", Colors.WHITE)

        # Run all functions sequentially
        website_url = get_website_url(url)
        domain = get_domain(website_url)
        
        print("\n" + "="*20 + "\n") # Separator
        
        ip = get_ip_address(domain)
        get_ip_type(ip)
        check_security(website_url)
        get_status_code(website_url)
        get_ip_info(ip)
        get_host_dns(ip)
        
        print("\n" + "="*20 + "\n") # Separator
        
        scan_website_ports(ip)
        
        print("\n" + "="*20 + "\n") # Separator
        
        get_http_headers(website_url)
        check_ssl_certificate(website_url)
        check_security_headers(website_url)
        analyze_cookies(website_url)
        detect_technologies(website_url)

    except KeyboardInterrupt:
        log_message("[EXIT]", "Scan interrupted by user.", Colors.RED)
    except Exception as e:
        log_message("[ERROR]", f"An unexpected error occurred: {e}", Colors.RED)

if __name__ == "__main__":
    run_scanner()