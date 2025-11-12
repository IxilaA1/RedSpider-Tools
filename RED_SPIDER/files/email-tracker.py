import re

def get_email_info(email):
    # Regular expression for a basic email format validation (not exhaustive)
    # [a-zA-Z0-9._%+-]+ : Local part
    # @ : The separator
    # [a-zA-Z0-9.-]+ : The domain
    # \. : A dot
    # [a-zA-Z]{2,} : The extension (tld), at least 2 characters
    regex = r"([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
    
    match = re.search(regex, email)
    
    if match:
        local_part = match.group(1)
        full_domain = match.group(2)
        
        # Separate the main domain from the extension (TLD)
        domain_parts = full_domain.rsplit('.', 1)
        # Handle cases where rsplit might not find a dot (for maximum robustness, although regex should prevent this)
        domain = domain_parts[0] if len(domain_parts) > 1 else full_domain 
        extension = domain_parts[1] if len(domain_parts) > 1 else "N/A"

        print("\n--- Email Information ---")
        print(f"Email Format: Valid (basic check)")
        print(f"Local Part: {local_part}")
        print(f"Full Domain: {full_domain}")
        print(f"Main Domain: {domain}")
        print(f"Extension (TLD): {extension}")
        print("-------------------------")
    else:
        print(f"\nThe format of the email '{email}' is not valid (basic check).")

# Ask the user for the email
user_email = input("Please enter an email address: ")

# Call the function
get_email_info(user_email)