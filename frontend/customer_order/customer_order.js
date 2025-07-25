function renderOrderPage() {
    const content = document.getElementById('content');
    
    // Check role permission
    const userToken = localStorage.getItem('token');
    if (!userToken) {
        navigateTo('login');
        return;
    }
    
    const userData = JSON.parse(userToken);
    if (userData.role !== 'customer') {
        content.innerHTML = `
            <div class="card">
                <h2>Access Denied</h2>
                <p>Only customers can place orders.</p>
                <button class="btn" onclick="navigateTo('home')">Back to Home</button>
            </div>
        `;
        return;
    }
    
    // Display the order form for customers
    content.innerHTML = `
        <div class="card">
            <h2>Place New Order</h2>
            <div id="medications-list">Loading available medications...</div>
            
            <form id="order-form" class="mt-1">
                <h3>Your Order</h3>
                <div id="order-items">
                    <p>Select medications from the list above</p>
                </div>
                
                <div class="form-group mt-1">
                    <label for="prescription">Prescription ID (if applicable)</label>
                    <input type="text" id="prescription" name="prescription">
                </div>
                
                <div class="form-group">
                    <label for="order-notes">Additional Notes</label>
                    <textarea id="order-notes" name="notes" rows="3"></textarea>
                </div>
                
                <button type="submit" class="btn btn-primary">Place Order</button>
                <button type="button" class="btn" onclick="navigateTo('home')">Cancel</button>
            </form>
        </div>
    `;
    
    // Load available medications
    loadMedications();
    
    // Set up form handler
    const form = document.getElementById('order-form');
    form.addEventListener('submit', handleOrderSubmit);
}

async function loadMedications() {
    const listContainer = document.getElementById('medications-list');
    
    try {
        const response = await InventoryAPI.getAll();
        if (response.success) {
            const medications = response.data;
            
            if (medications.length === 0) {
                listContainer.innerHTML = '<p>No medications available.</p>';
                return;
            }
            
            const medicationsList = `
                <div class="medication-selection">
                    ${medications.map(med => `
                        <div class="medication-item">
                            <div class="med-info">
                                <h4>${med.name}</h4>
                                <p>Price: $${med.price}</p>
                                <p>Available: ${med.quantity}</p>
                            </div>
                            <div class="med-actions">
                                <button type="button" class="btn btn-sm" 
                                    onclick="addToOrder(${med.id}, '${med.name}', ${med.price})">
                                    Add to Order
                                </button>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
            
            listContainer.innerHTML = medicationsList;
        } else {
            listContainer.innerHTML = `<div class="error">Failed to load medications</div>`;
        }
    } catch (error) {
        listContainer.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
}

// Global variable to track order items
const orderItems = [];

function addToOrder(id, name, price) {
    // Check if item already in order
    const existingItem = orderItems.find(item => item.id === id);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        orderItems.push({
            id,
            name,
            price,
            quantity: 1
        });
    }
    
    // Update the order display
    updateOrderDisplay();
}

function updateOrderDisplay() {
    const orderContainer = document.getElementById('order-items');
    
    if (orderItems.length === 0) {
        orderContainer.innerHTML = '<p>No items added to order</p>';
        return;
    }
    
    let total = 0;
    const orderHTML = `
        <table class="table">
            <thead>
                <tr>
                    <th>Medication</th>
                    <th>Quantity</th>
                    <th>Price</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                ${orderItems.map(item => {
                    const itemTotal = item.price * item.quantity;
                    total += itemTotal;
                    return `
                        <tr>
                            <td>${item.name}</td>
                            <td>
                                <input type="number" min="1" value="${item.quantity}" 
                                    onchange="updateItemQuantity(${item.id}, this.value)">
                            </td>
                            <td>$${itemTotal.toFixed(2)}</td>
                            <td>
                                <button type="button" class="btn btn-sm btn-danger" 
                                    onclick="removeFromOrder(${item.id})">Remove</button>
                            </td>
                        </tr>
                    `;
                }).join('')}
            </tbody>
            <tfoot>
                <tr>
                    <th colspan="2">Total</th>
                    <th>$${total.toFixed(2)}</th>
                    <th></th>
                </tr>
            </tfoot>
        </table>
        <input type="hidden" name="orderItems" value="${JSON.stringify(orderItems)}">
    `;
    
    orderContainer.innerHTML = orderHTML;
}

function updateItemQuantity(id, quantity) {
    const item = orderItems.find(item => item.id === id);
    if (item) {
        item.quantity = parseInt(quantity);
        updateOrderDisplay();
    }
}

function removeFromOrder(id) {
    const index = orderItems.findIndex(item => item.id === id);
    if (index !== -1) {
        orderItems.splice(index, 1);
        updateOrderDisplay();
    }
}

async function handleOrderSubmit(event) {
    event.preventDefault();
    
    if (orderItems.length === 0) {
        alert('Please add at least one medication to your order');
        return;
    }
    
    const formData = new FormData(event.target);
    const orderData = {
        items: orderItems,
        prescriptionId: formData.get('prescription') || null,
        notes: formData.get('notes') || '',
        customer: JSON.parse(localStorage.getItem('token')).username
    };
    
    try {
        const response = await InventoryAPI.createOrder(orderData);
        if (response.success) {
            alert('Order placed successfully!');
            // Clear order and redirect to my orders
            orderItems.length = 0;
            navigateTo('my-orders');
        } else {
            alert(`Failed to place order: ${response.message || 'Unknown error'}`);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}