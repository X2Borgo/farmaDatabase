#!/usr/bin/env python3
"""Test the GUI application without displaying it"""

import tkinter as tk
import sqlite3
import os
from classes import Window

def test_gui_functionality():
	"""Test the GUI window creation and sorting functionality"""
	print("Testing GUI functionality...")
	
	# Check if database exists
	if not os.path.exists('inventory.db'):
		print("ERROR: Database not found. Please run main.py first.")
		return False
	
	# Connect to database
	conn = sqlite3.connect('inventory.db')
	
	# Create a root window but don't display it
	root = tk.Tk()
	root.withdraw()  # Hide the window
	
	try:
		# Create the window instance but modify it to not run mainloop
		from classes import Window
		
		# Create a test window to check the sorting functionality
		test_window = TestWindow("Test Pharmacy Inventory", conn)
		
		# Test sorting functionality
		print("Testing sort by name...")
		test_window.sort_by_column("name")
		
		print("Testing sort by price...")
		test_window.sort_by_column("price")
		
		print("Testing sort by quantity...")
		test_window.sort_by_column("quantity")
		
		# Test toggle sorting
		print("Testing sort toggle...")
		test_window.sort_by_column("name")  # Should reverse
		
		print("GUI functionality test passed!")
		return True
		
	except Exception as e:
		print(f"ERROR: {e}")
		return False
	finally:
		conn.close()
		root.destroy()

class TestWindow(Window):
	"""Test version of Window that doesn't run mainloop"""
	def __init__(self, title: str, conn: sqlite3.Connection):
		self.conn = conn
		self.sort_column = None
		self.sort_reverse = False
		self.create_window(title)
		# Don't call mainloop() for testing

if __name__ == "__main__":
	success = test_gui_functionality()
	exit(0 if success else 1)