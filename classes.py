import tkinter as tk
from tkinter import ttk
import sqlite3
import pandas as pd

class Product:
	def __init__(self, name: str, price: float, quantity: int = 0):
		self.name = name
		self.price = price
		self.quantity = quantity
		
	def update_quantity(self, quantity: int):
		"""updates the product's quantity"""
		self.quantity += quantity

class Window:
	def __init__(self, title: str, conn: sqlite3.Connection):
		self.conn = conn
		self.sort_column = None
		self.sort_reverse = False
		self.create_window(title)
		self.root.mainloop()

	def create_window(self, title: str):
		"""creates a new window with the given title"""
		self.root = tk.Tk()
		self.root.title(title)
		self.root.geometry("1600x1000+1500+800")
		self.root.resizable(False, False)
		self.root.bind("<Escape>", lambda e: self.root.destroy())
		self.home()

	def home(self):
		"""home method to display the main window"""
		label = tk.Label(self.root, text="Welcome to the Pharmacy Inventory", font=("Arial", 20))
		label.pack(pady=20)
		
		# Button frame to hold refresh and add drug buttons
		button_frame = tk.Frame(self.root)
		button_frame.pack(pady=10)
		
		# Refresh button
		self.refresh = tk.PhotoImage(file="./icons/refresh-button.png")
		self.refreshImage = self.refresh.subsample(10, 10)
		self.display_products_button = tk.Button(button_frame, text="",
			command=self.display_products, font=("Arial", 20), image=self.refreshImage)
		self.display_products_button.pack(side=tk.LEFT, padx=5)
		
		# Add drug button
		self.add_drug_button = tk.Button(button_frame, text="Add Drug",
			command=self.add_drug_dialog, font=("Arial", 16), bg="#4CAF50", fg="white")
		self.add_drug_button.pack(side=tk.LEFT, padx=5)
		
		# Modify quantity button
		self.modify_quantity_button = tk.Button(button_frame, text="Modify Quantity",
			command=self.modify_quantity_dialog, font=("Arial", 16), bg="#2196F3", fg="white")
		self.modify_quantity_button.pack(side=tk.LEFT, padx=5)
		
		# Frame to hold the table
		self.table_frame = tk.Frame(self.root)
		self.table_frame.pack(pady=20, fill=tk.BOTH, expand=True)
		
		# Create Treeview widget
		columns = ("name", "price", "quantity")
		self.products_table = ttk.Treeview(self.table_frame, columns=columns, show="headings")
		
		# Define column headings with sorting functionality
		self.products_table.heading("name", text="Product Name", command=lambda: self.sort_by_column("name"))
		self.products_table.heading("price", text="Price ($)", command=lambda: self.sort_by_column("price"))
		self.products_table.heading("quantity", text="Quantity", command=lambda: self.sort_by_column("quantity"))
		
		# Define column widths
		self.products_table.column("name", width=300)
		self.products_table.column("price", width=150)
		self.products_table.column("quantity", width=150)
		
		# Add scrollbars
		y_scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.products_table.yview)
		x_scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL, command=self.products_table.xview)
		self.products_table.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
		
		# Grid layout (more control than pack)
		self.products_table.grid(row=0, column=0, sticky="nsew")
		y_scrollbar.grid(row=0, column=1, sticky="ns")
		x_scrollbar.grid(row=1, column=0, sticky="ew")
		
		# Configure the grid weights
		self.table_frame.rowconfigure(0, weight=1)
		self.table_frame.columnconfigure(0, weight=1)
		
		self.products_table.configure(selectmode="browse")
		# Set the style for the Treeview
		style = ttk.Style()
		style.configure("Treeview", rowheight=40, font=("Arial", 16), 
			background="#f0f0f0", foreground="#333333")
		style.configure("Treeview.Heading", font=("Arial", 20, "bold"))
		style.configure("Vertical.TScrollbar", troughcolor="#f0f0f0", background="#d9d9d9", bordercolor="#bfbfbf")
		style.configure("Horizontal.TScrollbar", troughcolor="#f0f0f0", background="#d9d9d9", bordercolor="#bfbfbf")
		# Add the Treeview to the frame
		self.products_table.config(style="Treeview")

		# Align text to the center for each column
		self.products_table.column("name", anchor="center")
		self.products_table.column("price", anchor="center")
		self.products_table.column("quantity", anchor="center")

		# Display the products
		self.display_products()

	def sort_by_column(self, column):
		"""Sort the table by the specified column"""
		# Toggle sort direction if clicking on the same column
		if self.sort_column == column:
			self.sort_reverse = not self.sort_reverse
		else:
			self.sort_column = column
			self.sort_reverse = False
		
		# Update column headings to show sort direction
		self.update_column_headings()
		
		# Refresh the display with sorted data
		self.display_products()
	
	def update_column_headings(self):
		"""Update column headings to show sort indicators"""
		# Reset all headings
		self.products_table.heading("name", text="Product Name")
		self.products_table.heading("price", text="Price ($)")
		self.products_table.heading("quantity", text="Quantity")
		
		# Add sort indicator to the current sort column
		if self.sort_column:
			indicator = " ▲" if not self.sort_reverse else " ▼"
			if self.sort_column == "name":
				self.products_table.heading("name", text="Product Name" + indicator)
			elif self.sort_column == "price":
				self.products_table.heading("price", text="Price ($)" + indicator)
			elif self.sort_column == "quantity":
				self.products_table.heading("quantity", text="Quantity" + indicator)

	def display_products(self):
		"""displays all products in the table"""
		# Clear existing items
		for item in self.products_table.get_children():
			self.products_table.delete(item)
		
		# Get data from database with sorting
		cursor = self.conn.cursor()
		
		# Build the SQL query with sorting
		if self.sort_column:
			sort_order = "DESC" if self.sort_reverse else "ASC"
			query = f"SELECT * FROM products ORDER BY {self.sort_column} {sort_order}"
		else:
			query = "SELECT * FROM products"
		
		cursor.execute(query)
		rows = cursor.fetchall()
		
		# Insert new data
		for row in rows:
			self.products_table.insert("", tk.END, values=(row[0], f"${row[1]:.2f}", row[2]))

	def add_drug_dialog(self):
		"""Open dialog to add a new drug to the inventory"""
		dialog = tk.Toplevel(self.root)
		dialog.title("Add New Drug")
		dialog.geometry("400x300")
		dialog.resizable(False, False)
		dialog.grab_set()  # Make dialog modal
		
		# Center the dialog on parent window
		dialog.transient(self.root)
		
		# Title label
		title_label = tk.Label(dialog, text="Add New Drug to Inventory", font=("Arial", 16, "bold"))
		title_label.pack(pady=20)
		
		# Input frame
		input_frame = tk.Frame(dialog)
		input_frame.pack(pady=10, padx=20, fill=tk.X)
		
		# Name input
		tk.Label(input_frame, text="Drug Name:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
		name_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
		name_entry.grid(row=0, column=1, pady=5, padx=10)
		
		# Price input
		tk.Label(input_frame, text="Price ($):", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
		price_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
		price_entry.grid(row=1, column=1, pady=5, padx=10)
		
		# Quantity input
		tk.Label(input_frame, text="Quantity:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
		quantity_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
		quantity_entry.grid(row=2, column=1, pady=5, padx=10)
		
		# Error label
		error_label = tk.Label(dialog, text="", font=("Arial", 10), fg="red")
		error_label.pack(pady=5)
		
		# Button frame
		button_frame = tk.Frame(dialog)
		button_frame.pack(pady=20)
		
		def save_drug():
			"""Save the new drug to the database"""
			try:
				# Get input values
				name = name_entry.get().strip()
				price_str = price_entry.get().strip()
				quantity_str = quantity_entry.get().strip()
				
				# Validate inputs
				if not name:
					error_label.config(text="Drug name is required")
					return
				if not price_str:
					error_label.config(text="Price is required")
					return
				if not quantity_str:
					error_label.config(text="Quantity is required")
					return
				
				# Convert and validate price
				try:
					price = float(price_str)
					if price <= 0:
						error_label.config(text="Price must be greater than 0")
						return
				except ValueError:
					error_label.config(text="Price must be a valid number")
					return
				
				# Convert and validate quantity
				try:
					quantity = int(quantity_str)
					if quantity < 0:
						error_label.config(text="Quantity must be 0 or greater")
						return
				except ValueError:
					error_label.config(text="Quantity must be a valid integer")
					return
				
				# Check if drug already exists
				cursor = self.conn.cursor()
				cursor.execute("SELECT name FROM products WHERE name = ?", (name,))
				if cursor.fetchone():
					error_label.config(text="Drug already exists in inventory")
					return
				
				# Insert new drug
				cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", 
					(name, price, quantity))
				self.conn.commit()
				
				# Close dialog and refresh table
				dialog.destroy()
				self.display_products()
				
			except Exception as e:
				error_label.config(text=f"Error: {str(e)}")
		
		def cancel():
			"""Cancel and close the dialog"""
			dialog.destroy()
		
		# Buttons
		save_button = tk.Button(button_frame, text="Save", command=save_drug, 
			font=("Arial", 12), bg="#4CAF50", fg="white", width=10)
		save_button.pack(side=tk.LEFT, padx=5)
		
		cancel_button = tk.Button(button_frame, text="Cancel", command=cancel, 
			font=("Arial", 12), bg="#f44336", fg="white", width=10)
		cancel_button.pack(side=tk.LEFT, padx=5)
		
		# Focus on name entry
		name_entry.focus_set()

	def modify_quantity_dialog(self):
		"""Open dialog to modify the quantity of an existing drug"""
		dialog = tk.Toplevel(self.root)
		dialog.title("Modify Drug Quantity")
		dialog.geometry("400x300")
		dialog.resizable(False, False)
		dialog.grab_set()  # Make dialog modal
		
		# Center the dialog on parent window
		dialog.transient(self.root)
		
		# Title label
		title_label = tk.Label(dialog, text="Modify Drug Quantity", font=("Arial", 16, "bold"))
		title_label.pack(pady=20)
		
		# Input frame
		input_frame = tk.Frame(dialog)
		input_frame.pack(pady=10, padx=20, fill=tk.X)
		
		# Drug selection dropdown
		tk.Label(input_frame, text="Select Drug:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
		
		# Get list of drugs from database
		cursor = self.conn.cursor()
		cursor.execute("SELECT name FROM products ORDER BY name")
		drugs = [row[0] for row in cursor.fetchall()]
		
		if not drugs:
			# No drugs available
			tk.Label(input_frame, text="No drugs found in inventory", font=("Arial", 12), fg="red").grid(row=0, column=1, pady=5, padx=10)
			tk.Button(dialog, text="Close", command=dialog.destroy, font=("Arial", 12), bg="#f44336", fg="white").pack(pady=20)
			return
		
		drug_var = tk.StringVar(value=drugs[0])
		drug_dropdown = ttk.Combobox(input_frame, textvariable=drug_var, values=drugs, 
			font=("Arial", 12), width=22, state="readonly")
		drug_dropdown.grid(row=0, column=1, pady=5, padx=10)
		
		# Current quantity display
		current_qty_label = tk.Label(input_frame, text="Current Quantity:", font=("Arial", 12))
		current_qty_label.grid(row=1, column=0, sticky="w", pady=5)
		current_qty_value = tk.Label(input_frame, text="", font=("Arial", 12), fg="blue")
		current_qty_value.grid(row=1, column=1, sticky="w", pady=5, padx=10)
		
		# New quantity input
		tk.Label(input_frame, text="New Quantity:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
		quantity_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
		quantity_entry.grid(row=2, column=1, pady=5, padx=10)
		
		def update_current_quantity(*args):
			"""Update the current quantity display when drug selection changes"""
			selected_drug = drug_var.get()
			if selected_drug:
				cursor = self.conn.cursor()
				cursor.execute("SELECT quantity FROM products WHERE name = ?", (selected_drug,))
				result = cursor.fetchone()
				if result:
					current_qty_value.config(text=str(result[0]))
					quantity_entry.delete(0, tk.END)
					quantity_entry.insert(0, str(result[0]))
		
		# Bind the function to dropdown selection change
		drug_var.trace('w', update_current_quantity)
		update_current_quantity()  # Initial update
		
		# Error label
		error_label = tk.Label(dialog, text="", font=("Arial", 10), fg="red")
		error_label.pack(pady=5)
		
		# Button frame
		button_frame = tk.Frame(dialog)
		button_frame.pack(pady=20)
		
		def save_quantity():
			"""Save the modified quantity to the database"""
			try:
				# Get input values
				selected_drug = drug_var.get()
				quantity_str = quantity_entry.get().strip()
				
				# Validate inputs
				if not selected_drug:
					error_label.config(text="Please select a drug")
					return
				if not quantity_str:
					error_label.config(text="Quantity is required")
					return
				
				# Convert and validate quantity
				try:
					new_quantity = int(quantity_str)
					if new_quantity < 0:
						error_label.config(text="Quantity must be 0 or greater")
						return
				except ValueError:
					error_label.config(text="Quantity must be a valid integer")
					return
				
				# Update quantity in database (set to new value, not add)
				cursor = self.conn.cursor()
				cursor.execute("UPDATE products SET quantity = ? WHERE name = ?", (new_quantity, selected_drug))
				
				if cursor.rowcount == 0:
					error_label.config(text=f"Drug '{selected_drug}' not found")
					return
				
				self.conn.commit()
				
				# Close dialog and refresh table
				dialog.destroy()
				self.display_products()
				
			except Exception as e:
				error_label.config(text=f"Error: {str(e)}")
		
		def cancel():
			"""Cancel and close the dialog"""
			dialog.destroy()
		
		# Buttons
		save_button = tk.Button(button_frame, text="Save", command=save_quantity, 
			font=("Arial", 12), bg="#4CAF50", fg="white", width=10)
		save_button.pack(side=tk.LEFT, padx=5)
		
		cancel_button = tk.Button(button_frame, text="Cancel", command=cancel, 
			font=("Arial", 12), bg="#f44336", fg="white", width=10)
		cancel_button.pack(side=tk.LEFT, padx=5)
		
		# Focus on quantity entry
		quantity_entry.focus_set()