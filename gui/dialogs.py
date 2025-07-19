"""Dialog components for the pharmacy inventory GUI."""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from database.db_manager import DatabaseManager
from utils.validation import validate_product_data, validate_quantity
from gui.styles import COLORS, FONTS, SPACING, BUTTON_STYLES, INPUT_STYLES


class BaseDialog:
    """Base class for all dialogs with common functionality."""
    
    def __init__(self, parent: tk.Widget, title: str, width: int = 500, height: int = 400):
        """Initialize the base dialog."""
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry(f"{width}x{height}")
        self.dialog.minsize(400, 300)
        self.dialog.resizable(True, False)  # Allow horizontal resize only
        self.dialog.grab_set()  # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.configure(bg=COLORS['bg_primary'])
        
        # Center the dialog
        self._center_dialog()
        
        # Error label for displaying validation messages
        self.error_label = None
    
    def _center_dialog(self):
        """Center the dialog on the parent window."""
        self.dialog.update_idletasks()
        x = (self.parent.winfo_rootx() + self.parent.winfo_width() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.parent.winfo_rooty() + self.parent.winfo_height() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
    def show_error(self, message: str):
        """Display an error message."""
        if self.error_label:
            self.error_label.config(text=message, fg=COLORS['danger'])
    
    def clear_error(self):
        """Clear any displayed error message."""
        if self.error_label:
            self.error_label.config(text="")
    
    def close(self):
        """Close the dialog."""
        self.dialog.destroy()


class AddProductDialog(BaseDialog):
    """Dialog for adding new products to the inventory."""
    
    def __init__(self, parent: tk.Widget, db_manager: DatabaseManager, on_success: Callable):
        """Initialize the add product dialog."""
        super().__init__(parent, "Add New Drug", 500, 450)
        self.db_manager = db_manager
        self.on_success = on_success
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout the dialog widgets."""
        # Main container with padding
        main_container = tk.Frame(self.dialog, bg=COLORS['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=SPACING['xl'], pady=SPACING['lg'])
        
        # Header
        header_frame = tk.Frame(main_container, bg=COLORS['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, SPACING['lg']))
        
        # Title with icon
        title_label = tk.Label(
            header_frame, 
            text="+ Add New Drug", 
            font=FONTS['heading_medium'],
            fg=COLORS['primary'],
            bg=COLORS['bg_primary']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame, 
            text="Enter the details for the new pharmaceutical product", 
            font=FONTS['body_medium'],
            fg=COLORS['text_secondary'],
            bg=COLORS['bg_primary']
        )
        subtitle_label.pack(pady=(SPACING['xs'], 0))
        
        # Input section
        input_frame = tk.Frame(main_container, bg=COLORS['bg_primary'])
        input_frame.pack(fill=tk.X, pady=(0, SPACING['lg']))
        
        # Configure grid weights for better layout
        input_frame.columnconfigure(1, weight=1)
        
        # Name input
        tk.Label(input_frame, text="Drug Name *", 
                font=FONTS['body_large'], fg=COLORS['text_primary'], 
                bg=COLORS['bg_primary']).grid(row=0, column=0, sticky="w", pady=(0, SPACING['xs']))
        
        self.name_entry = tk.Entry(input_frame, **INPUT_STYLES['default'])
        self.name_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, SPACING['md']))
        
        # Price input
        tk.Label(input_frame, text="Price ($) *", 
                font=FONTS['body_large'], fg=COLORS['text_primary'], 
                bg=COLORS['bg_primary']).grid(row=2, column=0, sticky="w", pady=(0, SPACING['xs']))
        
        self.price_entry = tk.Entry(input_frame, **INPUT_STYLES['default'])
        self.price_entry.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, SPACING['md']))
        
        # Quantity input
        tk.Label(input_frame, text="Quantity *", 
                font=FONTS['body_large'], fg=COLORS['text_primary'], 
                bg=COLORS['bg_primary']).grid(row=4, column=0, sticky="w", pady=(0, SPACING['xs']))
        
        self.quantity_entry = tk.Entry(input_frame, **INPUT_STYLES['default'])
        self.quantity_entry.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, SPACING['sm']))
        
        # Required fields note
        req_label = tk.Label(
            input_frame, 
            text="* Required fields", 
            font=FONTS['body_small'],
            fg=COLORS['text_secondary'],
            bg=COLORS['bg_primary']
        )
        req_label.grid(row=6, column=0, sticky="w", pady=(SPACING['xs'], 0))
        
        # Error label
        self.error_label = tk.Label(
            main_container, 
            text="", 
            font=FONTS['body_medium'], 
            fg=COLORS['danger'],
            bg=COLORS['bg_primary'],
            wraplength=400
        )
        self.error_label.pack(pady=(0, SPACING['md']))
        
        # Buttons
        self._create_buttons(main_container)
        
        # Focus on name entry
        self.name_entry.focus_set()
    
    def _create_buttons(self, parent):
        """Create the dialog buttons."""
        button_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        button_frame.pack(fill=tk.X)
        
        # Center the buttons
        button_container = tk.Frame(button_frame, bg=COLORS['bg_primary'])
        button_container.pack()
        
        save_button = tk.Button(
            button_container, 
            text="Save Drug", 
            command=self._save_product,
            **BUTTON_STYLES['success']
        )
        save_button.pack(side=tk.LEFT, padx=(0, SPACING['md']))
        
        cancel_button = tk.Button(
            button_container, 
            text="Cancel", 
            command=self.close,
            **BUTTON_STYLES['danger']
        )
        cancel_button.pack(side=tk.LEFT)
    
    def _save_product(self):
        """Save the new product to the database."""
        try:
            # Get input values
            name = self.name_entry.get()
            price_str = self.price_entry.get()
            quantity_str = self.quantity_entry.get()
            
            # Validate inputs
            is_valid, error_msg, data = validate_product_data(name, price_str, quantity_str)
            if not is_valid:
                self.show_error(error_msg)
                return
            
            # Check if product already exists
            if self.db_manager.product_exists(data['name']):
                self.show_error("Drug already exists in inventory")
                return
            
            # Add product to database
            success = self.db_manager.add_product(data['name'], data['price'], data['quantity'])
            if not success:
                self.show_error("Failed to add product to database")
                return
            
            # Close dialog and refresh parent
            self.close()
            self.on_success()
            
        except Exception as e:
            self.show_error(f"Error: {str(e)}")


class ModifyQuantityDialog(BaseDialog):
    """Dialog for modifying product quantities."""
    
    def __init__(self, parent: tk.Widget, db_manager: DatabaseManager, on_success: Callable):
        """Initialize the modify quantity dialog."""
        super().__init__(parent, "Modify Drug Quantity", 500, 400)
        self.db_manager = db_manager
        self.on_success = on_success
        self.drug_var = tk.StringVar()
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout the dialog widgets."""
        # Main container with padding
        main_container = tk.Frame(self.dialog, bg=COLORS['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=SPACING['xl'], pady=SPACING['lg'])
        
        # Header
        header_frame = tk.Frame(main_container, bg=COLORS['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, SPACING['lg']))
        
        # Title with icon
        title_label = tk.Label(
            header_frame, 
            text="✎ Modify Drug Quantity", 
            font=FONTS['heading_medium'],
            fg=COLORS['primary'],
            bg=COLORS['bg_primary']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame, 
            text="Update the quantity of an existing pharmaceutical product", 
            font=FONTS['body_medium'],
            fg=COLORS['text_secondary'],
            bg=COLORS['bg_primary']
        )
        subtitle_label.pack(pady=(SPACING['xs'], 0))
        
        # Check for drugs
        drugs = self.db_manager.get_product_names()
        if not drugs:
            self._show_no_drugs_message(main_container)
            return
        
        # Input section
        input_frame = tk.Frame(main_container, bg=COLORS['bg_primary'])
        input_frame.pack(fill=tk.X, pady=(0, SPACING['lg']))
        
        # Configure grid weights
        input_frame.columnconfigure(1, weight=1)
        
        # Drug selection dropdown
        tk.Label(input_frame, text="Select Drug *", 
                font=FONTS['body_large'], fg=COLORS['text_primary'], 
                bg=COLORS['bg_primary']).grid(row=0, column=0, sticky="w", pady=(0, SPACING['xs']))
        
        self.drug_var.set(drugs[0])
        self.drug_dropdown = ttk.Combobox(
            input_frame, 
            textvariable=self.drug_var, 
            values=drugs,
            font=FONTS['body_large'], 
            state="readonly",
            width=35
        )
        self.drug_dropdown.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, SPACING['md']))
        
        # Current quantity display
        current_qty_frame = tk.Frame(input_frame, bg=COLORS['bg_accent'], relief='solid', bd=1)
        current_qty_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, SPACING['md']))
        current_qty_frame.columnconfigure(1, weight=1)
        
        tk.Label(current_qty_frame, text="Current Quantity:", 
                font=FONTS['body_large'], fg=COLORS['text_primary'], 
                bg=COLORS['bg_accent']).grid(row=0, column=0, sticky="w", padx=SPACING['md'], pady=SPACING['sm'])
        
        self.current_qty_label = tk.Label(
            current_qty_frame, 
            text="", 
            font=FONTS['heading_small'], 
            fg=COLORS['primary'],
            bg=COLORS['bg_accent']
        )
        self.current_qty_label.grid(row=0, column=1, sticky="e", padx=SPACING['md'], pady=SPACING['sm'])
        
        # New quantity input
        tk.Label(input_frame, text="New Quantity *", 
                font=FONTS['body_large'], fg=COLORS['text_primary'], 
                bg=COLORS['bg_primary']).grid(row=3, column=0, sticky="w", pady=(SPACING['md'], SPACING['xs']))
        
        self.quantity_entry = tk.Entry(input_frame, **INPUT_STYLES['default'])
        self.quantity_entry.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, SPACING['sm']))
        
        # Required fields note
        req_label = tk.Label(
            input_frame, 
            text="* Required fields", 
            font=FONTS['body_small'],
            fg=COLORS['text_secondary'],
            bg=COLORS['bg_primary']
        )
        req_label.grid(row=5, column=0, sticky="w", pady=(SPACING['xs'], 0))
        
        # Bind dropdown change event
        self.drug_var.trace('w', self._update_current_quantity)
        self._update_current_quantity()
        
        # Error label
        self.error_label = tk.Label(
            main_container, 
            text="", 
            font=FONTS['body_medium'], 
            fg=COLORS['danger'],
            bg=COLORS['bg_primary'],
            wraplength=400
        )
        self.error_label.pack(pady=(0, SPACING['md']))
        
        # Buttons
        self._create_buttons(main_container)
        
        # Focus on quantity entry
        self.quantity_entry.focus_set()
    
    def _show_no_drugs_message(self, parent_frame):
        """Show message when no drugs are available."""
        message_frame = tk.Frame(parent_frame, bg=COLORS['bg_primary'])
        message_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icon and message
        tk.Label(message_frame, text="⚠️", font=FONTS['heading_large'], 
                fg=COLORS['warning'], bg=COLORS['bg_primary']).pack(pady=SPACING['lg'])
        
        tk.Label(message_frame, text="No drugs found in inventory", 
                font=FONTS['body_large'], fg=COLORS['text_primary'], 
                bg=COLORS['bg_primary']).pack(pady=SPACING['sm'])
        
        tk.Label(message_frame, text="Add some products first before modifying quantities.", 
                font=FONTS['body_medium'], fg=COLORS['text_secondary'], 
                bg=COLORS['bg_primary']).pack(pady=SPACING['sm'])
        
        # Close button
        button_frame = tk.Frame(message_frame, bg=COLORS['bg_primary'])
        button_frame.pack(pady=SPACING['lg'])
        
        tk.Button(button_frame, text="Close", command=self.close, 
                 **BUTTON_STYLES['primary']).pack()
    
    def _update_current_quantity(self, *args):
        """Update the current quantity display when drug selection changes."""
        selected_drug = self.drug_var.get()
        if selected_drug:
            current_qty = self.db_manager.get_product_quantity(selected_drug)
            if current_qty is not None:
                self.current_qty_label.config(text=str(current_qty))
                self.quantity_entry.delete(0, tk.END)
                self.quantity_entry.insert(0, str(current_qty))
    
    def _create_buttons(self, parent):
        """Create the dialog buttons."""
        button_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        button_frame.pack(fill=tk.X)
        
        # Center the buttons
        button_container = tk.Frame(button_frame, bg=COLORS['bg_primary'])
        button_container.pack()
        
        save_button = tk.Button(
            button_container, 
            text="Update Quantity", 
            command=self._save_quantity,
            **BUTTON_STYLES['success']
        )
        save_button.pack(side=tk.LEFT, padx=(0, SPACING['md']))
        
        cancel_button = tk.Button(
            button_container, 
            text="Cancel", 
            command=self.close,
            **BUTTON_STYLES['danger']
        )
        cancel_button.pack(side=tk.LEFT)
    
    def _save_quantity(self):
        """Save the modified quantity to the database."""
        try:
            # Get input values
            selected_drug = self.drug_var.get()
            quantity_str = self.quantity_entry.get()
            
            # Validate inputs
            if not selected_drug:
                self.show_error("Please select a drug")
                return
                
            is_valid, error_msg, quantity = validate_quantity(quantity_str)
            if not is_valid:
                self.show_error(error_msg)
                return
            
            # Update quantity in database
            success = self.db_manager.update_product_quantity(selected_drug, quantity)
            if not success:
                self.show_error(f"Drug '{selected_drug}' not found")
                return
            
            # Close dialog and refresh parent
            self.close()
            self.on_success()
            
        except Exception as e:
            self.show_error(f"Error: {str(e)}")