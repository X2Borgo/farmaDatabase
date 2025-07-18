import pandas as pd
import sqlite3
import os
from classes import Product, Window
import tkinter as tk

def connect_to_db(db_name):
    """Connect to the SQLite database."""
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
    
    pharmacy_inventory: list[Product] = [
        # Original list (15 items)
        Product(name='Lisinopril', price=25.99, quantity=120),
        Product(name='Atorvastatin', price=45.50, quantity=90),
        Product(name='Metformin', price=12.75, quantity=200),
        Product(name='Albuterol Inhaler', price=62.30, quantity=50),
        Product(name='Omeprazole', price=18.95, quantity=150),
        Product(name='Levothyroxine', price=22.40, quantity=110),
        Product(name='Simvastatin', price=28.60, quantity=85),
        Product(name='Losartan', price=32.25, quantity=95),
        Product(name='Acetaminophen', price=8.99, quantity=300),
        Product(name='Diphenhydramine', price=14.50, quantity=180),
        Product(name='Loratadine', price=16.75, quantity=160),
        Product(name='Hydrochlorothiazide', price=19.99, quantity=130),
        Product(name='Vitamin D3', price=11.25, quantity=240),
        Product(name='Melatonin', price=13.50, quantity=190),
        Product(name='Cetirizine', price=15.20, quantity=170),

        # New additions (15 more items)
        Product(name='Amoxicillin', price=27.80, quantity=75),
        Product(name='Azithromycin', price=38.90, quantity=60),
        Product(name='Ciprofloxacin', price=34.25, quantity=55),
        Product(name='Doxycycline', price=29.99, quantity=70),
        Product(name='Fluoxetine', price=21.50, quantity=100),
        Product(name='Sertraline', price=24.75, quantity=95),
        Product(name='Pantoprazole', price=19.45, quantity=120),
        Product(name='Montelukast', price=32.60, quantity=80),
        Product(name='Prednisone', price=15.80, quantity=110),
        Product(name='Tramadol', price=42.30, quantity=40),
        Product(name='Naproxen', price=10.99, quantity=200),
        Product(name='Ibuprofen', price=9.75, quantity=250),
        Product(name='Aspirin', price=7.50, quantity=300),
        Product(name='Calcium Carbonate', price=12.40, quantity=180),
        Product(name='Magnesium Supplement', price=14.90, quantity=150),
        Product(name='Multivitamin', price=16.25, quantity=170)
    ]

    insert_products(cursor, pharmacy_inventory)

    # Commit the changes
    conn.commit()

    root = Window("Pharmacy Inventory", conn)

    conn.close()

main()