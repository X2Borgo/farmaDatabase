// Home page functionality
function renderHomePage() {
    const content = document.getElementById('content');
    
    // Get user data from localStorage
    let userInfo = '';
    let roleSpecificActions = '';
    const userToken = localStorage.getItem('token');
    
    if (userToken) {
        try {
            const userData = JSON.parse(userToken);
            const role = userData.role || 'N/A';
            
            userInfo = `
                <div class="card mb-1">
                    <div class="user-info">
                        <h3>Welcome, ${userData.username}</h3>
                        <p>Role: ${role}</p>
                    </div>
                </div>
            `;
            
            // Role-specific action buttons
            switch(role) {
                case 'customer':
                    roleSpecificActions = `
                        <button class="btn" onclick="showInventory()">View Medications</button>
                        <button class="btn btn-primary" onclick="navigateTo('order')">Place New Order</button>
                        <button class="btn" onclick="navigateTo('my-orders')">View My Orders</button>
                    `;
                    break;
                case 'pharmacist':
                    roleSpecificActions = `
                        <button class="btn" onclick="showInventory()">View Inventory</button>
                        <button class="btn btn-success" onclick="showAddItemForm()">Add New Item</button>
                        <button class="btn btn-primary" onclick="navigateTo('pending-orders')">Manage Orders</button>
                    `;
                    break;
                case 'practitioner':
                    roleSpecificActions = `
                        <button class="btn" onclick="showInventory()">View Medications</button>
                        <button class="btn btn-primary" onclick="navigateTo('create-prescription')">Create Prescription</button>
                        <button class="btn" onclick="navigateTo('prescriptions')">View Prescriptions</button>
                    `;
                    break;
                default:
                    roleSpecificActions = `
                        <button class="btn" onclick="showInventory()">View Inventory</button>
                    `;
            }
        } catch (e) {
            console.error('Error parsing user data', e);
        }
    }
    
    content.innerHTML = `
        ${userInfo}
        <div class="card">
            <h1>Welcome to My Little Farma</h1>
            <p>Manage your pharmacy inventory with ease.</p>
            
            <div class="mt-1">
                <h3>Quick Actions</h3>
                ${roleSpecificActions}
            </div>
        </div>
        
        <div id="inventory-section" class="card" style="display: none;">
            <h3>Current Inventory</h3>
            <div id="inventory-list">Loading...</div>
        </div>
        
        <!-- Only show for pharmacists -->
        <div id="add-item-section" class="card" style="display: none;">
            <h3>Add New Item</h3>
            <form id="add-item-form">
                <div class="form-group">
                    <label for="item-name">Item Name</label>
                    <input type="text" id="item-name" name="name" required>
                </div>
                <div class="form-group">
                    <label for="item-quantity">Quantity</label>
                    <input type="number" id="item-quantity" name="quantity" required>
                </div>
                <div class="form-group">
                    <label for="item-price">Price</label>
                    <input type="number" id="item-price" name="price" step="0.01" required>
                </div>
                <button type="submit" class="btn btn-success">Add Item</button>
                <button type="button" class="btn" onclick="hideAddItemForm()">Cancel</button>
            </form>
        </div>
    `;
    
    // Set up form handler for pharmacists only
    const form = document.getElementById('add-item-form');
    if (form) {
        form.addEventListener('submit', handleAddItem);
    }
    
    // Hide the add form by default for non-pharmacists
    if (userToken) {
        const userData = JSON.parse(userToken);
        if (userData.role !== 'pharmacist') {
            const addItemSection = document.getElementById('add-item-section');
            if (addItemSection) {
                addItemSection.style.display = 'none';
            }
        }
    }
}

function showInventory() {
    const section = document.getElementById('inventory-section');
    const listContainer = document.getElementById('inventory-list');
    section.style.display = 'block';
    listContainer.innerHTML = 'Loading...';
    InventoryAPI.getAll().then(response => {
        if (response.success) {
            renderInventoryList(response.data);
        } else {
            listContainer.innerHTML = `<div class="error">Failed to load inventory</div>`;
        }
    }).catch(error => {
        listContainer.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    });
}

function renderInventoryList(items) {
    const listContainer = document.getElementById('inventory-list');
    
    if (items.length === 0) {
        listContainer.innerHTML = '<p>No items in inventory.</p>';
        return;
    }
    
    const table = `
        <table class="table">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Quantity</th>
                    <th>Price</th>
                    <th>Created Date</th>
                </tr>
            </thead>
            <tbody>
                ${items.map(item => `
                    <tr>
                        <td>${item.name}</td>
                        <td>${item.quantity}</td>
                        <td>$${item.price}</td>
                        <td>${item.created_date}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    
    listContainer.innerHTML = table;
}

// Only allow pharmacists to show the add item form
function showAddItemForm() {
    const userToken = localStorage.getItem('token');
    if (userToken) {
        const userData = JSON.parse(userToken);
        if (userData.role === 'pharmacist') {
            document.getElementById('add-item-section').style.display = 'block';
        } else {
            alert('Only pharmacists can add inventory items');
        }
    }
}

function hideAddItemForm() {
    document.getElementById('add-item-section').style.display = 'none';
    document.getElementById('add-item-form').reset();
}

async function handleAddItem(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const item = {
        name: formData.get('name'),
        quantity: parseInt(formData.get('quantity')),
        price: parseFloat(formData.get('price'))
    };
    
    try {
        const response = await InventoryAPI.add(item);
        if (response.success) {
            alert('Item added successfully!');
            hideAddItemForm();
            showInventory(); // Refresh the inventory
        } else {
            alert('Failed to add item');
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}