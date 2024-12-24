import tkinter as tk
from tkinter import ttk

# Color scheme
COLORS = {
    'primary': '#2196F3',  # Blue
    'secondary': '#FFC107',  # Amber
    'background': '#FFFFFF',  # White background for better contrast
    'text': '#000000',  # Black text for maximum readability
    'button_text': '#000000',  # Black text for buttons
    'button_hover': '#1976D2',  # Darker blue
    'success': '#4CAF50',  # Green
    'error': '#F44336'  # Red
}

def apply_modern_style():
    """Apply modern styling to ttk widgets"""
    style = ttk.Style()
    
    # Configure main window
    style.configure('.',
                   background=COLORS['background'],
                   foreground=COLORS['text'],
                   font=('Segoe UI', 10))
    
    # Configure frame
    style.configure('Modern.TFrame',
                   background=COLORS['background'])
    
    # Configure label
    style.configure('Modern.TLabel',
                   background=COLORS['background'],
                   foreground=COLORS['text'],
                   font=('Segoe UI', 10))
    
    # Configure button
    style.configure('Modern.TButton',
                   padding=(20, 10),
                   background='white',
                   foreground=COLORS['button_text'])
    
    # Button states
    style.map('Modern.TButton',
              foreground=[('pressed', COLORS['button_text']),
                         ('active', COLORS['button_text'])],
              background=[('pressed', '!disabled', 'white'),
                         ('active', 'white')])
    
    # Configure entry
    style.configure('Modern.TEntry',
                   fieldbackground='white',
                   foreground=COLORS['text'],
                   padding=5)
    
    # Configure progress bar
    style.configure('Modern.Horizontal.TProgressbar',
                   background=COLORS['primary'],
                   troughcolor='#E0E0E0')  # Light grey for progress bar background

def create_title_label(parent, text):
    """Create a styled title label"""
    label = ttk.Label(parent,
                     text=text,
                     style='Modern.TLabel',
                     font=('Segoe UI', 16, 'bold'))
    label.configure(foreground=COLORS['text'])  # Ensure text is visible
    return label

def create_button(parent, text, command):
    """Create a styled button"""
    btn = ttk.Button(parent,
                    text=text,
                    command=command,
                    style='Modern.TButton')
    return btn

def create_entry(parent):
    """Create a styled entry"""
    return ttk.Entry(parent, style='Modern.TEntry')
