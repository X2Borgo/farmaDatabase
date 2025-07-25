function renderPendingOrdersPage() {
    const content = document.getElementById('content');
    
    // Check role permission
    const userToken = localStorage.getItem('token');
    if (!userToken) {
        navigateTo('login');
        return;
    }
    
    const userData = JSON.parse(userToken);
    if (userData.role !== 'pharmacist') {
        content.innerHTML = `
            <div class="card">
                <h2>Access Denied</h2>
                <p>Only pharmacists can manage orders.</p>
                <button class="btn" onclick="navigateTo('home')">Back to Home</button>
            </div>
        `;
        return;
    }
    
    // Display the pending orders for pharmacists
    content.innerHTML = `
        <div class="card">
            <h2>Pending Orders</h2>
            <div id="orders-list">Loading pending orders...</div>
        </div>
    `;
    
    // Load pending orders
    loadPendingOrders();
}

async function loadPendingOrders() {
    const listContainer = document.getElementById('orders-list');
    
    try {
        const response = await InventoryAPI.getPendingOrders();
        if (response.success) {
            const orders = response.data;
            
            if (orders.length === 0) {
                listContainer.innerHTML = '<p>No pending orders.</p>';
                return;
            }
            
            const ordersList = `
                <div class="orders-list">
                    ${orders.map(order => `
                        <div class="order-card">
                            <div class="order-header">
                                <h4>Order #${order.id}</h4>
                                <p>Placed by: ${order.customer}</p>
                                <p>Date: ${new Date(order.created_date).toLocaleString()}</p>
                                <p>Status: <span class="badge ${order.status === 'pending' ? 'badge-warning' : 'badge-success'}">${order.status}</span></p>
                            </div>
                            <div class="order-items">
                                <h5>Items:</h5>
                                <ul>
                                    ${order.items.map(item => `
                                        <li>${item.quantity} x ${item.name} ($${item.price} each)</li>
                                    `).join('')}
                                </ul>
                                <p>Prescription ID: ${order.prescriptionId || 'N/A'}</p>
                                <p>Notes: ${order.notes || 'None'}</p>
                            </div>
                            <div class="order-actions">
                                <button type="button" class="btn btn-success" onclick="fulfillOrder(${order.id})">Fulfill Order</button>
                                <button type="button" class="btn btn-danger" onclick="rejectOrder(${order.id})">Reject Order</button>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
            
            listContainer.innerHTML = ordersList;
        } else {
            listContainer.innerHTML = `<div class="error">Failed to load orders</div>`;
        }
    } catch (error) {
        listContainer.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
}

async function fulfillOrder(orderId) {
    if (!confirm('Are you sure you want to fulfill this order? This will update inventory quantities.')) {
        return;
    }
    
    try {
        const response = await InventoryAPI.fulfillOrder(orderId);
        if (response.success) {
            alert('Order fulfilled successfully!');
            loadPendingOrders(); // Refresh the orders list
        } else {
            alert(`Failed to fulfill order: ${response.message || 'Unknown error'}`);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

async function rejectOrder(orderId) {
    const reason = prompt('Please enter a reason for rejecting this order:');
    if (reason === null) {
        return; // User cancelled
    }
    
    try {
        const response = await InventoryAPI.rejectOrder(orderId, reason);
        if (response.success) {
            alert('Order rejected successfully!');
            loadPendingOrders(); // Refresh the orders list
        } else {
            alert(`Failed to reject order: ${response.message || 'Unknown error'}`);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}