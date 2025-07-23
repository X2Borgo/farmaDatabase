// Signup page functionality
function renderSignupPage() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="card" style="max-width: 400px; margin: 2rem auto;">
            <h1 class="text-center">Sign Up</h1>
            <form id="signup-form">
                <div class="form-group">
                    <label for="signup-username">Username</label>
                    <input type="text" id="signup-username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="signup-email">Email</label>
                    <input type="email" id="signup-email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="signup-password">Password</label>
                    <input type="password" id="signup-password" name="password" required>
                </div>
                <div class="form-group">
                    <label for="confirm-password">Confirm Password</label>
                    <input type="password" id="confirm-password" name="confirmPassword" required>
                </div>
                <button type="submit" class="btn btn-success" style="width: 100%;">Sign Up</button>
            </form>
            <p class="text-center mt-1">
                Already have an account? <a href="#login" onclick="navigateTo('login')">Login here</a>
            </p>
        </div>
    `;
    
    // Set up form handler
    const form = document.getElementById('signup-form');
    form.addEventListener('submit', handleSignup);
}

async function handleSignup(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const userData = {
        username: formData.get('username'),
        email: formData.get('email'),
        password: formData.get('password'),
        confirmPassword: formData.get('confirmPassword')
    };
    
    // Basic validation
    if (userData.password !== userData.confirmPassword) {
        alert('Passwords do not match');
        return;
    }
    
    // For now, just simulate signup (since we haven't implemented auth endpoints yet)
    if (userData.username && userData.email && userData.password) {
        alert('Signup functionality will be implemented with authentication endpoints');
        navigateTo('login');
    } else {
        alert('Please fill in all fields');
    }
}