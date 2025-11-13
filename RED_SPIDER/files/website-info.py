import socket
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys
import ssl

# --- Configuration ---
# Ports to scan, including common ports where banner grabbing is effective
COMMON_PORTS = [21, 22, 23, 25, 80, 110, 443, 8080]
TIMEOUT_PORT = 1.0       # Timeout for initial port check
BANNER_TIMEOUT = 2.0     # Timeout for reading the banner data

def grab_banner(host, port, target_ip):
    """Connects to an open port and attempts to retrieve the service banner."""
    banner = "Not available / Connection closed"
    sock = None
    
    try:
        # 1. Handle SSL/TLS for HTTPS (Port 443)
        if port == 443:
            context = ssl.create_default_context()
            sock = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
        sock.settimeout(BANNER_TIMEOUT)
        sock.connect((target_ip, port))
        
        # 2. Send basic HTTP request for web ports (80/443/8080)
        if port in [80, 443, 8080]:
            # Send a GET request to retrieve HTTP headers, including 'Server'
            request = f"GET / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: InfoScanner/1.0\r\nConnection: close\r\n\r\n"
            sock.sendall(request.encode())
            
            # Read the first few lines of the response (the headers)
            response = sock.recv(4096).decode('latin-1', errors='ignore').split('\n')
            
            # Search for the 'Server' header
            server_info = [line for line in response if line.lower().startswith('server:')]
            if server_info:
                banner = server_info[0].strip()
            else:
                # Fallback: take the first line (HTTP response code)
                banner = response[0].strip() if response else "HTTP/HTTPS response with no 'Server' header"
                
        # 3. For other ports (FTP, SSH, Telnet, etc.), read the initial response
        else:
            # Read the initial data received (the service banner)
            data = sock.recv(1024)
            # Take the first line of the banner for cleaner output
            banner = data.decode('latin-1', errors='ignore').strip().split('\n')[0]
            
    except Exception as e:
        banner = f"Error retrieving banner: {e}"
    finally:
        if sock:
            try:
                sock.close()
            except:
                pass 

    return banner

def extract_internal_urls(target_url):
    """Fetches the webpage and extracts all internal links (Unchanged from previous version)."""
    # Ensure the URL has a scheme for successful request
    if not target_url.startswith(('http://', 'https://')):
        target_url = "http://" + target_url
        
    try:
        response = requests.get(target_url, timeout=5)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
        base_netloc = urlparse(target_url).netloc
        found_urls = set()
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(target_url, href)
            parsed_full_url = urlparse(full_url)
            
            if parsed_full_url.scheme in ['http', 'https'] and parsed_full_url.netloc == base_netloc:
                found_urls.add(full_url)
                
        return found_urls
        
    except requests.exceptions.RequestException as e:
        return set()

def scan_ports(host, ports_to_scan):
    """Scans ports and calls grab_banner for open ports."""
    print(f"\n--- Starting Port Scan and Info Grabbing for: {host}...")
    open_ports_details = [] # List to store port and banner info
    
    try:
        target_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"--- Error: Could not resolve hostname '{host}'.")
        return open_ports_details, host

    print(f"--- Target IP address: {target_ip}")

    for port in ports_to_scan:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT_PORT)
        
        result = sock.connect_ex((target_ip, port))
        
        if result == 0:
            print(f"--- Port {port} is OPEN. Attempting to retrieve info...")
            # Call the banner grabbing function
            banner = grab_banner(host, port, target_ip) 
            open_ports_details.append({'port': port, 'info': banner})
            
        sock.close()
        
    return open_ports_details, target_ip

def main():
    """Main function to execute the scanner."""
    print("\n--- Python Info and URL Scanner Tool ---")
    
    # 1. Ask the user for the URL
    url_input = input("Enter the URL or Hostname (e.g., example.com or https://example.com): ").strip()
    
    if not url_input:
        print("No URL entered. Exiting program.")
        sys.exit(1)
        
    # Extract the host (domain) for the port scan
    parsed_url = urlparse(url_input)
    host_for_scan = parsed_url.netloc if parsed_url.netloc else url_input
    
    if not host_for_scan:
        print("--- Invalid host after parsing. Exiting program.")
        sys.exit(1)
        
    # --- 2. Execute Port Scan & Info Grabbing ---
    open_ports_details, target_ip = scan_ports(host_for_scan, COMMON_PORTS)
    
    print("\n" + "="*70)
    print("PORT SCAN AND INFO (BANNER GRABBING) RESULTS")
    print(f"Target: {target_ip} ({host_for_scan})")
    print(f"Ports Scanned: {len(COMMON_PORTS)}")
    print("---")
    
    if open_ports_details:
        for item in open_ports_details:
            print(f"[Port {item['port']}] Service Info: {item['info']}")
    else:
        print("No open ports found in the common list.")
    print("="*70)
    
    # --- 3. Execute Internal URL Extraction ---
    internal_urls = extract_internal_urls(url_input)
    
    print("\n" + "="*70)
    print("INTERNAL URL EXTRACTION RESULTS")
    print(f"Total Internal URLs Found: {len(internal_urls)}")
    for url in sorted(list(internal_urls)):
        print(f"- {url}")
    print("="*70)


if __name__ == "__main__":
    main()