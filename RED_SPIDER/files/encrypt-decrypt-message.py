from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

def derive_key(password_string, salt):
    """
    Derives a secure 32-byte encryption key (for AES-256) from the
    password (key) and the salt using PBKDF2.
    """
    password_bytes = password_string.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32, # Key size for AES-256
        salt=salt,
        iterations=100000, # High iteration count for robustness
        backend=default_backend()
    )
    return kdf.derive(password_bytes)

def encrypt_message(message, key_string):
    """Encrypts a message using AES-256 in GCM mode (with salt and IV)."""
    
    # 1. Generate a random Salt (unique for each encryption)
    salt = os.urandom(16)
    
    # 2. Derive the secure key from the robust key and salt
    key = derive_key(key_string, salt)
    
    # 3. Generate a random Initialization Vector (IV/Nonce)
    iv = os.urandom(12) # 12 bytes is the recommended size for GCM
    
    # 4. Encryption
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    tag = encryptor.tag # GCM Authentication Tag

    # 5. Combine components and encode in Base64 for transport
    # Output format is: salt + iv + ciphertext + tag
    encrypted_data = salt + iv + ciphertext + tag
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_message(encrypted_b64, key_string):
    """Decrypts a message using AES-256 GCM."""
    
    # 1. Decode Base64
    try:
        encrypted_data = base64.b64decode(encrypted_b64)
    except:
        return "ERROR: Encrypted message is not a valid Base64 string."
    
    # Check minimum length (Salt 16 + IV 12 + Tag 16)
    if len(encrypted_data) < 44: 
        return "ERROR: Encrypted message is too short or malformed."

    # 2. Separate components (Salt, IV, Ciphertext, Tag)
    salt = encrypted_data[:16]  # 16 bytes of salt
    iv = encrypted_data[16:28]  # 12 bytes of IV
    tag = encrypted_data[-16:]  # 16 bytes of GCM tag
    ciphertext = encrypted_data[28:-16] # The rest is the ciphertext
    
    # 3. Derive the key using the same salt as for encryption
    key = derive_key(key_string, salt)
    
    # 4. Decryption
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    
    try:
        decrypted_text_bytes = decryptor.update(ciphertext) + decryptor.finalize()
        return decrypted_text_bytes.decode('utf-8')
    except Exception as e:
        # Failure of the GCM tag verification means the key is incorrect 
        # or the message was tampered with.
        return f"ERROR: Decryption failed (Incorrect Key or Tampered data). Details: {e}"


def main():
    """Main function for the menu."""
    
    while True:
        print("\n--- AES Encryption/Decryption Tool (User Key) ---")
        print("1. Encrypt a message")
        print("2. Decrypt a message")
        print("3. Quit")
        
        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            print("\n--- ENCRYPTION MODE ---")
            # User enters their key
            key_input = input("Enter the SECRET KEY (e.g., 12345...): ")
            message = input("Enter the message to encrypt: ")
            
            encrypted_data = encrypt_message(message, key_input)
            
            print(f"\nOriginal Message: {message}")
            print(f"Key Used: {key_input[:5]}...{key_input[-5:]}")
            print(f"Encrypted Result (Base64): {encrypted_data}")
            
        elif choice == '2':
            print("\n--- DECRYPTION MODE ---")
            # User enters the key
            key_input = input("Enter the ORIGINAL SECRET KEY used for encryption: ")
            encrypted_message = input("Enter the encrypted message (Base64 string): ")
            
            decrypted_text = decrypt_message(encrypted_message, key_input)
            
            print(f"\nEncrypted Message: {encrypted_message}")
            print(f"Key Used: {key_input[:5]}...{key_input[-5:]}")
            print(f"Decrypted Result: {decrypted_text}")
            
        elif choice == '3':
            print("Exiting the encryption tool. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()