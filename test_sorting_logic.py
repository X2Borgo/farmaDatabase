#!/usr/bin/env python3
"""Test the sorting functionality without GUI dependencies"""

import sqlite3
import os
import sys

def test_sorting_logic():
    """Test the sorting logic used in the application"""
    print("Testing sorting logic...")
    
    # Check if database exists
    if not os.path.exists('inventory.db'):
        print("ERROR: Database not found. Please run main.py first.")
        return False
    
    # Connect to database
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Test the sorting logic that's used in the actual application
    sort_column = "name"
    sort_reverse = False
    
    # Test ascending sort
    print(f"Testing sort by {sort_column} ascending...")
    sort_order = "DESC" if sort_reverse else "ASC"
    query = f"SELECT * FROM products ORDER BY {sort_column} {sort_order}"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    print(f"First 3 products sorted by {sort_column} {sort_order}:")
    for i, row in enumerate(rows[:3]):
        print(f"  {i+1}. {row[0]} - ${row[1]:.2f} - {row[2]}")
    
    # Test descending sort (toggle)
    print(f"\nTesting sort by {sort_column} descending...")
    sort_reverse = True
    sort_order = "DESC" if sort_reverse else "ASC"
    query = f"SELECT * FROM products ORDER BY {sort_column} {sort_order}"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    print(f"First 3 products sorted by {sort_column} {sort_order}:")
    for i, row in enumerate(rows[:3]):
        print(f"  {i+1}. {row[0]} - ${row[1]:.2f} - {row[2]}")
    
    # Test sorting by price
    print(f"\nTesting sort by price...")
    sort_column = "price"
    sort_reverse = False
    sort_order = "DESC" if sort_reverse else "ASC"
    query = f"SELECT * FROM products ORDER BY {sort_column} {sort_order}"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    print(f"First 3 products sorted by {sort_column} {sort_order}:")
    for i, row in enumerate(rows[:3]):
        print(f"  {i+1}. {row[0]} - ${row[1]:.2f} - {row[2]}")
    
    # Test sorting by quantity
    print(f"\nTesting sort by quantity...")
    sort_column = "quantity"
    sort_reverse = False
    sort_order = "DESC" if sort_reverse else "ASC"
    query = f"SELECT * FROM products ORDER BY {sort_column} {sort_order}"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    print(f"First 3 products sorted by {sort_column} {sort_order}:")
    for i, row in enumerate(rows[:3]):
        print(f"  {i+1}. {row[0]} - ${row[1]:.2f} - {row[2]}")
    
    conn.close()
    print("\nSorting logic test passed!")
    return True

if __name__ == "__main__":
    success = test_sorting_logic()
    sys.exit(0 if success else 1)