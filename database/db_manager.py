import sqlite3
import pandas as pd
from typing import List, Optional, Tuple


class DatabaseManager:
    """Handles all database operations for the pharmacy inventory system."""
    
    def __init__(self, db_name: str = 'inventory.db'):
        """Initialize database connection and create tables if needed."""
        self.db_name = db_name
        self.conn = None
        self.connect()
        self.create_tables()
    
    def connect(self) -> sqlite3.Connection:
        """Connect to the SQLite database."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn
    
    def create_tables(self):
        """Create the products table if it doesn't exist."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')
        self.conn.commit()
    
    def insert_products(self, products: List[dict]):
        """Insert multiple products into the database."""
        df = pd.DataFrame(products)
        df.to_sql('products', con=self.conn, if_exists='replace', index=False)
        self.conn.commit()
    
    def add_product(self, name: str, price: float, quantity: int) -> bool:
        """Add a single product to the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", 
                          (name, price, quantity))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update_product_quantity(self, product_name: str, new_quantity: int) -> bool:
        """Update the quantity of a product in the database."""
        cursor = self.conn.cursor()
        cursor.execute("UPDATE products SET quantity = ? WHERE name = ?", 
                      (new_quantity, product_name))
        success = cursor.rowcount > 0
        self.conn.commit()
        return success
    
    def get_all_products(self, sort_column: Optional[str] = None, sort_reverse: bool = False) -> List[Tuple]:
        """Get all products from the database with optional sorting."""
        cursor = self.conn.cursor()
        
        if sort_column and sort_column in ['name', 'price', 'quantity']:
            sort_order = "DESC" if sort_reverse else "ASC"
            query = f"SELECT name, price, quantity FROM products ORDER BY {sort_column} {sort_order}"
        else:
            query = "SELECT name, price, quantity FROM products"
        
        cursor.execute(query)
        return cursor.fetchall()
    
    def get_product_names(self) -> List[str]:
        """Get a list of all product names."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM products ORDER BY name")
        return [row[0] for row in cursor.fetchall()]
    
    def get_product_quantity(self, product_name: str) -> Optional[int]:
        """Get the current quantity of a specific product."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT quantity FROM products WHERE name = ?", (product_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def product_exists(self, product_name: str) -> bool:
        """Check if a product exists in the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM products WHERE name = ?", (product_name,))
        return cursor.fetchone() is not None
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None