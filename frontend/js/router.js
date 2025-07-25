// Simple SPA Router
class Router {
    constructor() {
        this.routes = {};
        this.currentRoute = '';
    }

    addRoute(path, handler) {
        this.routes[path] = handler;
    }

    navigateTo(path) {
        if (this.routes[path]) {
            this.currentRoute = path;
            history.pushState(null, null, `${path}`);
            this.routes[path]();
        } else {
            console.error(`Route ${path} not found`);
        }
    }

    init() {
        // Handle browser back/forward buttons
        window.addEventListener('popstate', () => {
            const path = location.hash.slice(1) || 'home';
            this.handleNavigation(path);
        });

        // Navigate to initial route
        const initialPath = location.hash.slice(1) || 'home';
        this.handleNavigation(initialPath);
    }

    handleNavigation(path) {
        // Allow access to login and signup without token
        if (path === 'login' || path === 'signup') {
            this.navigateTo(path);
            return;
        }
        
        // Check if user is logged in
        if (!localStorage.getItem('token')) {
            this.navigateTo('login');
            return;
        }
        
        // Role-based access control
        const userData = JSON.parse(localStorage.getItem('token'));
        
        // Define role-specific pages
        const customerPages = ['home', 'order', 'my-orders'];
        const pharmacistPages = ['home', 'pending-orders', 'inventory'];
        const practitionerPages = ['home', 'create-prescription', 'prescriptions'];
        
        // Check if the user has access to the requested page
        let hasAccess = false;
        
        switch(userData.role) {
            case 'customer':
                hasAccess = customerPages.includes(path);
                break;
            case 'pharmacist':
                hasAccess = pharmacistPages.includes(path);
                break;
            case 'practitioner':
                hasAccess = practitionerPages.includes(path);
                break;
            default:
                hasAccess = path === 'home';
        }
        
        if (hasAccess) {
            this.navigateTo(path);
        } else {
            alert('You do not have permission to access this page');
            this.navigateTo('home');
        }
    }
}

// Global router instance
const router = new Router();

// Navigation function for global use
function navigateTo(path) {
    // check if user is logged in
    if (!localStorage.getItem('token')) {
        router.navigateTo('login');
        return;
    }

    router.navigateTo(path);
}