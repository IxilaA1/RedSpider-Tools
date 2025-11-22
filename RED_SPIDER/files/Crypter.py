import hashlib
import os

def process_file():
    """Handles the user input and the file encryption/decryption process."""

    # --- Step 1: Operation Selection ---
    print("--- File Processor ---")
    while True:
        mode = input("Select operation (E for Encrypt, D for Decrypt): ").upper()
        if mode in ('E', 'D'):
            break
        print("Invalid selection. Please enter 'E' or 'D'.")

    operation = "Encryption" if mode == 'E' else "Decryption"
    print(f"\nSelected operation: **{operation}**")
    print("----------------------")


    # --- Step 2: User Inputs ---
    # 1. Exact path of the file to process
    input_path = input("Enter the exact path of the file to process (e.g., C:\\Users\\...\\file.txt): ")
    
    # 2. Output file name
    output_name = input("Enter the desired name for the output file: ")
    
    # 3. Key for encryption/decryption
    key = input("Enter the secret key: ")
    
    # --- Step 3: Key Derivation ---
    # Hash the key using SHA256 to create the actual encryption/decryption key stream
    keys = hashlib.sha256(key.encode('utf-8')).digest()
    
    # --- Step 4: Determine Output Path ---
    try:
        # Get the directory (folder) of the input file
        input_directory = os.path.dirname(input_path)
        if not input_directory:
             # Handle cases where only a filename is given (assumes current directory)
             input_directory = os.getcwd() 

        # Construct the full output path in the same directory
        output_path = os.path.join(input_directory, output_name)

    except Exception as e:
        print(f"\n Error resolving file paths: {e}")
        return

    # --- Step 5: File Operation ---
    print(f"\nProcessing file: {input_path}")
    print(f"Saving output to: {output_path}")

    try:
        # Open the input file in binary read mode ('rb')
        with open(input_path, 'rb') as f_input:
            # Open the output file in binary write mode ('wb')
            with open(output_path, 'wb') as f_output:
                i = 0  # Counter for key stream index
                
                # Loop until the end of the input file is reached
                while True:
                    # Read one byte at a time
                    read_byte = f_input.read(1)
                    
                    # Exit the loop if no more bytes are read (End of File)
                    if not read_byte:
                        break
                    
                    # Convert the byte to an integer (c)
                    c = ord(read_byte)
                    
                    # Calculate the key stream index (j)
                    j = i % len(keys)
                    
                    # XOR Operation: c ^ keys[j]
                    # The result is converted back to a byte object (b)
                    b = bytes([c ^ keys[j]])
                    
                    # Write the processed byte
                    f_output.write(b)
                    
                    # Increment the counter
                    i = i + 1
            
        print(f"\n Operation {operation} completed successfully!")
        print(f"The file '{output_name}' has been created in the directory: {input_directory}")

    except FileNotFoundError:
        print(f"\n Error: The input file was not found at the specified location: {input_path}")
    except Exception as e:
        print(f"\n An unexpected error occurred during file processing: {e}")

# Run the main function
if __name__ == "__main__":
    process_file()