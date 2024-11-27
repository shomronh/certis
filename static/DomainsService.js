
class DomainsService {

    #backendUrl = "http://127.0.0.1:8080";

    // private fields start with #
    static #_instance

    static getInstance() {
        if (!DomainsService.#_instance) {
            DomainsService.#_instance = new DomainsService()
        }
        return DomainsService.#_instance
    }

    // Function to add a domain to the backend
    async addDomain(domain, messageBox) {
        try {

            const username = LocalStorageService.getInstance().getItem("username")

            // Send a POST request to the backend to add a domain
            const response = await fetch(`${this.#backendUrl}/domains/add`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",  
                },
                // Sends cookies from the current session
                credentials: 'include',
                body: JSON.stringify({ user_id: username, domain })
            });

            // Parse the response from the backend
            const responseData = await response.json();

            if(response.ok) {
                return {isOk: true, message: responseData}
            }
            return {isOk: false, message: responseData}

        } catch (error) {
            // Handle any errors and show a message in the messageBox
            // messageBox.textContent = "An error occurred while adding the domain.";
            // messageBox.style.color = "red";
            console.error(error)
            return { isOk: false, message: "An error occurred" };
        }
    }

    // Function to handle bulk upload (e.g., uploading a file)
    async bulkUpload(formData, messageBox) {
        try {
            // Send a POST request with the form data (including the file) for bulk upload
            const response = await fetch(`${this.#backendUrl}/bulk_upload`, {
                method: "POST",
                body: formData,  // Include the file and other data in the formData
            });

            // Parse the response from the backend
            const responseData = await response.json();
            return responseData;  // Return the response to be handled by the frontend
        } catch (error) {
            // Handle any errors and show a message in the messageBox
            messageBox.textContent = "An error occurred during the bulk upload.";
            messageBox.style.color = "red";
            return { message: "An error occurred", error: true, ok: false };
        }
    }

    async getDomains() {
        try {

            const userId = LocalStorageService.getInstance().getItem('username')

            // Send a GET request to the backend with the user_id as a query parameter
            const response = await fetch(`${this.#backendUrl}/domains/user/${userId}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
                // Sends cookies from the current session
                credentials: 'include',
            });

            if (response.ok) {
                const data = await response.json();
                return data ? data : [];
            } else {
                const errorData = await response.json();
                throw new Error(errorData.message || "Error fetching domains.");
            }
        } catch (error) {
            // Handle any errors during the fetch request
            throw new Error("An error occurred while fetching domains: " + error.message);
        }
    }
}
