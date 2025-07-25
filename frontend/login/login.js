// Login page functionality
function renderLoginPage() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="card" style="max-width: 400px; margin: 2rem auto;">
            <h1 class="text-center">Login</h1>
            <form id="login-form">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit" class="btn" style="width: 100%;">Login</button>
            </form>
            <p class="text-center mt-1">
                Don't have an account? <a href="#signup" onclick="navigateTo('signup')">Sign up here</a>
            </p>
        </div>
    `;
    
    // Set up form handler
    const form = document.getElementById('login-form');
    form.addEventListener('submit', handleLogin);
}

async function handleLogin(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const credentials = {
        username: formData.get('username'),
        password: formData.get('password')
    };
    
    // For now, just simulate login (since we haven't implemented auth endpoints yet)
    if (credentials.username && credentials.password) {
        const response = await InventoryAPI.login(credentials.username, credentials.password);
        if (response.error) {
            alert(`Login failed: ${response.error}`);
            return;
        }
        localStorage.setItem('token', JSON.stringify({username: credentials.username}));
        navigateTo('home');
    } else {
        alert('Please fill in all fields');
    }
}