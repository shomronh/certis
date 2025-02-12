

class LoginService {

    #backendUrl = EnvVariablesHandler.getInstance().backendUrl;

    // private fields start with #
    static #_instance

    static getInstance() {
        if (!LoginService.#_instance) {
            LoginService.#_instance = new LoginService()
        }
        return LoginService.#_instance
    }

    constructor(){
        
    }

    async login(username, password) {
        try {
            // Make the POST request to the Flask backend
            const response = await fetch(`${this.#backendUrl}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
                credentials: 'include'
            });

            const data = await response.json();

            console.log('Response status:', response.status);
            console.log('Response message:', data.message);

            if (response.ok) {
                alert(data.message); // Successful login
                LocalStorageService.getInstance().setItem('username', username)

                // window.location.href = `${this.#backendUrl}/dashboardPage`;
                window.location.href = `/dashboardPage`;

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

    async logout() {
        try {
            const username = LocalStorageService.getInstance().getItem('username')

            const response = await fetch(`${this.#backendUrl}/logout`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username }),
                credentials: 'include'
            });

            if (response.ok) {
                LocalStorageService.getInstance().setItem('username', null)

                // window.location.href = `${this.#backendUrl}/dashboardPage`;
                window.location.href = `/`;
            } else {
                alert("An unexpected error occurred. Please try again.");
            }
        } catch (error) {
            console.error('Error during fetch:', error);
            alert("An error occurred while trying to log in. Please try again later.");
        }
    }

    async showGoogleButton() {
        // The client ID you got from Google Developer Console
        // const clientId = 'YOUR_CLIENT_ID.apps.googleusercontent.com';
        const clientId = '646869605585-0i2ljqvpddcj40m7vnho8818mft60rta.apps.googleusercontent.com';

        // The Google API Client for JavaScript
        google.accounts.id.initialize({
            client_id: clientId,
            callback: async (response) => {
                try {
                    await this.fetchUserInfo(response)
                    resolve(true)
                } catch (error) {
                    console.error("Error fetching user info", error);
                }
            }
        });

        google.accounts.id.renderButton(
            document.getElementById('google_login_button'), // Specify where the button will be rendered
            {
                theme: 'outline',
                size: 'large',
                type: 'icon',
            }
        );
    }

    async fetchUserInfo(googleResponse) {

        const idToken = googleResponse.credential;

        // Make the POST request to the Flask backend
        const response = await fetch(`${this.#backendUrl}/google-auth`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id_token: idToken }),
            // credentials: 'include'
        });

        const data = await response.json();

        console.log('Response status:', response.status);
        console.log('Response message:', data.message);

        if (response.ok) {
            alert(data.message); // Successful login
            
            const username = data.username
            LocalStorageService.getInstance().setItem('username', username)

            window.location.href = `/dashboardPage`;

        } else if (response.status === 404) {
            alert(data.message);
        } else if (response.status === 401) {
            alert(data.message); // Invalid credentials
        } else {
            alert("An unexpected error occurred. Please try again.");
        }
    }
}