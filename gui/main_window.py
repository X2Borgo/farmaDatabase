"""Main window component for the pharmacy inventory GUI."""

import tkinter as tk
from tkinter import ttk
from typing import Optional
from database.db_manager import DatabaseManager
from gui.dialogs import AddProductDialog, ModifyQuantityDialog
from gui.styles import COLORS, FONTS, SPACING, BUTTON_STYLES, TABLE_STYLE_CONFIG


class MainWindow:
    """Main window class for the pharmacy inventory application."""
    
    def __init__(self, title: str, db_manager: DatabaseManager):
        """Initialize the main window."""
        self.db_manager = db_manager
        self.sort_column = None
        self.sort_reverse = False
        self.root = tk.Tk()
        self._setup_window(title)
        self._create_widgets()
        self._setup_styles()
        self.refresh_display()
        
    def _setup_window(self, title: str):
        """Configure the main window properties."""
        self.root.title(title)
        self.root.geometry("1400x900")  # More standard size
        self.root.minsize(1200, 700)    # Allow resizing but set minimum
        self.root.resizable(True, True)  # Allow resizing for better UX
        self.root.configure(bg=COLORS['bg_primary'])  # Set modern background
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        
        # Center the window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self):
        """Create and layout all window widgets."""
        # Create main container with padding
        main_container = tk.Frame(self.root, bg=COLORS['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=SPACING['xl'], pady=SPACING['lg'])
        
        # Header section
        self._create_header(main_container)
        
        # Button frame
        self._create_button_frame(main_container)
        
        # Table frame and components
        self._create_table_frame(main_container)
    
    def _create_header(self, parent):
        """Create the header section with title and subtitle."""
        header_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, SPACING['xl']))
        
        # Main title
        title_label = tk.Label(
            header_frame, 
            text="Pharmacy Inventory Management", 
            font=FONTS['heading_large'],
            fg=COLORS['primary'],
            bg=COLORS['bg_primary']
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame, 
            text="Manage your pharmaceutical inventory efficiently", 
            font=FONTS['body_large'],
            fg=COLORS['text_secondary'],
            bg=COLORS['bg_primary']
        )
        subtitle_label.pack(pady=(SPACING['xs'], 0))
    
    def _create_button_frame(self, parent):
        """Create the frame containing action buttons."""
        button_container = tk.Frame(parent, bg=COLORS['bg_primary'])
        button_container.pack(fill=tk.X, pady=(0, SPACING['lg']))
        
        # Center the buttons
        button_frame = tk.Frame(button_container, bg=COLORS['bg_primary'])
        button_frame.pack()
        
        # Refresh button with icon (simplified for now)
        try:
            self.refresh = tk.PhotoImage(file="./icons/refresh-button.png")
            self.refresh_image = self.refresh.subsample(15, 15)  # Make icon smaller
            self.refresh_button = tk.Button(
                button_frame, 
                image=self.refresh_image,
                command=self.refresh_display,
                bg=COLORS['primary'],
                activebackground=COLORS['primary_dark'],
                relief='flat',
                borderwidth=0,
                cursor='hand2',
                padx=SPACING['md'],
                pady=SPACING['sm']
            )
            self.refresh_button.pack(side=tk.LEFT, padx=(0, SPACING['md']))
        except:
            # Fallback if icon doesn't exist
            self.refresh_button = tk.Button(
                button_frame, 
                text="⟳",  # Unicode refresh symbol
                command=self.refresh_display,
                **BUTTON_STYLES['primary']
            )
            self.refresh_button.pack(side=tk.LEFT, padx=(0, SPACING['md']))
        
        # Add drug button
        self.add_drug_button = tk.Button(
            button_frame, 
            text="+ Add Drug",
            command=self._show_add_dialog, 
            **BUTTON_STYLES['success']
        )
        self.add_drug_button.pack(side=tk.LEFT, padx=(0, SPACING['md']))
        
        # Modify quantity button
        self.modify_quantity_button = tk.Button(
            button_frame, 
            text="✎ Modify Quantity",
            command=self._show_modify_dialog, 
            **BUTTON_STYLES['info']
        )
        self.modify_quantity_button.pack(side=tk.LEFT)
    
    def _create_table_frame(self, parent):
        """Create the table and its container."""
        # Frame to hold the table with modern styling
        self.table_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        self.table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Table title
        table_title = tk.Label(
            self.table_frame, 
            text="Current Inventory", 
            font=FONTS['heading_small'],
            fg=COLORS['text_primary'],
            bg=COLORS['bg_primary']
        )
        table_title.pack(anchor='w', pady=(0, SPACING['sm']))
        
        # Create container for table and scrollbars
        table_container = tk.Frame(self.table_frame, bg=COLORS['bg_primary'])
        table_container.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview widget with modern styling
        columns = ("name", "price", "quantity")
        self.products_table = ttk.Treeview(table_container, columns=columns, show="headings")
        
        # Define column headings with sorting functionality
        self.products_table.heading("name", text="Product Name", 
                                   command=lambda: self._sort_by_column("name"))
        self.products_table.heading("price", text="Price ($)", 
                                   command=lambda: self._sort_by_column("price"))
        self.products_table.heading("quantity", text="Quantity", 
                                   command=lambda: self._sort_by_column("quantity"))
        
        # Configure column properties
        self._configure_columns()
        
        # Add scrollbars
        self._add_scrollbars(table_container)
        
        # Configure table selection
        self.products_table.configure(selectmode="browse")
    
    def _configure_columns(self):
        """Configure table column properties."""
        # Define column widths and alignment
        self.products_table.column("name", width=400, anchor="w")  # Left align for names
        self.products_table.column("price", width=150, anchor="center")
        self.products_table.column("quantity", width=150, anchor="center")
    
    def _add_scrollbars(self, container):
        """Add scrollbars to the table."""
        y_scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, 
                                   command=self.products_table.yview)
        x_scrollbar = ttk.Scrollbar(container, orient=tk.HORIZONTAL, 
                                   command=self.products_table.xview)
        
        self.products_table.configure(yscrollcommand=y_scrollbar.set, 
                                     xscrollcommand=x_scrollbar.set)
        
        # Grid layout
        self.products_table.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure the grid weights
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
    
    def _setup_styles(self):
        """Configure the visual styles for the table and other widgets."""
        style = ttk.Style()
        
        # Apply modern table styling
        for style_name, config in TABLE_STYLE_CONFIG.items():
            if 'configure' in config:
                style.configure(style_name, **config['configure'])
            if 'map' in config:
                style.map(style_name, **config['map'])
        
        # Configure scrollbar styles
        style.configure("Vertical.TScrollbar", 
                       troughcolor=COLORS['bg_secondary'],
                       background=COLORS['border'],
                       bordercolor=COLORS['border'],
                       arrowcolor=COLORS['text_secondary'],
                       darkcolor=COLORS['border'],
                       lightcolor=COLORS['bg_primary'])
        
        style.configure("Horizontal.TScrollbar", 
                       troughcolor=COLORS['bg_secondary'],
                       background=COLORS['border'],
                       bordercolor=COLORS['border'],
                       arrowcolor=COLORS['text_secondary'],
                       darkcolor=COLORS['border'],
                       lightcolor=COLORS['bg_primary'])
    
    def _sort_by_column(self, column: str):
        """Sort the table by the specified column."""
        # Toggle sort direction if clicking on the same column
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        
        # Update column headings to show sort direction
        self._update_column_headings()
        
        # Refresh the display with sorted data
        self.refresh_display()
    
    def _update_column_headings(self):
        """Update column headings to show sort indicators."""
        # Reset all headings
        self.products_table.heading("name", text="Product Name")
        self.products_table.heading("price", text="Price ($)")
        self.products_table.heading("quantity", text="Quantity")
        
        # Add sort indicator to the current sort column
        if self.sort_column:
            indicator = " ▲" if not self.sort_reverse else " ▼"
            column_titles = {
                "name": "Product Name",
                "price": "Price ($)",
                "quantity": "Quantity"
            }
            new_title = column_titles[self.sort_column] + indicator
            self.products_table.heading(self.sort_column, text=new_title)
    
    def refresh_display(self):
        """Refresh the table display with current database data."""
        # Clear existing items
        for item in self.products_table.get_children():
            self.products_table.delete(item)
        
        # Get sorted data from database
        rows = self.db_manager.get_all_products(self.sort_column, self.sort_reverse)
        
        # Insert new data
        for row in rows:
            self.products_table.insert("", tk.END, values=(row[0], f"${row[1]:.2f}", row[2]))
    
    def _show_add_dialog(self):
        """Show the add product dialog."""
        AddProductDialog(self.root, self.db_manager, self.refresh_display)
    
    def _show_modify_dialog(self):
        """Show the modify quantity dialog."""
        ModifyQuantityDialog(self.root, self.db_manager, self.refresh_display)
    
    def run(self):
        """Start the main event loop."""
        self.root.mainloop()
    
    def destroy(self):
        """Destroy the window and cleanup resources."""
        self.root.destroy()
        self.db_manager.close()