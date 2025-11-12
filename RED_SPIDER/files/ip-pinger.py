import socket
import time
import sys
import random

def tcp_connect_ping(ip, port, size):
    """
    Attempts a TCP connection to the target port, measures latency,
    and displays status in the requested format.
    The 'bytes' field is simulated to match the visual output.
    """
    
    # Simulate a successful connection by attempting a socket connection
    # and measuring the time it takes.
    
    # Set a small timeout to avoid hanging indefinitely
    socket.setdefaulttimeout(0.5) 
    
    # The bytes field in the output is constant (64) for visual similarity
    simulated_bytes = 64
    
    print(f"\n Starting TCP Ping on {ip}:{port} with {simulated_bytes} bytes per connection...")
    print("Press Ctrl+C to stop the process.")

    # Loop to continuously attempt connections
    while True:
        try:
            start_time = time.time()
            
            # Create a TCP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Attempt to connect
            result = sock.connect_ex((ip, port))
            
            end_time = time.time()
            # Calculate the latency in milliseconds
            latency_ms = (end_time - start_time) * 1000 
            
            # Close the connection immediately
            sock.close()
            
            # Determine status based on the connect_ex result
            if result == 0:
                status = "succeed"
            else:
                # Common errors like Connection Refused or Timeout
                status = "failed"
                
            # Display the result in the requested format
            print(f"Hostname: {ip} time: {latency_ms:.2f}ms port: {port} bytes: {simulated_bytes} status: {status}")
            
            # Pause for a short duration before the next attempt
            time.sleep(0.1) 
            
        except KeyboardInterrupt:
            print("\nStopping process. Exiting.")
            break
        except Exception as e:
            # Handle unexpected errors
            print(f"\nAn error occurred: {e}. Stopping process.")
            break


def main():
    """Handles user input and starts the TCP connection attempts."""
    print("---  Continuous TCP Connection Checker  ---")
    
    # 1. Ask for IP Address
    while True:
        ip = input("Enter the Target IP Address: ")
        if ip:
            break
        print("IP address cannot be empty.")

    # 2. Ask for Port (with default)
    port_default = 80
    while True:
        port_input = input(f"Enter the Target Port [enter for default: {port_default}]: ")
        if not port_input:
            port = port_default
            break
        try:
            port = int(port_input)
            if 1 <= port <= 65535:
                break
            print("Port must be between 1 and 65535.")
        except ValueError:
            print("Invalid port number. Please enter a valid integer.")
            
    # 3. Ask for Bytes (with default) - Used for visual effect only in this TCP script
    size_default = 64
    while True:
        # Note: The size here doesn't affect the TCP connection attempt, 
        # it's just used for the output display to match the image.
        size_input = input(f"Enter the Packet Size (bytes) [enter for default: {size_default}]: ")
        if not size_input:
            size = size_default
            break
        try:
            size = int(size_input)
            if size > 0:
                break
            print("Packet size must be greater than 0.")
        except ValueError:
            print("Invalid size. Please enter a valid integer.")
            
    # Start the TCP connection attempts
    tcp_connect_ping(ip, port, size)

if __name__ == '__main__':
    main()