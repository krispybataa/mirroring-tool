import os
import sys
import shutil
import filecmp
from pathlib import Path
from tkinter import *
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from styles import apply_modern_style, COLORS, create_title_label, create_button

# Constants
def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # type: ignore
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

ICON_PATH = get_resource_path(os.path.join('resources', 'app_icon_final.ico'))
CONFIG_FILE = 'directory_config.json'

class ProgressWindow:
    def __init__(self, title="Copying Files"):
        self.window = tk.Toplevel()
        self.window.title(title)
        self.window.geometry("500x200")
        
        # Set icon
        if os.path.exists(ICON_PATH):
            self.window.iconbitmap(ICON_PATH)
        
        # Make it modal
        self.window.transient()
        self.window.grab_set()
        
        # Create main frame
        main_frame = ttk.Frame(self.window, style='Modern.TFrame', padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Current file label
        self.file_label = ttk.Label(main_frame, 
                                  text="Preparing...", 
                                  style='Modern.TLabel',
                                  wraplength=480)
        self.file_label.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, 
                                      length=400, 
                                      mode='determinate',
                                      style='Modern.Horizontal.TProgressbar')
        self.progress.pack(pady=15)
        
        # Stats label
        self.stats_label = ttk.Label(main_frame, 
                                   text="", 
                                   style='Modern.TLabel')
        self.stats_label.pack(pady=10)
        
        # Center the window
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def update(self, file_path, current, total):
        # Update file label
        self.file_label.config(text=f"Copying: {os.path.basename(file_path)}")
        
        # Update progress bar
        progress_percent = (current / total) * 100
        self.progress['value'] = progress_percent
        
        # Update stats
        self.stats_label.config(text=f"Progress: {current} of {total} files ({progress_percent:.1f}%)")
        
        # Force update
        self.window.update()
    
    def close(self):
        self.window.destroy()

def count_files(directory):
    """Count total number of files in directory and subdirectories."""
    total = 0
    for root, _, files in os.walk(directory):
        total += len(files)
    return total

def load_config():
    """Load directory configuration from JSON file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    """Save directory configuration to JSON file."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def select_directory(prompt, initial_dir=None):
    """Open a directory selection dialog."""
    directory = filedialog.askdirectory(title=prompt, initialdir=initial_dir)
    return directory if directory else None

def sync_folders(source, destination):
    if not os.path.exists(source):
        raise FileNotFoundError(f"Source directory not found: {source}")

    # Create progress window
    progress = ProgressWindow()
    
    try:
        # Count total files
        total_files = count_files(source)
        current_file = 0
        
        # Create destination folder if it doesn't exist
        Path(destination).mkdir(parents=True, exist_ok=True)

        for root, _, files in os.walk(source):
            relative_path = os.path.relpath(root, source)
            target_folder = os.path.join(destination, relative_path)

            Path(target_folder).mkdir(parents=True, exist_ok=True)

            for file in files:
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_folder, file)

                current_file += 1
                progress.update(source_file, current_file, total_files)

                if not os.path.exists(target_file) or not filecmp.cmp(source_file, target_file, shallow=False):
                    shutil.copy2(source_file, target_file)
    
    finally:
        progress.close()

class DirectorySelectionDialog:
    def __init__(self, mode, config):
        self.result = None
        self.config = config
        self.mode = mode  # Store mode for returning to main window
        
        # Create dialog window
        self.dialog = tk.Toplevel()
        self.dialog.title(f"{mode} - Select Directories")
        self.dialog.geometry("600x300")
        
        # Store reference to main window
        self.main_window = self.dialog.master
        
        # Set icon
        if os.path.exists(ICON_PATH):
            self.dialog.iconbitmap(ICON_PATH)
        
        # Make it modal
        self.dialog.transient()
        self.dialog.grab_set()
        
        # Create main frame
        main_frame = ttk.Frame(self.dialog, style='Modern.TFrame', padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add labels and entry fields
        title_label = create_title_label(main_frame, "Select Directories")
        title_label.pack(pady=(0, 20))
        
        # Directory frames
        if mode == "Work Mode":
            # Work directory frame
            self.work_var = tk.StringVar(value=config.get('work_dir', ''))
            work_frame = ttk.Frame(main_frame, style='Modern.TFrame')
            work_frame.pack(fill=tk.X, pady=5)
            ttk.Label(work_frame, text="Work Directory:", style='Modern.TLabel').pack(side=tk.LEFT, padx=5)
            ttk.Entry(work_frame, textvariable=self.work_var, style='Modern.TEntry', width=50).pack(side=tk.LEFT, padx=5)
            create_button(work_frame, "Browse", 
                         lambda: self.browse('work_dir', "Select Work Directory")).pack(side=tk.LEFT)
            
            # External drive frame
            self.external_var = tk.StringVar()
            external_frame = ttk.Frame(main_frame, style='Modern.TFrame')
            external_frame.pack(fill=tk.X, pady=5)
            ttk.Label(external_frame, text="External Drive (TO):", style='Modern.TLabel').pack(side=tk.LEFT, padx=5)
            ttk.Entry(external_frame, textvariable=self.external_var, style='Modern.TEntry', width=50).pack(side=tk.LEFT, padx=5)
            create_button(external_frame, "Browse",
                         lambda: self.browse('external_drive', "Select External Drive")).pack(side=tk.LEFT)
        else:
            # External drive frame
            self.external_var = tk.StringVar()
            external_frame = ttk.Frame(main_frame, style='Modern.TFrame')
            external_frame.pack(fill=tk.X, pady=5)
            ttk.Label(external_frame, text="External Drive (FROM):", style='Modern.TLabel').pack(side=tk.LEFT, padx=5)
            ttk.Entry(external_frame, textvariable=self.external_var, style='Modern.TEntry', width=50).pack(side=tk.LEFT, padx=5)
            create_button(external_frame, "Browse",
                         lambda: self.browse('external_drive', "Select External Drive")).pack(side=tk.LEFT)
            
            # Home directory frame
            self.home_var = tk.StringVar(value=config.get('home_dir', ''))
            home_frame = ttk.Frame(main_frame, style='Modern.TFrame')
            home_frame.pack(fill=tk.X, pady=5)
            ttk.Label(home_frame, text="Home Directory:", style='Modern.TLabel').pack(side=tk.LEFT, padx=5)
            ttk.Entry(home_frame, textvariable=self.home_var, style='Modern.TEntry', width=50).pack(side=tk.LEFT, padx=5)
            create_button(home_frame, "Browse",
                         lambda: self.browse('home_dir', "Select Home Directory")).pack(side=tk.LEFT)
        
        # Buttons
        button_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        button_frame.pack(pady=20)
        create_button(button_frame, "Next", self.next).pack(side=tk.LEFT, padx=5)
        create_button(button_frame, "Cancel", self.cancel).pack(side=tk.LEFT, padx=5)
        
        # Center the dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')

    def browse(self, var_name, prompt):
        initial_dir = None
        if var_name == 'work_dir':
            initial_dir = self.work_var.get() if os.path.exists(self.work_var.get()) else None
        elif var_name == 'home_dir':
            initial_dir = self.home_var.get() if os.path.exists(self.home_var.get()) else None
            
        directory = select_directory(prompt, initial_dir)
        if directory:
            if var_name == 'work_dir':
                self.work_var.set(directory)
            elif var_name == 'home_dir':
                self.home_var.set(directory)
            elif var_name == 'external_drive':
                self.external_var.set(directory)
    
    def next(self):
        # Validate entries
        if hasattr(self, 'work_var'):
            if not self.work_var.get() or not self.external_var.get():
                messagebox.showerror("Error", "Please select both directories")
                return
            self.result = {
                'source': self.work_var.get(),
                'destination': self.external_var.get()
            }
            self.config['work_dir'] = self.work_var.get()
        else:
            if not self.home_var.get() or not self.external_var.get():
                messagebox.showerror("Error", "Please select both directories")
                return
            self.result = {
                'source': self.external_var.get(),
                'destination': self.home_var.get()
            }
            self.config['home_dir'] = self.home_var.get()
        
        save_config(self.config)
        self.dialog.destroy()
        
    def cancel(self):
        self.result = None
        self.dialog.destroy()
        # Show main window again
        if self.main_window:
            self.main_window.deiconify()

class ConfirmationDialog:
    def __init__(self, source, destination, mode="work"):
        self.result = False
        self.mode = mode
        
        # Create dialog window
        self.dialog = tk.Toplevel()
        self.dialog.title("Confirm Directory Sync")
        self.dialog.geometry("500x450")
        
        # Store reference to previous window
        self.prev_window = self.dialog.master
        
        # Set icon
        if os.path.exists(ICON_PATH):
            self.dialog.iconbitmap(ICON_PATH)
        
        # Make it modal
        self.dialog.transient()
        self.dialog.grab_set()
        
        # Create main frame
        main_frame = ttk.Frame(self.dialog, style='Modern.TFrame', padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add title
        title_label = create_title_label(main_frame, "Confirm Directories")
        title_label.pack(pady=(0, 30))
        
        # Source directory frame
        source_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        source_frame.pack(fill=tk.X, pady=10)
        ttk.Label(source_frame, text="From:", style='Modern.TLabel', width=8).pack(side=tk.LEFT)
        ttk.Label(source_frame, text=source, style='Modern.TLabel', wraplength=400).pack(side=tk.LEFT)
        
        # Destination directory frame
        dest_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        dest_frame.pack(fill=tk.X, pady=10)
        ttk.Label(dest_frame, text="To:", style='Modern.TLabel', width=8).pack(side=tk.LEFT)
        ttk.Label(dest_frame, text=destination, style='Modern.TLabel', wraplength=400).pack(side=tk.LEFT)
        
        # Warning message
        if mode == "work":
            message = "Files will be copied FROM work directory TO external drive."
        else:
            message = "Files will be copied FROM external drive TO home directory."
        ttk.Label(main_frame, 
                 text=message, 
                 style='Modern.TLabel',
                 foreground=COLORS['primary']).pack(pady=30)
        
        # Buttons frame at the bottom
        button_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        button_frame.pack(side=tk.BOTTOM, pady=20)
        
        # Create buttons using tk.Button for consistent appearance
        confirm_button = tk.Button(
            button_frame,
            text="Confirm",
            command=self.confirm,
            font=('Segoe UI', 10),
            bg='white',
            fg='black',
            relief=tk.GROOVE,
            padx=20,
            pady=10
        )
        confirm_button.pack(side=tk.LEFT, padx=10)
        
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel,
            font=('Segoe UI', 10),
            bg='white',
            fg='black',
            relief=tk.GROOVE,
            padx=20,
            pady=10
        )
        cancel_button.pack(side=tk.LEFT, padx=10)
        
        # Center the dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
        
    def confirm(self):
        self.result = True
        self.dialog.destroy()
        
    def cancel(self):
        self.result = False
        self.dialog.destroy()
        # Return to the previous window
        if self.prev_window:
            self.prev_window.deiconify()

def work_mode(config):
    """Handle work mode: sync from work directory to external drive."""
    # First dialog: Select directories
    dir_dialog = DirectorySelectionDialog("Work Mode", config)
    dir_dialog.dialog.wait_window()
    
    if not dir_dialog.result:
        return False  # Return False if cancelled
        
    # Second dialog: Confirm directories
    confirm_dialog = ConfirmationDialog(dir_dialog.result['source'], 
                                      dir_dialog.result['destination'], "work")
    confirm_dialog.dialog.wait_window()
    
    if confirm_dialog.result:
        print(f"\nSyncing from Work ({dir_dialog.result['source']}) to External Drive ({dir_dialog.result['destination']})...")
        try:
            sync_folders(dir_dialog.result['source'], dir_dialog.result['destination'])
            messagebox.showinfo("Success", "Work files successfully synced to external drive!")
            return True  # Return True on successful sync
        except Exception as e:
            messagebox.showerror("Error", f"Sync failed: {str(e)}")
            return False
    return False  # Return False if cancelled

def home_mode(config):
    """Handle home mode: sync from external drive to home directory."""
    # First dialog: Select directories
    dir_dialog = DirectorySelectionDialog("Home Mode", config)
    dir_dialog.dialog.wait_window()
    
    if not dir_dialog.result:
        return False  # Return False if cancelled
        
    # Second dialog: Confirm directories
    confirm_dialog = ConfirmationDialog(dir_dialog.result['source'], 
                                      dir_dialog.result['destination'], "home")
    confirm_dialog.dialog.wait_window()
    
    if confirm_dialog.result:
        print(f"\nSyncing from External Drive ({dir_dialog.result['source']}) to Home ({dir_dialog.result['destination']})...")
        try:
            sync_folders(dir_dialog.result['source'], dir_dialog.result['destination'])
            messagebox.showinfo("Success", "External drive files successfully synced to home directory!")
            return True  # Return True on successful sync
        except Exception as e:
            messagebox.showerror("Error", f"Sync failed: {str(e)}")
            return False
    return False  # Return False if cancelled

def main():
    # Load existing configuration
    config = load_config()
    
    # Create root window for mode selection
    root = tk.Tk()
    root.title("ARMR Work-Home Mirror Tool")
    root.geometry("600x480")
    
    # Set icon
    if os.path.exists(ICON_PATH):
        root.iconbitmap(ICON_PATH)
    
    # Apply modern styling
    apply_modern_style()
    root.configure(bg=COLORS['background'])
    
    # Create main frame with padding
    main_frame = ttk.Frame(root, style='Modern.TFrame', padding="40")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    title_label = create_title_label(main_frame, "Select Mode")
    title_label.pack(pady=20)
    
    # Description
    description = ttk.Label(main_frame, 
                          text="Choose how you want to sync your files",
                          style='Modern.TLabel')
    description.configure(foreground=COLORS['text'])
    description.pack(pady=10)
    
    def work_click():
        root.withdraw()  # Hide main window
        if not work_mode(config):  # If work_mode returns False (cancelled)
            root.deiconify()  # Show main window again
        else:
            root.quit()  # Only quit if sync was successful
    
    def home_click():
        root.withdraw()  # Hide main window
        if not home_mode(config):  # If home_mode returns False (cancelled)
            root.deiconify()  # Show main window again
        else:
            root.quit()  # Only quit if sync was successful
    
    # Button frame
    button_frame = ttk.Frame(main_frame, style='Modern.TFrame')
    button_frame.pack(pady=30)
    
    # Create buttons
    work_button = tk.Button(
        button_frame,
        text="Work Mode\nSync TO External Drive",
        command=work_click,
        font=('Segoe UI', 10),
        bg='white',
        fg='black',
        relief=tk.GROOVE,
        padx=20,
        pady=10
    )
    work_button.pack(pady=15)
    
    home_button = tk.Button(
        button_frame,
        text="Home Mode\nSync FROM External Drive",
        command=home_click,
        font=('Segoe UI', 10),
        bg='white',
        fg='black',
        relief=tk.GROOVE,
        padx=20,
        pady=10
    )
    home_button.pack(pady=15)
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()