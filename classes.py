"""Product data model for the pharmacy inventory system."""


class Product:
	"""Simple product data model."""
	
	def __init__(self, name: str, price: float, quantity: int = 0):
		"""Initialize a product with name, price, and quantity."""
		self.name = name
		self.price = price
		self.quantity = quantity
		
	def update_quantity(self, quantity: int):
		"""Update the product's quantity by adding the given amount."""
		self.quantity += quantity
		
	def __dict__(self):
		"""Return product data as dictionary for database operations."""
		return {
			'name': self.name,
			'price': self.price,
			'quantity': self.quantity
		}