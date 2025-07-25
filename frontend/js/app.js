// Main application initialization
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the router with all routes
    router.addRoute('home', renderHomePage);
    router.addRoute('login', renderLoginPage);
    router.addRoute('signup', renderSignupPage);
    
    // Customer routes
    router.addRoute('order', renderOrderPage);
    router.addRoute('my-orders', renderMyOrdersPage);
    
    // Pharmacist routes
    router.addRoute('pending-orders', renderPendingOrdersPage);
    
    // Practitioner routes
    router.addRoute('create-prescription', renderCreatePrescriptionPage);
    router.addRoute('prescriptions', renderPrescriptionsPage);
    
    // Start the router
    router.init();
    
    // Test backend connection
    testBackendConnection();
});

async function testBackendConnection() {
    try {
        const response = await InventoryAPI.healthCheck();
        if (response.status === 'healthy') {
            console.log('✓ Backend connection successful');
        }
    } catch (error) {
        console.warn('⚠ Backend connection failed:', error.message);
        console.log('Make sure to start the Python backend server');
    }
}