"""Main window component for the pharmacy inventory GUI."""

import tkinter as tk
from tkinter import ttk
from typing import Optional
from database.db_manager import DatabaseManager
from gui.dialogs import AddProductDialog, ModifyQuantityDialog


class MainWindow:
	"""Main window class for the pharmacy inventory application."""
	
	def __init__(self, title: str, db_manager: DatabaseManager):
		"""Initialize the main window."""
		self.db_manager = db_manager
		self.sort_column = None
		self.sort_reverse = False
		self.root = tk.Tk()
		self._setup_window(title)
		self._create_widgets()
		self._setup_styles()
		self.refresh_display()
		
	def _setup_window(self, title: str):
		"""Configure the main window properties."""
		self.root.title(title)
		self.root.geometry("1600x1000+1500+800")
		self.root.resizable(False, False)
		self.root.bind("<Escape>", lambda e: self.root.destroy())
	
	def _create_widgets(self):
		"""Create and layout all window widgets."""
		# Welcome label
		label = tk.Label(self.root, text="Welcome to the Pharmacy Inventory", font=("Arial", 20))
		label.pack(pady=20)
		
		# Button frame
		self._create_button_frame()
		
		# Table frame and components
		self._create_table_frame()
	
	def _create_button_frame(self):
		"""Create the frame containing action buttons."""
		button_frame = tk.Frame(self.root)
		button_frame.pack(pady=10)
		
		# Refresh button with icon
		self.refresh = tk.PhotoImage(file="./icons/refresh-button.png")
		self.refresh_image = self.refresh.subsample(10, 10)
		self.refresh_button = tk.Button(button_frame, text="", image=self.refresh_image,
			command=self.refresh_display, font=("Arial", 20))
		self.refresh_button.pack(side=tk.LEFT, padx=5)
		
		# Add drug button
		self.add_drug_button = tk.Button(button_frame, text="Add Drug",
										command=self._show_add_dialog, font=("Arial", 16), 
										bg="#4CAF50", fg="white")
		self.add_drug_button.pack(side=tk.LEFT, padx=5)
		
		# Modify quantity button
		self.modify_quantity_button = tk.Button(button_frame, text="Modify Quantity",
			command=self._show_modify_dialog, font=("Arial", 16), bg="#2196F3", fg="white")
		self.modify_quantity_button.pack(side=tk.LEFT, padx=5)
	
	def _create_table_frame(self):
		"""Create the table and its container."""
		# Frame to hold the table
		self.table_frame = tk.Frame(self.root)
		self.table_frame.pack(pady=20, fill=tk.BOTH, expand=True)
		
		# Create Treeview widget
		columns = ("name", "price", "quantity")
		self.products_table = ttk.Treeview(self.table_frame, columns=columns, show="headings")
		
		# Define column headings with sorting functionality
		self.products_table.heading("name", text="Product Name", 
			command=lambda: self._sort_by_column("name"))
		self.products_table.heading("price", text="Price ($)", 
			command=lambda: self._sort_by_column("price"))
		self.products_table.heading("quantity", text="Quantity", 
			command=lambda: self._sort_by_column("quantity"))
		
		# Configure column properties
		self._configure_columns()
		
		# Add scrollbars
		self._add_scrollbars()
		
		# Configure table selection
		self.products_table.configure(selectmode="browse")
	
	def _configure_columns(self):
		"""Configure table column properties."""
		# Define column widths
		self.products_table.column("name", width=300, anchor="center")
		self.products_table.column("price", width=150, anchor="center")
		self.products_table.column("quantity", width=150, anchor="center")
	
	def _add_scrollbars(self):
		"""Add scrollbars to the table."""
		y_scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, 
			command=self.products_table.yview)
		x_scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL, 
			command=self.products_table.xview)

		self.products_table.configure(yscrollcommand=y_scrollbar.set, 
			xscrollcommand=x_scrollbar.set)

		# Grid layout
		self.products_table.grid(row=0, column=0, sticky="nsew")
		y_scrollbar.grid(row=0, column=1, sticky="ns")
		x_scrollbar.grid(row=1, column=0, sticky="ew")
		
		# Configure the grid weights
		self.table_frame.rowconfigure(0, weight=1)
		self.table_frame.columnconfigure(0, weight=1)
	
	def _setup_styles(self):
		"""Configure the visual styles for the table."""
		style = ttk.Style()
		style.configure("Treeview", rowheight=40, font=("Arial", 16), 
			background="#f0f0f0", foreground="#333333")
		style.configure("Treeview.Heading", font=("Arial", 20, "bold"))
		style.configure("Vertical.TScrollbar", troughcolor="#f0f0f0", 
			background="#d9d9d9", bordercolor="#bfbfbf")
		style.configure("Horizontal.TScrollbar", troughcolor="#f0f0f0", 
			background="#d9d9d9", bordercolor="#bfbfbf")
	
	def _sort_by_column(self, column: str):
		"""Sort the table by the specified column."""
		# Toggle sort direction if clicking on the same column
		if self.sort_column == column:
			self.sort_reverse = not self.sort_reverse
		else:
			self.sort_column = column
			self.sort_reverse = False
		
		# Update column headings to show sort direction
		self._update_column_headings()
		
		# Refresh the display with sorted data
		self.refresh_display()
	
	def _update_column_headings(self):
		"""Update column headings to show sort indicators."""
		# Reset all headings
		self.products_table.heading("name", text="Product Name")
		self.products_table.heading("price", text="Price ($)")
		self.products_table.heading("quantity", text="Quantity")
		
		# Add sort indicator to the current sort column
		if self.sort_column:
			indicator = " ▲" if not self.sort_reverse else " ▼"
			column_titles = {
				"name": "Product Name",
				"price": "Price ($)",
				"quantity": "Quantity"
			}
			new_title = column_titles[self.sort_column] + indicator
			self.products_table.heading(self.sort_column, text=new_title)
	
	def refresh_display(self):
		"""Refresh the table display with current database data."""
		# Clear existing items
		for item in self.products_table.get_children():
			self.products_table.delete(item)
		
		# Get sorted data from database
		rows = self.db_manager.get_all_products(self.sort_column, self.sort_reverse)
		
		# Insert new data
		for row in rows:
			self.products_table.insert("", tk.END, values=(row[0], f"${row[1]:.2f}", row[2]))
	
	def _show_add_dialog(self):
		"""Show the add product dialog."""
		AddProductDialog(self.root, self.db_manager, self.refresh_display)
	
	def _show_modify_dialog(self):
		"""Show the modify quantity dialog."""
		ModifyQuantityDialog(self.root, self.db_manager, self.refresh_display)
	
	def run(self):
		"""Start the main event loop."""
		self.root.mainloop()
	
	def destroy(self):
		"""Destroy the window and cleanup resources."""
		self.root.destroy()
		self.db_manager.close()