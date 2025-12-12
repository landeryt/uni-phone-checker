const BACKEND_URL = "http://localhost:8000";

const form = document.getElementById('registrationForm');
const nameInput = document.getElementById('name');
const emailInput = document.getElementById('email');
const phoneInput = document.getElementById('phone');
const formMessage = document.getElementById('formMessage');
const usersBody = document.getElementById('usersBody');

// Handle form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = nameInput.value.trim();
    const email = emailInput.value.trim();
    const phone = phoneInput.value.trim();

    // Client-side validation
    if (!name || !email || !phone) {
        showMessage('All fields are required.');
        return;
    }

    if (phone.length !== 6 || !/^\d{6}$/.test(phone)) {
        showMessage('Phone must be exactly 6 digits.');
        return;
    }

    // Validate phone with backend
    try {
        const validateRes = await fetch(`${BACKEND_URL}/api/phone/validate/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `phone_number=${encodeURIComponent(phone)}`
        });

        const validateData = await validateRes.json();

        if (!validateRes.ok) {
            showMessage('Invalid phone number: ' + validateData.error);
            return;
        }

        // Register user
        const registerRes = await fetch(`${BACKEND_URL}/api/registration/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `name=${encodeURIComponent(name)}&email=${encodeURIComponent(email)}&phone_number=${encodeURIComponent(phone)}`
        });

        const registerData = await registerRes.json();

        if (!registerRes.ok) {
            showMessage('Registration failed: ' + registerData.error);
            return;
        }

        showMessage('Registration successful!');
        form.reset();
        loadUsers();
    } catch (err) {
        showMessage('Error: ' + err.message);
    }
});

// Load and display users
async function loadUsers() {
    try {
        const res = await fetch(`${BACKEND_URL}/api/users/`);
        const users = await res.json();

        usersBody.innerHTML = '';
        users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.email}</td>
                <td>${user.phone_number}</td>
                <td>${new Date(user.created_at).toLocaleDateString()}</td>
            `;
            usersBody.appendChild(row);
        });
    } catch (err) {
        console.error('Failed to load users:', err);
    }
}

// Show message
function showMessage(msg, type) {
    formMessage.textContent = msg;
    setTimeout(() => formMessage.textContent = '', 4000);
}

// Load users on page load
loadUsers();