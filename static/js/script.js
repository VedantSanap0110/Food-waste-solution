// Client-side validation
document.addEventListener('DOMContentLoaded', function() {
    // Get forms
    const loginForm = document.querySelector('form[action*="login"]');
    const signupForm = document.querySelector('form[action*="signup"]');
    
    // Login form validation
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Validate email format
            if (!isValidEmail(email)) {
                event.preventDefault();
                showError('Please enter a valid email address');
                return;
            }
            
            // Validate password length
            if (password.length < 6) {
                event.preventDefault();
                showError('Password must be at least 6 characters long');
                return;
            }
        });
    }
    
    // Signup form validation
    if (signupForm) {
        signupForm.addEventListener('submit', function(event) {
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm-password').value;
            const terms = document.getElementById('terms');
            
            // Validate name
            if (name.length < 2) {
                event.preventDefault();
                showError('Please enter your full name');
                return;
            }
            
            // Validate email format
            if (!isValidEmail(email)) {
                event.preventDefault();
                showError('Please enter a valid email address');
                return;
            }
            
            // Validate password length
            if (password.length < 6) {
                event.preventDefault();
                showError('Password must be at least 6 characters long');
                return;
            }
            
            // Check if passwords match
            if (password !== confirmPassword) {
                event.preventDefault();
                showError('Passwords do not match');
                return;
            }
            
            // Check if terms are accepted
            if (!terms.checked) {
                event.preventDefault();
                showError('You must accept the Terms of Service and Privacy Policy');
                return;
            }
        });
    }
    
    // Helper function to validate email
    function isValidEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }
    
    // Helper function to show error message
    function showError(message) {
        // Check if there's already an error alert
        let alert = document.querySelector('.alert-danger');
        
        if (!alert) {
            // Create a new alert if none exists
            alert = document.createElement('div');
            alert.className = 'alert alert-danger';
            
            // Get the form and insert alert before it
            const form = document.querySelector('form');
            form.parentNode.insertBefore(alert, form);
        }
        
        // Set the message and scroll to it
        alert.textContent = message;
        alert.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
});

// Password visibility toggle (you can add this if needed)
function togglePasswordVisibility() {
    const passwordField = document.getElementById('password');
    
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
    } else {
        passwordField.type = 'password';
    }
}