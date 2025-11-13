import socket
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys

# --- Configuration ---
# List of common ports to scan (you can modify this list)
COMMON_PORTS = [21, 22, 23, 25, 80, 110, 443, 3389, 8080]
PORT_TIMEOUT = 1.0 # Max wait time for each port connection attempt

def extract_internal_urls(target_url):
    """Fetches the webpage and extracts all internal links."""
    print(f"\n--- Fetching internal URLs for: {target_url}")
    
    # Ensure the URL has a scheme for successful request
    if not target_url.startswith(('http://', 'https://')):
        target_url = "http://" + target_url
        
    try:
        # Get page content
        response = requests.get(target_url, timeout=5)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get the base domain for filtering
        base_netloc = urlparse(target_url).netloc
        
        found_urls = set()
        
        # Find all <a> tags with an href attribute
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Convert relative URLs to absolute URLs
            full_url = urljoin(target_url, href)
            
            # Parse the full URL
            parsed_full_url = urlparse(full_url)
            
            # Check if it is an HTTP/HTTPS link and belongs to the same domain
            if parsed_full_url.scheme in ['http', 'https'] and parsed_full_url.netloc == base_netloc:
                found_urls.add(full_url)
                
        return found_urls
        
    except requests.exceptions.RequestException as e:
        print(f"--- Error while retrieving URL: {e}")
        return set()

def scan_ports(host, ports_to_scan):
    """Attempts to connect to specified ports to check if they are open."""
    print(f"\n--- Starting port scan for: {host}...")
    open_ports = []
    
    # Resolve hostname to IP address
    try:
        target_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"--- Error: Could not resolve hostname '{host}'.")
        return open_ports, host

    print(f"--- Target IP address: {target_ip}")

    for port in ports_to_scan:
        # Create a new socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(PORT_TIMEOUT)
        
        # Attempt connection
        result = sock.connect_ex((target_ip, port))
        
        if result == 0:
            open_ports.append(port)
            print(f"--- Port {port} is OPEN")
            
        sock.close()
        
    return open_ports, target_ip

def main():
    """Main function to run the scanner."""
    print("\n--- Python URL and Port Scanner Tool ---")
    
    # 1. Ask the user for the URL
    url_input = input("Enter the URL or Hostname (e.g., example.com or https://example.com): ").strip()
    
    if not url_input:
        print("No URL entered. Exiting program.")
        sys.exit(1)
        
    # Extract the host (domain) for the port scan
    parsed_url = urlparse(url_input)
    
    # Use the netloc (e.g., example.com) as the host for the port scan
    # If no scheme, use the raw input
    host_for_scan = parsed_url.netloc if parsed_url.netloc else url_input
    
    if not host_for_scan:
        print("--- Invalid host after parsing. Exiting program.")
        sys.exit(1)
        
    # --- 2. Execute Port Scan ---
    open_ports, target_ip = scan_ports(host_for_scan, COMMON_PORTS)
    
    print("\n" + "="*40)
    print("PORT SCAN RESULTS")
    print(f"Target: {target_ip} ({host_for_scan})")
    print(f"Ports Scanned: {len(COMMON_PORTS)}")
    print(f"Open Ports: {open_ports if open_ports else 'None found in the common list.'}")
    print("="*40)
    
    # --- 3. Execute URL Extraction ---
    internal_urls = extract_internal_urls(url_input)
    
    print("\n" + "="*40)
    print("INTERNAL URL EXTRACTION RESULTS")
    print(f"Total Internal URLs Found: {len(internal_urls)}")
    for url in sorted(list(internal_urls)):
        print(f"- {url}")
    print("="*40)


if __name__ == "__main__":
    main()