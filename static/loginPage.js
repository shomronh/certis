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

        if (response.ok) {
            // Redirect to the dashboard if login is successful
            window.location.href = "/dashboard";
        } else {
            // Alert the message returned by the server
            alert(data.message);
        }

    } catch (error) {
        console.error('Error during fetch:', error);
        alert("An error occurred while trying to log in. Please try again later.");
    }
}
