import socket
import time
import ipaddress
import sys

def port_scanner():
    """
    A simple port scanner that prompts for an IP address and checks common ports.
    """
    # --- Get Target IP from User ---
    while True:
        try:
            target_ip_str = input("Enter Target IP: ")
            # Validate IP format
            ipaddress.ip_address(target_ip_str)
            target_ip = target_ip_str
            break
        except ValueError:
            print("Invalid IP address format. Please try again.")
            
    print(f"\nScanning Target: {target_ip}")
    print("-" * 40)
    
    start_time = time.time()
    scan_start_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
    print(f"Scanning started at: {scan_start_datetime}")
    print("-" * 40)
    
    # --- Define Ports to Scan ---
    # Common ports (you can expand this list)
    ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3389, 8080]
    
    open_ports_found = False

    # --- Scan Loop ---
    for port in ports_to_scan:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5) # Set a timeout for connection attempts

        # Attempt to connect to the port
        result = sock.connect_ex((target_ip, port))
        
        if result == 0:
            print(f"[*] Port {port} is open")
            open_ports_found = True
        
        sock.close()

    # --- Scanning Summary ---
    end_time = time.time()
    total_time = end_time - start_time
    print("-" * 40)
    
    if not open_ports_found:
        print("No common open ports found in the specified range.")
    
    print(f"Scanning finished in {total_time:.2f} seconds.")

if __name__ == "__main__":
    try:
        port_scanner()
    except KeyboardInterrupt:
        print("\nExiting program.")
        sys.exit()
    except socket.gaierror:
        print("\nHostname could not be resolved.")
        sys.exit()
    except socket.error:
        print("\nCould not connect to the server.")
        sys.exit()