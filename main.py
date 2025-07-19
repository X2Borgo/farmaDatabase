"""
Pharmacy Inventory Management System - Main Application Entry Point

This module initializes the database, loads sample data, and starts the GUI application.
"""

from database.db_manager import DatabaseManager
from data.sample_data import SAMPLE_PRODUCTS
from gui.main_window import MainWindow


def initialize_database(db_manager: DatabaseManager):
    """Initialize the database with sample data if it's empty."""
    # Check if database has data already
    products = db_manager.get_all_products()
    if not products:
        # Insert sample products
        db_manager.insert_products(SAMPLE_PRODUCTS)
        print(f"Initialized database with {len(SAMPLE_PRODUCTS)} sample products")


def main():
    """Main application entry point."""
    try:
        # Initialize database manager
        db_manager = DatabaseManager('inventory.db')
        
        # Load sample data if needed
        initialize_database(db_manager)
        
        # Create and run the main window
        main_window = MainWindow("Pharmacy Inventory", db_manager)
        main_window.run()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()