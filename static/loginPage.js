const loginForm = document.getElementById('login-form');


loginForm.addEventListener('submit', async function(event) {
    console.log('Form is submitted!');
    event.preventDefault(); // Prevent the default form submission

    // Get input values
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    console.log(`Username: ${username}, Password: ${password}`); // Corrected template literals

    await Login(username, password);
});

async function Login(username, password) {
    try {
        // Make the POST request to the Flask backend
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }), // Shorter object syntax
        });

        // Parse the JSON response
        const data = await response.json();
        console.log('Response status:', response.status);
        console.log('Response message:', data.message);

        if (response.ok) {
            alert(data.message); // Successful login
            window.location.href = "/dashboard";
        } else if (response.status === 404) {
            alert(data.message); // Missing users.json or registration required
        } else if (response.status === 401) {
            alert(data.message); // Invalid credentials
        } else {
            alert("An unexpected error occurred. Please try again.");
        }

    } catch (error) {
        console.error('Error during fetch:', error);
        alert("An error occurred while trying to log in. Please try again later.");
    }
}
