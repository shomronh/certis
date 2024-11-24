
// DOTO:

// 1. update scheduler settings (POST)


// 2. add domain OR add domains bulk (POST)
 // Bulk Upload
 document.getElementById("bulk-upload-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const userId = document.getElementById("bulk-user-id").value;
    const file = document.getElementById("bulk-file").files[0];
    const messageBox = document.getElementById("bulk-upload-message");

    const formData = new FormData();
    formData.append("user_id", userId);
    formData.append("file", file);

    try {
        const response = await fetch(`${backendUrl}/bulk_upload`, {
            method: "POST",
            body: formData,
        });

        const data = await response.json();
        messageBox.textContent = data.message || data.error;
        messageBox.style.color = response.ok ? "green" : "red";
    } catch (error) {
        messageBox.textContent = "An error occurred during bulk upload.";
        messageBox.style.color = "red";
    }
});


// 3. get domains (get all domains from API GET METHOD)