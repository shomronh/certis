// Ensure the document is ready before attaching event listeners

document.addEventListener("DOMContentLoaded", async function () {
    // Get the User ID from session or another method (e.g., localStorage)
    const userId = document.getElementById("user-id").value; // Or get it from somewhere else

    // Fetch and display domains on page load
    try {
        const domains = await getDomains(userId);  // Fetch the domains for the user
        displayDomains(domains);  // Display the domains on the page
    } catch (error) {
        console.error("Error fetching domains:", error);
        alert("There was an error fetching the domains.");
    }

    // Add Domain form submission listener
    document.getElementById("add-domain-form").addEventListener("submit", async (e) => {
        e.preventDefault();  // Prevent the form from submitting normally

        const userId = document.getElementById("user-id").value;  // Get the user ID from the input
        const domain = document.getElementById("domain").value;  // Get the domain from the input
        const messageBox = document.getElementById("add-domain-message");  // Get the message box for displaying status

        const data = { user_id: userId, domain };  // Prepare the data for the backend
        const response = await addDomain(data, messageBox);  // Call the addDomain function

        // Display the response message
        messageBox.textContent = response.message || response.error;
        messageBox.style.color = response.ok ? "green" : "red";  // Change the message color based on success or error

        // Optionally, refresh the domains list after adding a new domain
        try {
            const updatedDomains = await getDomains(userId);  // Fetch the updated domains
            displayDomains(updatedDomains);  // Display the updated list of domains
        } catch (error) {
            console.error("Error fetching updated domains:", error);
        }
    });

    // Bulk Upload form submission listener
    document.getElementById("bulk-upload-form").addEventListener("submit", async (e) => {
        e.preventDefault();  // Prevent the form from submitting normally

        const userId = document.getElementById("bulk-user-id").value;  // Get the user ID
        const file = document.getElementById("bulk-file").files[0];  // Get the file from the input
        const messageBox = document.getElementById("bulk-upload-message");  // Get the message box

        const formData = new FormData();  // Create a new FormData object
        formData.append("user_id", userId);  // Append the user ID to the FormData
        formData.append("file", file);  // Append the file to the FormData

        const response = await bulkUpload(formData, messageBox);  // Call the bulkUpload function

        // Display the response message
        messageBox.textContent = response.message || response.error;
        messageBox.style.color = response.ok ? "green" : "red";  // Change the message color based on success or error

        // Optionally, refresh the domains list after bulk upload
        try {
            const updatedDomains = await getDomains(userId);  // Fetch the updated domains
            displayDomains(updatedDomains);  // Display the updated list of domains
        } catch (error) {
            console.error("Error fetching updated domains:", error);
        }
    });
});

// Function to display domains on the page
function displayDomains(domains) {
    const domainsContainer = document.getElementById("domains-container");  // Container where domains will be displayed
    domainsContainer.innerHTML = "";  // Clear any previous domains

    // Create a new div for each domain and append it to the container
    domains.forEach(domain => {
        const domainItem = document.createElement("div"); //Can change to an existing div
        domainItem.textContent = domain;  // Set the domain name as the text content
        domainsContainer.appendChild(domainItem);  // Append the domain item to the container
    });
}
