// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// API Helper functions
class API {
    static async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        };

        if (config.body && typeof config.body === 'object') {
            config.body = JSON.stringify(config.body);
        }

        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    static async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    static async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: data,
        });
    }

    static async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: data,
        });
    }

    static async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

// Specific API calls
const InventoryAPI = {
    async login(username, password) {
        try {
            return await API.post('/login', { username: username, password: password });
        } catch (error) {
            return { error: error.message || 'Login failed' };
        }
    },

    async signup(userData) {
        try {
            return await API.post('/signup', { 
                username: userData.username, 
                email: userData.email, 
                password: userData.password,
                role: userData.role
            });
        } catch (error) {
            return { error: error.message || 'Signup failed' };
        }
    },

    async getAll() {
        return API.get('/inventory');
    },

    async add(item) {
        return API.post('/inventory', item);
    },

    async healthCheck() {
        return API.get('/health');
    },

    // Customer API calls
    async createOrder(orderData) {
        try {
            return await API.post('/orders', orderData);
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    async getMyOrders() {
        try {
            return await API.get('/orders/my');
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    // Pharmacist API calls
    async getPendingOrders() {
        try {
            return await API.get('/orders/pending');
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    async fulfillOrder(orderId) {
        try {
            return await API.post(`/orders/${orderId}/fulfill`, {});
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    async rejectOrder(orderId, reason) {
        try {
            return await API.post(`/orders/${orderId}/reject`, { reason });
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    // Practitioner API calls
    async createPrescription(prescriptionData) {
        try {
            return await API.post('/prescriptions', prescriptionData);
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    async getPrescriptions() {
        try {
            return await API.get('/prescriptions');
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
};