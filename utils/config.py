"""Configuration settings for the pharmacy inventory application."""

# Database settings
DEFAULT_DB_NAME = 'inventory.db'

# GUI settings
WINDOW_TITLE = "Pharmacy Inventory"
WINDOW_GEOMETRY = "1600x1000+1500+800"

# Button colors
BUTTON_COLORS = {
    'add': '#4CAF50',      # Green
    'modify': '#2196F3',   # Blue  
    'cancel': '#f44336',   # Red
    'save': '#4CAF50',     # Green
}

# Table settings
TABLE_COLUMNS = ("name", "price", "quantity")
COLUMN_WIDTHS = {
    "name": 300,
    "price": 150, 
    "quantity": 150
}

COLUMN_HEADINGS = {
    "name": "Product Name",
    "price": "Price ($)",
    "quantity": "Quantity"
}

# Font settings
FONTS = {
    'title': ("Arial", 20),
    'subtitle': ("Arial", 16, "bold"),
    'button': ("Arial", 16),
    'dialog_button': ("Arial", 12),
    'label': ("Arial", 12),
    'table': ("Arial", 16),
    'table_heading': ("Arial", 20, "bold"),
    'error': ("Arial", 10)
}

# Dialog settings
DIALOG_SIZE = {
    'add_product': (400, 300),
    'modify_quantity': (400, 300)
}

# Icons
ICON_PATH = "./icons/refresh-button.png"
ICON_SUBSAMPLE = (10, 10)

# Validation limits
MAX_NAME_LENGTH = 100
MAX_PRICE = 999999.99
MAX_QUANTITY = 999999