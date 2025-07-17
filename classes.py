class Product:
	def __init__(self, name: str, price: float, quantity: int = 0):
		self.name = name
		self.price = price
		self.quantity = quantity
		
	def update_quantity(self, quantity: int):
		"""updates the product's quantity"""
		self.quantity += quantity