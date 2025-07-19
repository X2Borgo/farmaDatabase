"""GUI utility functions for creating consistent UI components."""

import tkinter as tk


def create_styled_button(parent, text: str, command, bg_color: str = "#4CAF50", 
                        fg_color: str = "white", width: int = 10, font: tuple = ("Arial", 12)):
    """Create a consistently styled button."""
    return tk.Button(parent, text=text, command=command, font=font, 
                    bg=bg_color, fg=fg_color, width=width)


def create_labeled_entry(parent, label_text: str, row: int, font: tuple = ("Arial", 12), 
                        entry_width: int = 25) -> tk.Entry:
    """Create a label-entry pair and return the entry widget."""
    label = tk.Label(parent, text=label_text, font=font)
    label.grid(row=row, column=0, sticky="w", pady=5)
    
    entry = tk.Entry(parent, font=font, width=entry_width)
    entry.grid(row=row, column=1, pady=5, padx=10)
    
    return entry


def center_dialog(dialog, parent=None):
    """Center a dialog window on screen or on parent."""
    dialog.update_idletasks()
    
    if parent:
        # Center on parent window
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (dialog.winfo_height() // 2)
    else:
        # Center on screen
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
    
    dialog.geometry(f"+{x}+{y}")


def create_error_label(parent) -> tk.Label:
    """Create a standardized error label."""
    return tk.Label(parent, text="", font=("Arial", 10), fg="red")