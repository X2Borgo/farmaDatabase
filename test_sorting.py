#!/usr/bin/env python3
"""Test script for table sorting functionality"""

import sqlite3
import os
import sys
from classes import Window

def test_sorting():
	"""Test the sorting functionality"""
	print("Testing table sorting functionality...")
	
	# Check if database exists
	if not os.path.exists('inventory.db'):
		print("ERROR: Database not found. Please run main.py first.")
		return False
	
	# Connect to database
	conn = sqlite3.connect('inventory.db')
	cursor = conn.cursor()
	
	# Test different sort queries
	test_cases = [
		("name", "ASC", "SELECT * FROM products ORDER BY name ASC"),
		("name", "DESC", "SELECT * FROM products ORDER BY name DESC"),
		("price", "ASC", "SELECT * FROM products ORDER BY price ASC"),
		("price", "DESC", "SELECT * FROM products ORDER BY price DESC"),
		("quantity", "ASC", "SELECT * FROM products ORDER BY quantity ASC"),
		("quantity", "DESC", "SELECT * FROM products ORDER BY quantity DESC"),
	]
	
	for column, direction, query in test_cases:
		print(f"\nTesting sort by {column} {direction}:")
		cursor.execute(query)
		rows = cursor.fetchall()
		
		# Show first 3 results
		for i, row in enumerate(rows[:3]):
			print(f"  {i+1}. {row[0]} - ${row[1]:.2f} - {row[2]}")
		
		# Verify sort order
		if column == "name":
			values = [row[0] for row in rows]
		elif column == "price":
			values = [row[1] for row in rows]
		elif column == "quantity":
			values = [row[2] for row in rows]
		
		if direction == "ASC":
			is_sorted = all(values[i] <= values[i+1] for i in range(len(values)-1))
		else:
			is_sorted = all(values[i] >= values[i+1] for i in range(len(values)-1))
		
		print(f"  Sort order correct: {is_sorted}")
		
		if not is_sorted:
			print("  ERROR: Sort order is incorrect!")
			return False
	
	conn.close()
	print("\nAll sorting tests passed!")
	return True

if __name__ == "__main__":
	success = test_sorting()
	sys.exit(0 if success else 1)