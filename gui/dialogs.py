"""Dialog components for the pharmacy inventory GUI."""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from database.db_manager import DatabaseManager
from utils.validation import validate_product_data, validate_quantity


class BaseDialog:
    """Base class for all dialogs with common functionality."""
    
    def __init__(self, parent: tk.Widget, title: str, width: int = 400, height: int = 300):
        """Initialize the base dialog."""
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry(f"{width}x{height}")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()  # Make dialog modal
        self.dialog.transient(parent)
        
        # Error label for displaying validation messages
        self.error_label = None
        
    def show_error(self, message: str):
        """Display an error message."""
        if self.error_label:
            self.error_label.config(text=message)
    
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
        super().__init__(parent, "Add New Drug", 400, 300)
        self.db_manager = db_manager
        self.on_success = on_success
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout the dialog widgets."""
        # Title label
        title_label = tk.Label(self.dialog, text="Add New Drug to Inventory", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Input frame
        input_frame = tk.Frame(self.dialog)
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Name input
        tk.Label(input_frame, text="Drug Name:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
        self.name_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Price input
        tk.Label(input_frame, text="Price ($):", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.price_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
        self.price_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Quantity input
        tk.Label(input_frame, text="Quantity:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.quantity_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
        self.quantity_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # Error label
        self.error_label = tk.Label(self.dialog, text="", font=("Arial", 10), fg="red")
        self.error_label.pack(pady=5)
        
        # Buttons
        self._create_buttons()
        
        # Focus on name entry
        self.name_entry.focus_set()
    
    def _create_buttons(self):
        """Create the dialog buttons."""
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=20)
        
        save_button = tk.Button(button_frame, text="Save", command=self._save_product, 
                               font=("Arial", 12), bg="#4CAF50", fg="white", width=10)
        save_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.close, 
                                 font=("Arial", 12), bg="#f44336", fg="white", width=10)
        cancel_button.pack(side=tk.LEFT, padx=5)
    
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
        super().__init__(parent, "Modify Drug Quantity", 400, 300)
        self.db_manager = db_manager
        self.on_success = on_success
        self.drug_var = tk.StringVar()
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout the dialog widgets."""
        # Title label
        title_label = tk.Label(self.dialog, text="Modify Drug Quantity", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Input frame
        input_frame = tk.Frame(self.dialog)
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Get drugs from database
        drugs = self.db_manager.get_product_names()
        if not drugs:
            self._show_no_drugs_message(input_frame)
            return
        
        # Drug selection dropdown
        tk.Label(input_frame, text="Select Drug:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.drug_var.set(drugs[0])
        self.drug_dropdown = ttk.Combobox(input_frame, textvariable=self.drug_var, values=drugs, 
                                         font=("Arial", 12), width=22, state="readonly")
        self.drug_dropdown.grid(row=0, column=1, pady=5, padx=10)
        
        # Current quantity display
        tk.Label(input_frame, text="Current Quantity:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.current_qty_label = tk.Label(input_frame, text="", font=("Arial", 12), fg="blue")
        self.current_qty_label.grid(row=1, column=1, sticky="w", pady=5, padx=10)
        
        # New quantity input
        tk.Label(input_frame, text="New Quantity:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.quantity_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
        self.quantity_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # Bind dropdown change event
        self.drug_var.trace('w', self._update_current_quantity)
        self._update_current_quantity()
        
        # Error label
        self.error_label = tk.Label(self.dialog, text="", font=("Arial", 10), fg="red")
        self.error_label.pack(pady=5)
        
        # Buttons
        self._create_buttons()
        
        # Focus on quantity entry
        self.quantity_entry.focus_set()
    
    def _show_no_drugs_message(self, parent_frame):
        """Show message when no drugs are available."""
        tk.Label(parent_frame, text="No drugs found in inventory", 
                font=("Arial", 12), fg="red").grid(row=0, column=1, pady=5, padx=10)
        tk.Button(self.dialog, text="Close", command=self.close, 
                 font=("Arial", 12), bg="#f44336", fg="white").pack(pady=20)
    
    def _update_current_quantity(self, *args):
        """Update the current quantity display when drug selection changes."""
        selected_drug = self.drug_var.get()
        if selected_drug:
            current_qty = self.db_manager.get_product_quantity(selected_drug)
            if current_qty is not None:
                self.current_qty_label.config(text=str(current_qty))
                self.quantity_entry.delete(0, tk.END)
                self.quantity_entry.insert(0, str(current_qty))
    
    def _create_buttons(self):
        """Create the dialog buttons."""
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=20)
        
        save_button = tk.Button(button_frame, text="Save", command=self._save_quantity, 
                               font=("Arial", 12), bg="#4CAF50", fg="white", width=10)
        save_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.close, 
                                 font=("Arial", 12), bg="#f44336", fg="white", width=10)
        cancel_button.pack(side=tk.LEFT, padx=5)
    
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