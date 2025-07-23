import sqlite3
import os

def init_database():
    """Initialize the database with basic tables"""
    db_path = os.path.join(os.path.dirname(__file__), '../databases/inventory.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create inventory table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create users table for authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

def read_inventory():
    """Read all inventory items"""
    db_path = os.path.join(os.path.dirname(__file__), '../databases/inventory.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM inventory')
    items = cursor.fetchall()
    
    conn.close()
    return items

if __name__ == '__main__':
    init_database()
    items = read_inventory()
    print(f"Found {len(items)} items in inventory")
    for item in items:
        print(item)