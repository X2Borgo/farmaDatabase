#!/usr/bin/env python3
"""Integration test for the refactored pharmacy inventory system"""

import os
import sys
import tempfile
from database.db_manager import DatabaseManager
from data.sample_data import SAMPLE_PRODUCTS
from utils.validation import validate_product_data, validate_quantity
from classes import Product


def test_database_operations():
    """Test database manager functionality"""
    print("Testing DatabaseManager...")
    
    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
        test_db = tmp_file.name
    
    try:
        # Initialize database manager
        db_manager = DatabaseManager(test_db)
        
        # Test sample data insertion
        db_manager.insert_products(SAMPLE_PRODUCTS)
        products = db_manager.get_all_products()
        assert len(products) == len(SAMPLE_PRODUCTS), f"Expected {len(SAMPLE_PRODUCTS)} products, got {len(products)}"
        print(f"✓ Sample data inserted successfully ({len(products)} products)")
        
        # Test product addition
        success = db_manager.add_product("Test Drug", 15.99, 50)
        assert success, "Failed to add new product"
        print("✓ Product addition works")
        
        # Test duplicate detection
        success = db_manager.add_product("Test Drug", 15.99, 50)  # Same name
        assert not success, "Should not allow duplicate product"
        print("✓ Duplicate detection works")
        
        # Test quantity modification
        success = db_manager.update_product_quantity("Test Drug", 75)
        assert success, "Failed to update product quantity"
        new_qty = db_manager.get_product_quantity("Test Drug")
        assert new_qty == 75, f"Expected quantity 75, got {new_qty}"
        print("✓ Quantity modification works")
        
        # Test sorting
        sorted_by_name = db_manager.get_all_products("name", False)
        sorted_by_price = db_manager.get_all_products("price", True)
        assert len(sorted_by_name) == len(products) + 1, "Sorting should return all products"
        print("✓ Sorting functionality works")
        
        db_manager.close()
        print("✓ Database operations test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Database operations test failed: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists(test_db):
            os.unlink(test_db)


def test_validation_functions():
    """Test input validation utilities"""
    print("\nTesting validation utilities...")
    
    try:
        # Test valid product data
        valid, error, data = validate_product_data("Aspirin", "9.99", "100")
        assert valid and data['name'] == "Aspirin", "Valid product data should pass"
        print("✓ Valid product data validation works")
        
        # Test invalid product data
        invalid_cases = [
            ("", "9.99", "100"),  # Empty name
            ("Aspirin", "-1", "100"),  # Negative price
            ("Aspirin", "9.99", "-5"),  # Negative quantity
            ("Aspirin", "abc", "100"),  # Invalid price format
            ("Aspirin", "9.99", "abc"),  # Invalid quantity format
        ]
        
        for name, price, qty in invalid_cases:
            valid, error, data = validate_product_data(name, price, qty)
            assert not valid, f"Invalid data should fail: {name}, {price}, {qty}"
        print("✓ Invalid product data validation works")
        
        # Test quantity validation
        valid, error, qty = validate_quantity("50")
        assert valid and qty == 50, "Valid quantity should pass"
        print("✓ Quantity validation works")
        
        print("✓ Validation functions test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Validation functions test failed: {e}")
        return False


def test_product_class():
    """Test the Product class"""
    print("\nTesting Product class...")
    
    try:
        product = Product("Test Medicine", 25.50, 100)
        assert product.name == "Test Medicine", "Product name not set correctly"
        assert product.price == 25.50, "Product price not set correctly"
        assert product.quantity == 100, "Product quantity not set correctly"
        
        # Test quantity update
        product.update_quantity(50)
        assert product.quantity == 150, "Quantity update not working"
        print("✓ Product class works correctly")
        return True
        
    except Exception as e:
        print(f"✗ Product class test failed: {e}")
        return False


def main():
    """Run all integration tests"""
    print("=== INTEGRATION TESTS FOR REFACTORED PHARMACY INVENTORY ===\n")
    
    tests = [
        test_product_class,
        test_validation_functions,
        test_database_operations,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Refactoring successful!")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)