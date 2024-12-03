

class LoginService {

    #backendUrl = EnvVariablesService.getInstance().backendUrl;

    // private fields start with #
    static #_instance

    static getInstance() {
        if (!LoginService.#_instance) {
            LoginService.#_instance = new LoginService()
        }
        return LoginService.#_instance
    }

    async login(username, password) {
        try {
            // Make the POST request to the Flask backend
            const t =''
            const response = await fetch(`${this.#backendUrl}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });
    
            const data = await response.json();
    
            console.log('Response status:', response.status);
            console.log('Response message:', data.message);
    
            if (response.ok) {
                alert(data.message); // Successful login
                window.location.href = `${this.#backendUrl}/dashboardPage`;
    
                LocalStorageService.getInstance().setItem('username', username)
    
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
    
}