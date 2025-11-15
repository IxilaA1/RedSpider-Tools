import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import time
import datetime  # Necessary for dates and timestamps in simulated content

# 1. Le logo en texte ASCII généré (exemple)
logo_ascii = """
                                                         ...                                       
                                                  +%@@@@@@@@@@@@@*.                                
                                               #@@@@@@@@@@@@@@@@@@@@@:                             
                                             %@@@@@@@@@@@@@@@@@@@@@@@@@:                           
                                           .@@@@@@@@@@@@@@@@@@@@@@@@@@@@:                          
                                           :@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                          
                                           =@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                          
                                           :@@@@@@@@@@@@@@@@@@@@@@@@@@@@*                          
                                            #@@@%.     .@@@@+      #@@@%                           
                                             +@@=      .@@@@=      .@@#                            
                                              @@@@00%@@@@%*@@@@00%@@@@=                            
                                             .@@@@@@@@@@*  -@@@@@@@@@@=                            
                                           .    .::-@@@@@@@@@@@@+::.    .                          
                                         *@@@@#     @@@@@@@@@@@@-    +@@@@@.                       
                                         #@@@@@0    -%@@@@@@@@%=.   *@@@@@@:                       
                                       @@@@@@@@@@@@:            .#@@@@@@@@@@@-                     
                                       +@@@@@*#@@@@@@@@*:  .+@@@@@@@@%*0@@@@#                      
                                                    *@@@@@@@@@@%.                                  
                                        .==.    .+%@@@@@@@%@@@@@@@+:     :=:                       
                                       @@@@@@@@@@@@@@*.       :@@@@@@@@@@@@@@=                     
                                       -@@@@@@@@%=                :#@@@@@@@@*                      
                                         *@@@@@:                     %@@@@@:                       
                                         :%@@%.                       *@@@=     
"""

# Nettoyer l'écran avant l'affichage (optionnel)
os.system('cls' if os.name == 'nt' else 'clear')

# Afficher le logo
print(logo_ascii)

# Petite pause avant le reste du script
time.sleep(2)

class RedSpiderForge:
    """
    # This is the main application (GUI) for forging information artifacts.
    """
    def __init__(self, master):
        self.master = master

        # Window Configuration
        master.title("RED SPIDER")
        master.geometry("500x500")  # Slight increase for new path labels
        master.resizable(False, False)

        # --- Style Configuration ---
        style = ttk.Style()
        style.theme_use('clam')
        BLACK_BG = '#1a1a1a'
        VIVID_RED_ACCENT = '#e53935'
        WHITE_FG = '#ffffff'
        DARK_GRAY_WIDGET = '#333333'

        style.configure('TFrame', background=BLACK_BG)
        style.configure('TLabel', background=BLACK_BG, foreground=WHITE_FG, font=('Consolas', 10))
        style.configure('TButton', background=VIVID_RED_ACCENT, foreground=WHITE_FG, font=('Consolas', 10, 'bold'), padding=[10, 5])
        style.map('TButton', background=[('active', '#ff6666')], foreground=[('active', BLACK_BG)])
        style.configure('TCombobox', fieldbackground=DARK_GRAY_WIDGET, foreground=WHITE_FG, selectbackground=VIVID_RED_ACCENT, selectforeground=WHITE_FG)
        style.configure('TEntry', fieldbackground=DARK_GRAY_WIDGET, foreground=WHITE_FG, insertcolor=VIVID_RED_ACCENT)

        self.frame = ttk.Frame(master, padding="15")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(self.frame, text="RED SPIDER VIRUS BUILDER", font=('Consolas', 18, 'bold'), foreground=VIVID_RED_ACCENT).pack(pady=20)

        # Script and Builder folder location
        try:
            # Gets the current script folder (e.g., .../parent/files/)
            self.initial_script_dir = os.path.dirname(os.path.abspath(sys.argv[0])) if not getattr(sys, 'frozen', False) else os.path.dirname(sys.executable)
        except:
            self.initial_script_dir = os.getcwd()

        # Parent directory
        parent_dir = os.path.dirname(self.initial_script_dir)

        # Builder folder path
        self.builder_dir = os.path.join(parent_dir, 'Builder')

        # Output folder is now YOURFILES in the parent folder
        self.output_dir = os.path.join(parent_dir, 'YOURFILES')

        # Create folders if they do not exist
        if not os.path.exists(self.builder_dir):
            os.makedirs(self.builder_dir)

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Variables and data
        # Artifact types updated to include extension
        self.artefact_types = [
            "Python Script (.py)",
            "Configuration File (.ini)",
            "Log File (.log)",
            "Text Document (.txt)",
            "Batch Script (.bat)",
            "Executable (.exe)"
        ]
        self.content_themes = ["KEYLOGGER (PY)", "MALWARE (BAT)", "RAD DISCORD (PY)", "MALWARE (PY)"]

        self.artefact_type_var = tk.StringVar(value=self.artefact_types[0])
        self.content_theme_var = tk.StringVar(value=self.content_themes[0])

        # Widgets
        ttk.Label(self.frame, text="Choose the Virus Type:").pack(anchor=tk.W, pady=(10, 5))
        ttk.Combobox(self.frame, textvariable=self.artefact_type_var, values=self.artefact_types, state="readonly", width=45).pack(anchor=tk.W, pady=5)

        ttk.Label(self.frame, text="Choose the Virus Content:").pack(anchor=tk.W, pady=(10, 5))
        ttk.Combobox(self.frame, textvariable=self.content_theme_var, values=self.content_themes, state="readonly", width=45).pack(anchor=tk.W, pady=5)

        ttk.Label(self.frame, text="File Name:").pack(anchor=tk.W, pady=(10, 5))
        self.file_name_entry = ttk.Entry(self.frame, width=45)
        self.file_name_entry.pack(anchor=tk.W, pady=5)
        self.file_name_entry.insert(0, "Virus")

        ttk.Button(self.frame, text="BUILD VIRUS", command=self.build_artefact).pack(pady=25)

        # Display paths
        ttk.Label(self.frame, text=f"Template folder: {self.builder_dir}", font=('Consolas', 8, 'italic'), foreground='#808080', background=BLACK_BG).pack(anchor=tk.W, pady=2)
        ttk.Label(self.frame, text=f"Output folder: {self.output_dir}", font=('Consolas', 8, 'italic'), foreground='#808080', background=BLACK_BG).pack(anchor=tk.W, pady=2)

    def _get_template_content(self, content_theme):
        """
        Finds and reads the content of the template file in the Builder folder.
        The file must START with the theme name (e.g., 'goat.py', 'goat_config.ini').
        """
        # Search for a file in the Builder folder that starts with the theme name
        theme_files = [f for f in os.listdir(self.builder_dir) if f.startswith(content_theme)]
        if not theme_files:
            raise FileNotFoundError(f"No template file found for theme '{content_theme}' in '{self.builder_dir}'.")
        template_file_name = theme_files[0]
        template_path = os.path.join(self.builder_dir, template_file_name)

        try:
            with open(template_path, "r", encoding="utf-8") as f:
                content = f.read()
            return content
        except Exception as e:
            raise IOError(f"Failed to read template file '{template_file_name}': {e}")

    def build_artefact(self):
        """
        Builds the artifact by copying the content of the selected template
        to the destination file.
        """
        base_name = self.file_name_entry.get().strip()
        if not base_name:
            messagebox.showerror("Build Error", "Please provide a name for your Virus.")
            return

        # Determine the extension from the artifact type
        artefact_type = self.artefact_type_var.get()
        try:
            extension_start = artefact_type.find("(")
            extension_end = artefact_type.find(")")
            extension = artefact_type[extension_start + 1:extension_end]
            if not extension.startswith('.'):
                extension = f".{extension}"
        except:
            extension = ""  # Safety fallback

        content_theme = self.content_theme_var.get()
        file_path = os.path.join(self.output_dir, base_name + extension)

        try:
            # Retrieve template content
            content = self._get_template_content(content_theme)
            # Write to file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content.strip())

            # Success message
            messagebox.showinfo("Virus Build!", f"The Virus '{base_name}{extension}' was successfully built using the '{content_theme}' template and is located here:\n{file_path}")
        except FileNotFoundError as e:
            messagebox.showerror("Build Error - Template Missing", str(e))
        except IOError as e:
            messagebox.showerror("Build Error - Read Error", str(e))
        except Exception as e:
            messagebox.showerror("Build Error", f"Failed to build Virus: {e}")

def main():
    root = tk.Tk()
    forge = RedSpiderForge(root)
    root.mainloop()

if __name__ == "__main__":
    main()