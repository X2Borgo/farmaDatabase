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
            this.navigateTo(path);
        });



        // Navigate to initial route
        const initialPath = location.hash.slice(1) || 'login';
        this.navigateTo(initialPath);
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