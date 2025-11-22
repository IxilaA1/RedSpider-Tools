import piexif
import exifread
import base64
import os
import tkinter
from PIL import Image
from tkinter import filedialog
import time # Added missing import for time.ctime/time.sleep
import sys # Added missing import for sys.platform

# --- Assume these external variables and functions are defined elsewhere in the original script ---
# For translation purposes, I'll replace them with placeholders or standard print calls.
# You will need to define or replace the following functions/variables:
# BEFORE, current_time_hour, AFTER, INPUT, reset, INFO, white, name_tool, version_tool, tool_path,
# osint_banner, WAIT, ERROR, INFO_ADD, Slow, Continue, Reset, Error, ErrorModule, Title
# For this corrected script, I will use standard Python print for output.

# Placeholder definitions for missing dependencies (replace with your actual utility functions/variables)
def ErrorModule(e):
    print(f"ERROR: Failed to import module: {e}")

def Title(title_text):
    print(f"\n--- {title_text} ---\n")

def current_time_hour():
    return time.strftime("%H:%M:%S")

# Simplified logging placeholders (replace with your actual colored logging system)
BEFORE = "[LOG "
AFTER = "]"
INPUT = "[INPUT]"
INFO = "[INFO]"
WAIT = "[WAIT]"
ERROR = "[ERROR]"
INFO_ADD = "[DATA]"
reset = ""
white = ""
name_tool = "EXIF Extractor"
version_tool = "1.0"
osint_banner = "--- Image EXIF Analysis ---"

def Slow(text):
    print(text)

def Continue():
    input("\nPress Enter to continue...")

def Reset():
    pass

def Error(e):
    print(f"\nAN UNEXPECTED ERROR OCCURRED: {e}")
# ------------------------------------------------------------------------------------------------

Title("Get Image Exif")

try:
    def ChooseImageFile():
        """
        Opens a file dialog for selecting an image file, or falls back to
        command-line input if the dialog fails.
        """
        try:
            print(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Enter the path to the image -> {reset}")
            
            # File type filter for dialog
            image_file_types = [("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff"), ("All files", "*.*")]

            file = ""
            
            # Windows/Linux specific file dialog setup
            if sys.platform.startswith("win"):
                root = tkinter.Tk()
                # If tool_path is defined, uncomment the next line, otherwise remove it.
                # root.iconbitmap(os.path.join(tool_path, "Img", "RedTiger_icon.ico"))
                root.withdraw()
                root.attributes('-topmost', True)
                file = filedialog.askopenfilename(parent=root, title=f"{name_tool} {version_tool} - Choose an image file", filetypes=image_file_types)
                root.destroy() # Clean up the Tkinter root window
            else: # Covers Linux and other systems
                # Note: On Linux, ensure tkinter is installed (e.g., python3-tk)
                root = tkinter.Tk()
                root.withdraw()
                file = filedialog.askopenfilename(title=f"{name_tool} {version_tool} - Choose an image file", filetypes=image_file_types)
                root.destroy()
            
            # Check if a file was selected/path provided
            if file:
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} File path: {white + file}")
                return file
            else:
                 # If dialog is closed/canceled, fall back to manual input prompt
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} File selection canceled. Falling back to manual input.")
                return input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Enter the path to the image -> {reset}")

        except Exception as e:
            # Fallback for systems where tkinter or file dialog fails
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} File dialog failed ({e}). Falling back to manual input.")
            return input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Enter the path to the image -> {reset}")


    def CleanValue(value):
        """
        Cleans up raw EXIF values, decoding bytes to strings or formatting lists/tuples.
        """
        if isinstance(value, bytes):
            try:
                # Try to decode as standard UTF-8
                return value.decode('utf-8', errors='replace')
            except:
                # Fallback to base64 encoding if decoding fails
                return base64.b64encode(value).decode('utf-8')
        elif isinstance(value, (list, tuple)):
            # Join lists/tuples into a comma-separated string
            return ', '.join(str(v) for v in value)
        elif isinstance(value, dict):
            # Recursively clean up dictionary values
            return {k: CleanValue(v) for k, v in value.items()}
        else:
            # Return all other types as is
            return value
            
    def GetAllExif(image_path):
        """
        Extracts all available EXIF and file metadata using piexif, exifread, PIL, and os.
        """
        exif_data = {}

        # 1. Extract data using piexif (Handles standard EXIF data structures well)
        try:
            exif_dict = piexif.load(image_path)
            for ifd in exif_dict:
                if isinstance(exif_dict[ifd], dict):
                    for tag in exif_dict[ifd]:
                        # Get tag name from piexif dictionary, fall back to tag number
                        tag_name = piexif.TAGS.get(ifd, {}).get(tag, {"name": tag})["name"]
                        raw_value = exif_dict[ifd][tag]
                        
                        # Only add if not already present from the second pass (second piexif attempt was redundant)
                        # We are consolidating the two piexif blocks into one for efficiency
                        if tag_name not in exif_data:
                            exif_data[f"{tag_name}"] = CleanValue(raw_value)
        except Exception as e:
            # Log piexif error but continue to other methods
            # exif_data["PIEXIF_ERROR"] = str(e) # Keeping this commented out for cleaner output unless troubleshooting is needed.
            pass

        # 2. Extract data using exifread (Good for robust raw tag reading and often GPS data)
        try:
            with open(image_path, 'rb') as f:
                # details=True provides raw values, which we convert to string later
                tags = exifread.process_file(f, details=True)
                for tag in tags:
                    # Use the last part of the tag name (e.g., 'Make' from 'Image Make')
                    label = tag.split()[-1]
                    # Only add if the tag name isn't already found by piexif
                    if label not in exif_data:
                        exif_data[label] = CleanValue(str(tags[tag])) # exifread values are converted to string here
        except Exception as e:
            # exif_data["EXIFREAD_ERROR"] = str(e) # Keeping this commented out for cleaner output
            pass
            
        # 3. Get basic image file dimensions (Width, Height, Depth/Bands) using PIL
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                depth = len(img.getbands())
                exif_data['Dimension'] = f"{width}x{height}"
                exif_data['Width'] = width
                exif_data['Height'] = height
                exif_data['Depth'] = depth
        except Exception as e:
            exif_data["Image Error"] = f"Could not open image file: {str(e)}"

        # The second 'piexif.load' block in the original script was redundant, so it's removed.

        # 4. Get file system statistics and basic info using os
        try:
            file_stats = os.stat(image_path)
            exif_data['Name'] = os.path.basename(image_path)
            exif_data['Type'] = os.path.splitext(image_path)[1]
            # Convert timestamp to human-readable format
            exif_data['Creation Date'] = time.ctime(file_stats.st_ctime)
            exif_data['Date Modified'] = time.ctime(file_stats.st_mtime)
            exif_data['Attributes (Mode)'] = oct(file_stats.st_mode)
            # Check read access
            exif_data['Availability'] = 'Available (Read Access)' if os.access(image_path, os.R_OK) else 'Not available (No Read Access)'
            exif_data['Offline Status'] = 'Online (Exists)' if os.path.exists(image_path) else 'Offline (Does not Exist)'
        except Exception as e:
            exif_data["File Stats Error"] = str(e)
            
        # 5. Display the results
        if exif_data:
            # Find the length of the longest key for neat alignment
            max_key_length = max(len(k) for k in exif_data.keys()) if exif_data.keys() else 0

            print(f"\n{white}------------------------------------------------------------------------------------------------------------------------")
            # Sort the output by key name (case-insensitive) for better readability
            for key, value in sorted(exif_data.items(), key=lambda x: x[0].lower()):
                # Format: [DATA] KeyName : Value
                print(f" {INFO_ADD} {key.ljust(max_key_length)} : {white + str(value)}")
                time.sleep(0.01) # Small delay for 'Slow' effect (original script used this)
            print(f"{white}------------------------------------------------------------------------------------------------------------------------\n")
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} No information found.")

    Slow(osint_banner)
    image_path = ChooseImageFile()
    
    # Only proceed if a non-empty path was returned
    if image_path:
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Searching for information in the image roots...")
        GetAllExif(image_path)
    else:
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} No image file selected or path provided. Exiting.")
        
    Continue()
    Reset()
    
except Exception as e:
    # Catch any errors in the main execution block
    Error(e)