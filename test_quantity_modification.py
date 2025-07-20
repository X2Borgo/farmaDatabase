#!/usr/bin/env python3
"""Test script for quantity modification functionality"""

import sqlite3
import os
import sys
import tempfile
import pandas as pd

class Product:
	"""Simple Product class for testing"""
	def __init__(self, name: str, price: float, quantity: int = 0):
		self.name = name
		self.price = price
		self.quantity = quantity

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

def test_quantity_modification():
	"""Test the quantity modification functionality"""
	print("Testing quantity modification functionality...")
	
	# Create a temporary database for testing
	test_db = tempfile.mktemp(suffix='.db')
	
	try:
		# Connect to test database
		conn = connect_to_db(test_db)
		cursor = conn.cursor()
		
		# Create products table
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS products (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL,
				price REAL NOT NULL,
				quantity INTEGER NOT NULL
			)
		''')
		
		# Insert test products
		test_products = [
			Product(name='Test Drug A', price=10.99, quantity=50),
			Product(name='Test Drug B', price=25.50, quantity=75),
			Product(name='Test Drug C', price=15.25, quantity=100)
		]
		
		insert_products(cursor, test_products)
		conn.commit()
		
		print("✓ Test products inserted successfully")
		
		# Test 1: Modify quantity using existing function (adds to current quantity)
		print("\n--- Test 1: Update quantity using existing function ---")
		original_qty = cursor.execute("SELECT quantity FROM products WHERE name = 'Test Drug A'").fetchone()[0]
		print(f"Original quantity for Test Drug A: {original_qty}")
		
		# Add 25 to the quantity
		update_product_quantity(cursor, 'Test Drug A', 25)
		conn.commit()
		
		new_qty = cursor.execute("SELECT quantity FROM products WHERE name = 'Test Drug A'").fetchone()[0]
		print(f"New quantity after adding 25: {new_qty}")
		
		if new_qty == original_qty + 25:
			print("✓ Quantity update function works correctly")
		else:
			print(f"✗ Quantity update failed. Expected {original_qty + 25}, got {new_qty}")
			return False
		
		# Test 2: Set quantity to specific value (like our new GUI would do)
		print("\n--- Test 2: Set quantity to specific value ---")
		cursor.execute("UPDATE products SET quantity = ? WHERE name = ?", (80, 'Test Drug B'))
		conn.commit()
		
		updated_qty = cursor.execute("SELECT quantity FROM products WHERE name = 'Test Drug B'").fetchone()[0]
		print(f"Set Test Drug B quantity to: {updated_qty}")
		
		if updated_qty == 80:
			print("✓ Direct quantity update works correctly")
		else:
			print(f"✗ Direct quantity update failed. Expected 80, got {updated_qty}")
			return False
		
		# Test 3: Verify all products are retrievable
		print("\n--- Test 3: Verify product retrieval ---")
		cursor.execute("SELECT name, quantity FROM products ORDER BY name")
		all_products = cursor.fetchall()
		
		expected_products = [
			('Test Drug A', 75),  # Original 50 + 25
			('Test Drug B', 80),  # Set to 80
			('Test Drug C', 100)  # Unchanged
		]
		
		print("Current products in database:")
		for name, qty in all_products:
			print(f"  - {name}: {qty}")
		
		if all_products == expected_products:
			print("✓ All products retrieved correctly")
		else:
			print("✗ Product retrieval failed")
			print(f"Expected: {expected_products}")
			print(f"Got: {all_products}")
			return False
		
		# Test 4: Test error handling for non-existent product
		print("\n--- Test 4: Error handling for non-existent product ---")
		try:
			update_product_quantity(cursor, 'Non-existent Drug', 10)
			print("✗ Should have raised an error for non-existent product")
			return False
		except ValueError as e:
			print(f"✓ Correctly raised error: {e}")
		
		print("\n✓ All quantity modification tests passed!")
		return True
		
	except Exception as e:
		print(f"✗ Test failed with error: {e}")
		import traceback
		traceback.print_exc()
		return False
	finally:
		# Clean up
		if 'conn' in locals():
			conn.close()
		if os.path.exists(test_db):
			os.remove(test_db)

if __name__ == "__main__":
	success = test_quantity_modification()
	sys.exit(0 if success else 1)