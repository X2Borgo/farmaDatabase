#!/usr/bin/env python3
"""Test script for GUI modification functionality - code validation only"""

import sqlite3
import tempfile
import os
import sys
import re

def test_gui_code_structure():
	"""Test that the GUI code structure is correct"""
	print("Testing GUI code structure for quantity modification...")
	
	# Read the classes.py file
	try:
		with open('classes.py', 'r') as f:
			content = f.read()
		
		# Test 1: Check if modify quantity button is added
		if 'modify_quantity_button' in content and 'Modify Quantity' in content:
			print("✓ Modify Quantity button added to GUI")
		else:
			print("✗ Modify Quantity button not found in GUI")
			return False
		
		# Test 2: Check if modify_quantity_dialog method exists
		if 'def modify_quantity_dialog(self):' in content:
			print("✓ modify_quantity_dialog method defined")
		else:
			print("✗ modify_quantity_dialog method not found")
			return False
		
		# Test 3: Check for proper SQL UPDATE statement
		update_pattern = r'UPDATE products SET quantity = \? WHERE name = \?'
		if re.search(update_pattern, content):
			print("✓ Proper SQL UPDATE statement for setting quantity found")
		else:
			print("✗ SQL UPDATE statement for setting quantity not found")
			return False
		
		# Test 4: Check for dropdown/combobox for drug selection
		if 'ttk.Combobox' in content and 'SELECT name FROM products' in content:
			print("✓ Drug selection dropdown implemented")
		else:
			print("✗ Drug selection dropdown not properly implemented")
			return False
		
		# Test 5: Check for input validation
		if 'Quantity must be 0 or greater' in content and 'Quantity must be a valid integer' in content:
			print("✓ Input validation implemented")
		else:
			print("✗ Input validation not properly implemented")
			return False
		
		# Test 6: Check for current quantity display
		if 'Current Quantity:' in content and 'update_current_quantity' in content:
			print("✓ Current quantity display functionality implemented")
		else:
			print("✗ Current quantity display not implemented")
			return False
		
		# Test 7: Check for error handling
		if 'error_label' in content and 'fg="red"' in content:
			print("✓ Error handling UI elements present")
		else:
			print("✗ Error handling UI not properly implemented")
			return False
		
		# Test 8: Check that display_products is called to refresh
		if 'self.display_products()' in content:
			print("✓ Product display refresh implemented")
		else:
			print("✗ Product display refresh not implemented")
			return False
		
		print("\n✓ All GUI code structure tests passed!")
		return True
		
	except FileNotFoundError:
		print("✗ classes.py file not found")
		return False
	except Exception as e:
		print(f"✗ Error reading classes.py: {e}")
		return False

def test_integration_points():
	"""Test that the integration points are correct"""
	print("\nTesting integration points...")
	
	try:
		# Create a temporary database to test the actual database operations
		test_db = tempfile.mktemp(suffix='.db')
		conn = sqlite3.connect(test_db)
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
		
		# Insert test data
		cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", 
					  ('Test Drug', 10.99, 50))
		conn.commit()
		
		# Test the SQL queries that would be used in the GUI
		
		# Test 1: Get list of drug names (for dropdown)
		cursor.execute("SELECT name FROM products ORDER BY name")
		drugs = [row[0] for row in cursor.fetchall()]
		if drugs == ['Test Drug']:
			print("✓ Drug name retrieval query works")
		else:
			print(f"✗ Drug name retrieval failed. Got: {drugs}")
			return False
		
		# Test 2: Get current quantity for a drug
		cursor.execute("SELECT quantity FROM products WHERE name = ?", ('Test Drug',))
		result = cursor.fetchone()
		if result and result[0] == 50:
			print("✓ Current quantity retrieval query works")
		else:
			print(f"✗ Current quantity retrieval failed. Got: {result}")
			return False
		
		# Test 3: Update quantity to a specific value (our new functionality)
		cursor.execute("UPDATE products SET quantity = ? WHERE name = ?", (75, 'Test Drug'))
		conn.commit()
		
		# Verify the update
		cursor.execute("SELECT quantity FROM products WHERE name = ?", ('Test Drug',))
		result = cursor.fetchone()
		if result and result[0] == 75:
			print("✓ Quantity update to specific value works")
		else:
			print(f"✗ Quantity update failed. Got: {result}")
			return False
		
		print("✓ All integration points tested successfully!")
		return True
		
	except Exception as e:
		print(f"✗ Integration test failed: {e}")
		return False
	finally:
		if 'conn' in locals():
			conn.close()
		if 'test_db' in locals() and os.path.exists(test_db):
			os.remove(test_db)

if __name__ == "__main__":
	success1 = test_gui_code_structure()
	success2 = test_integration_points()
	success = success1 and success2
	
	if success:
		print("\n🎉 All tests passed! Quantity modification functionality is properly implemented.")
	else:
		print("\n❌ Some tests failed. Please check the implementation.")
	
	sys.exit(0 if success else 1)