// Ensure the document is ready before attaching event listeners
document.addEventListener("DOMContentLoaded", function () {
    // Add Domain form submission listener
    document.getElementById("add-domain-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const userId = document.getElementById("user-id").value;
        const domain = document.getElementById("domain").value;
        const messageBox = document.getElementById("add-domain-message");

        const data = { user_id: userId, domain };
        const response = await addDomain(data, messageBox);
        messageBox.textContent = response.message || response.error;
        messageBox.style.color = response.ok ? "green" : "red";
    });

    // Bulk Upload form submission listener
    document.getElementById("bulk-upload-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const userId = document.getElementById("bulk-user-id").value;
        const file = document.getElementById("bulk-file").files[0];
        const messageBox = document.getElementById("bulk-upload-message");

        const formData = new FormData();
        formData.append("user_id", userId);
        formData.append("file", file);

        const response = await bulkUpload(formData, messageBox);
        messageBox.textContent = response.message || response.error;
        messageBox.style.color = response.ok ? "green" : "red";
    });
});