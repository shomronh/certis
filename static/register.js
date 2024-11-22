const form = document.getElementById('register');
const status = document.getElementById('status');

form.addEventListener('submit', function(event) {
    console.log('Form is submitted!');
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    // Check for spaces in the username
    // if (username.includes(' ')) {
    //     alert("Username should not contain spaces");
    //     return; // Stop the form submission
    // }
    // if (password.includes(' ')) {
    //     alert("password should not contain spaces");
    //     return; // Stop the form submission
    // }

    event.target.reset();
    console.log(`Username: ${username}, Password: ${password}`);
    dataInsert(username, password);
});

async function dataInsert(username, password) {
    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: username, password: password })
        });

        console.log('Fetch response:', response);

        const data = await response.json();

        if (data.message === "User registered successfully") {
            alert("User registered successfully");
        }else if (data.message === "Username is taken") {
            alert("Username is already taken. Please choose a different one.");
        }else if (data.message === "Username should not contain spaces"||data.message ==="password should not contain spaces") {
            alert("canot contain spaces");
        }

        console.log('Response data:', data);
       

    } catch (error) {
        console.error('Error during fetch:', error);
    }
}