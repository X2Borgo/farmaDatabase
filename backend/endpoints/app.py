from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '../databases/inventory.db')

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'API is running'})

@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    """Get all inventory items"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM inventory')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify({'success': True, 'data': items})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/inventory', methods=['POST'])
def add_inventory_item():
    """Add new inventory item"""
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)',
            (data.get('name'), data.get('quantity'), data.get('price'))
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Item added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password_hash = ?',
                        (username, password)).fetchone()
    conn.close()

    if user:
        print(user)
        user_dict = dict(user)
        print(user_dict)
        return jsonify({
            'message': 'Login successful', 
            'token': 'fake-jwt-token',
            'username': user_dict['username'],
            'role': user_dict['role']
        }), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    role = request.json.get('role')

    print(f"Creating user: {username}, {email}, {role}")

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)', 
                    (username, email, password, role))
        conn.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Username already exists'}), 409
    finally:
        conn.close()

# For customers to place orders
@app.route('/api/orders', methods=['POST'])
def create_order():
    # Create a new order in the database
    # Return order ID and confirmation
    pass

# For customers to view their orders
@app.route('/api/orders/my', methods=['GET'])
def get_my_orders():
    # Get orders for the current user
    pass

# For pharmacists to view pending orders
@app.route('/api/orders/pending', methods=['GET'])
def get_pending_orders():
    # Get all pending orders
    pass

# For pharmacists to fulfill orders
@app.route('/api/orders/<int:order_id>/fulfill', methods=['POST'])
def fulfill_order(order_id):
    # Mark order as fulfilled
    # Update inventory quantities
    pass

# For pharmacists to reject orders
@app.route('/api/orders/<int:order_id>/reject', methods=['POST'])
def reject_order(order_id):
    # Mark order as rejected
    # Record rejection reason
    pass

# For practitioners to create prescriptions
@app.route('/api/prescriptions', methods=['POST'])
def create_prescription():
    # Create a new prescription
    pass

# For practitioners to view prescriptions
@app.route('/api/prescriptions', methods=['GET'])
def get_prescriptions():
    # Get prescriptions created by the current practitioner
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)