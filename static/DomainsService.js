
// DOTO:

// 1. update scheduler settings (POST)


// 2. add domain OR add domains bulk (POST)
const backendUrl = "http://127.0.0.1:5000";

// Function to handle Add Domain
async function addDomain(data, messageBox) {
    try {
        const response = await fetch(`${backendUrl}/add_domain`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });

        const responseData = await response.json();
        return responseData; // Return the response data to be handled in dataListener.js
    } catch (error) {
        messageBox.textContent = "An error occurred while adding the domain.";
        messageBox.style.color = "red";
        return { message: "An error occurred", error: true, ok: false };
    }
}

// Function to handle Bulk Upload
async function bulkUpload(formData, messageBox) {
    try {
        const response = await fetch(`${backendUrl}/bulk_upload`, {
            method: "POST",
            body: formData,
        });

        const responseData = await response.json();
        return responseData; // Return the response data to be handled in dataListener.js
    } catch (error) {
        messageBox.textContent = "An error occurred during the bulk upload.";
        messageBox.style.color = "red";
        return { message: "An error occurred", error: true, ok: false };
    }
}



// 3. get domains (get all domains from API GET METHOD)