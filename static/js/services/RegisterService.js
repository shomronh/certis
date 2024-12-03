
class RegisterService {

    #backendUrl = EnvVariablesService.getInstance().backendUrl;

    // private fields start with #
    static #_instance

    static getInstance() {
        if (!RegisterService.#_instance) {
            RegisterService.#_instance = new RegisterService()
        }
        return RegisterService.#_instance
    }

    async register(username, password) {
        try {
            const response = await fetch(`${this.#backendUrl}/register`, {
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
                window.location.href = `${this.#backendUrl}`;
            } else if (data.message === "Username is taken") {
                alert("Username is already taken. Please choose a different one.");
            } else if (data.message === "Username should not contain spaces" || data.message === "password should not contain spaces") {
                alert("canot contain spaces");
            }

            console.log('Response data:', data);
        } catch (error) {
            console.error('Error during fetch:', error);
        }
    }

}


