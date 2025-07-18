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
		
		# Refresh button
		self.refresh = tk.PhotoImage(file="./icons/refresh-button.png")
		self.refreshImage = self.refresh.subsample(10, 10)
		self.display_products_button = tk.Button(self.root, text="",
			command=self.display_products, font=("Arial", 20), image=self.refreshImage)
		self.display_products_button.pack(pady=10)
		
		# Frame to hold the table
		self.table_frame = tk.Frame(self.root)
		self.table_frame.pack(pady=20, fill=tk.BOTH, expand=True)
		
		# Create Treeview widget
		columns = ("name", "price", "quantity")
		self.products_table = ttk.Treeview(self.table_frame, columns=columns, show="headings")
		
		# Define column headings
		self.products_table.heading("name", text="Product Name")
		self.products_table.heading("price", text="Price ($)")
		self.products_table.heading("quantity", text="Quantity")
		
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

	def display_products(self):
		"""displays all products in the table"""
		# Clear existing items
		for item in self.products_table.get_children():
			self.products_table.delete(item)
		
		# Get data from database
		cursor = self.conn.cursor()
		cursor.execute("SELECT * FROM products")
		rows = cursor.fetchall()
		
		# Insert new data
		for row in rows:
			self.products_table.insert("", tk.END, values=(row[0], f"${row[1]:.2f}", row[2]))