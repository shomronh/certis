
// DOTO:

// 1. update scheduler settings (POST)


// 2. add domain OR add domains bulk (POST)

const backendUrl = "http://127.0.0.1:5000";  // URL of the backend API

// Function to add a domain to the backend
async function addDomain(data, messageBox) {
    try {
        // Send a POST request to the backend to add a domain
        const response = await fetch(`${backendUrl}/add_domain`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",  // Set the content type as JSON
            },
            body: JSON.stringify(data),  // Send the data as JSON in the request body
        });

        // Parse the response from the backend
        const responseData = await response.json();
        return responseData;  // Return the response to be handled by the frontend
    } catch (error) {
        // Handle any errors and show a message in the messageBox
        messageBox.textContent = "An error occurred while adding the domain.";
        messageBox.style.color = "red";
        return { message: "An error occurred", error: true, ok: false };
    }
}

// Function to handle bulk upload (e.g., uploading a file)
async function bulkUpload(formData, messageBox) {
    try {
        // Send a POST request with the form data (including the file) for bulk upload
        const response = await fetch(`${backendUrl}/bulk_upload`, {
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

// Function to fetch all domains for a given user
async function getDomains(userId) {
    try {
        // Send a GET request to the backend with the user_id as a query parameter
        const response = await fetch(`${backendUrl}/domains?user_id=${userId}`, {
            method: "GET",  // Make a GET request
            headers: {
                "Content-Type": "application/json",  // You can still send headers, even though it's a GET request
            },
        });

        // Check if the response was successful
        if (response.ok) {
            const data = await response.json();
            return data.message ? data.message.domains : [];  // Return the domains from the response
        } else {
            // If the request fails, throw an error with the message from the backend
            const errorData = await response.json();
            throw new Error(errorData.message || "Error fetching domains.");
        }
    } catch (error) {
        // Handle any errors during the fetch request
        throw new Error("An error occurred while fetching domains: " + error.message);
    }
}

