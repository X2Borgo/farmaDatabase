import pandas as pd
import sqlite3
import os
from classes import Product

def connect_to_db(db_name):
    """Connect to the SQLite database."""
    if not os.path.exists(db_name):
        raise FileNotFoundError(f"Database {db_name} does not exist.")
    conn = sqlite3.connect(db_name)
    return conn

def insert_products(cursor, products: list[Product]):
    # Convert list of Product objects to list of dicts
    product_dicts = [product.__dict__ for product in products]
    pd.DataFrame(product_dicts).to_sql('products', con=cursor.connection, if_exists='replace', index=False)

def update_product_quantity(cursor, product_name: str, quantity: int):
    """Update the quantity of a product in the database."""
    cursor.execute("UPDATE products SET quantity = quantity + ? WHERE name = ?", (quantity, product_name))
    if cursor.rowcount == 0:
        raise ValueError(f"Product '{product_name}' not found in the database.")
    
def display_products(cursor):
    """Display all products in the database."""
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
def main_loop(conn, cursor):
    while True:
        print("\nOptions:")
        print("1. Update product quantity")
        print("2. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            product_name = input("Enter product name: ")
            quantity = int(input("Enter quantity to add (can be negative): "))
            try:
                update_product_quantity(cursor, product_name, quantity)
                conn.commit()
                display_products(cursor)
            except ValueError as e:
                print(e)
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    # Create a new SQLite database (or connect to an existing one)
    conn = connect_to_db('inventory.db')
    if conn is None:
        print("Failed to connect to the database.")
        return

    # Create a cursor object
    cursor = conn.cursor()
    
    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')

    # Commit the changes
    conn.commit()
    
    samples: list[Product] = [
        Product(name='aspirin', price=10.99, quantity=100),
        Product(name='ibuprofen', price=20.49, quantity=200),
        Product(name='paracetamol', price=15.75, quantity=150),
        Product(name='amoxicillin', price=30.00, quantity=80)
    ]

    insert_products(cursor, samples)

    # Commit the changes
    conn.commit()
    
    # read data from db
    display_products(cursor)

    main_loop(conn, cursor)

    conn.close()

main()