"""Input validation utilities for the pharmacy inventory system."""

from typing import Tuple, Optional
from utils.config import MAX_NAME_LENGTH, MAX_PRICE, MAX_QUANTITY


def validate_product_name(name: str) -> Tuple[bool, Optional[str]]:
    """
    Validate product name input.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, "Drug name is required"
    
    if len(name.strip()) > MAX_NAME_LENGTH:
        return False, f"Drug name cannot exceed {MAX_NAME_LENGTH} characters"
    
    return True, None


def validate_price(price_str: str) -> Tuple[bool, Optional[str], Optional[float]]:
    """
    Validate and parse price input.
    
    Returns:
        Tuple of (is_valid, error_message, parsed_price)
    """
    if not price_str or not price_str.strip():
        return False, "Price is required", None
    
    try:
        price = float(price_str.strip())
        if price <= 0:
            return False, "Price must be greater than 0", None
        if price > MAX_PRICE:
            return False, "Price is too large", None
        return True, None, price
    except ValueError:
        return False, "Price must be a valid number", None


def validate_quantity(quantity_str: str) -> Tuple[bool, Optional[str], Optional[int]]:
    """
    Validate and parse quantity input.
    
    Returns:
        Tuple of (is_valid, error_message, parsed_quantity)
    """
    if not quantity_str or not quantity_str.strip():
        return False, "Quantity is required", None
    
    try:
        quantity = int(quantity_str.strip())
        if quantity < 0:
            return False, "Quantity must be 0 or greater", None
        if quantity > MAX_QUANTITY:
            return False, "Quantity is too large", None
        return True, None, quantity
    except ValueError:
        return False, "Quantity must be a valid integer", None


def validate_product_data(name: str, price_str: str, quantity_str: str) -> Tuple[bool, Optional[str], Optional[dict]]:
    """
    Validate all product data at once.
    
    Returns:
        Tuple of (is_valid, error_message, parsed_data_dict)
    """
    # Validate name
    name_valid, name_error = validate_product_name(name)
    if not name_valid:
        return False, name_error, None
    
    # Validate price
    price_valid, price_error, parsed_price = validate_price(price_str)
    if not price_valid:
        return False, price_error, None
    
    # Validate quantity
    quantity_valid, quantity_error, parsed_quantity = validate_quantity(quantity_str)
    if not quantity_valid:
        return False, quantity_error, None
    
    return True, None, {
        'name': name.strip(),
        'price': parsed_price,
        'quantity': parsed_quantity
    }