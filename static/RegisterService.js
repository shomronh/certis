
const backendUrl = "http://127.0.0.1:8080";

async function dataInsert(username, password) {
    try {
        const response = await fetch(`${backendUrl}/register`, {
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
            window.location.href = "/loginPage";
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