# -*- coding: utf-8 -*-
import random
import time

def generate_random_ip():
    """Generates a random IPv4 address."""
    ip_parts = []
    # Loop 4 times for the 4 octets
    for _ in range(4):
        octet = str(random.randint(0, 255))
        ip_parts.append(octet)
    
    ip = ".".join(ip_parts)
    return ip

if __name__ == "__main__":
    while True:
        try:
            num_ips_input = input("Enter the number of IP addresses to generate: ")
            num_ips = int(num_ips_input)

            if num_ips < 1:
                print("Please enter a positive number (1 or more).")
                continue
            
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print(f"\nGenerating {num_ips} random IP addresses...")
    print("---------------------------------")
    
    # Slower initial delay
    time.sleep(0.7) 
    
    for i in range(num_ips):
        # 1. Start message (slower display)
        # We print a placeholder to be overwritten later
        print(f"[{i+1}/{num_ips}] Creating IP address...", end="", flush=True) 
        
        # 2. Slower delay to simulate processing time
        time.sleep(0.75) 
        
        # 3. Actual generation
        random_ip = generate_random_ip()
        
        # 4. Display the result, overwriting the "Creating..." message
        # \r (carriage return) moves the cursor to the start of the line
        # Note: We use a longer string here to ensure it fully overwrites the previous one.
        print(f"\r[{i+1}/{num_ips}] IP created: {random_ip}         ") 
        
        # 5. Slower delay before moving to the next one
        time.sleep(0.5)