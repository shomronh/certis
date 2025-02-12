

const loginForm = document.getElementById('login-form');

    const backendUrl = EnvVariablesHandler.getInstance().backendUrl;

    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // Prevent the default form submission

        // Get input values
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        await LoginService.getInstance().login(username, password);
    });




