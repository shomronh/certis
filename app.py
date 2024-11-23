from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from domain_service import DomainService
from domain_repository import DomainRepository
import os
import re

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize repository and service
repository = DomainRepository()
service = DomainService(repository)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def is_valid_domain(domain):
    """Validate domain format using a regex."""
    pattern = re.compile(
        r"^(?:[a-zA-Z0-9]"  # Start with alphanumeric character
        r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)"  # Middle characters
        r"+[a-zA-Z]{2,}$"  # Top-level domain
    )
    return pattern.match(domain) is not None

@app.route("/add_domain", methods=["POST"])
def add_domain():
    data = request.get_json()
    user_id = data.get("user_id")
    domain = data.get("domain")

    if not user_id or not domain:
        return jsonify({"error": "User ID and domain are required"}), 400

    if not is_valid_domain(domain):
        return jsonify({"error": "Invalid domain format"}), 400

    result = service.add_domain(user_id, domain)
    return jsonify({"message": f"Domain {domain} added successfully."})

@app.route("/bulk_upload", methods=["POST"])
def bulk_upload():
    user_id = request.form.get("user_id")
    file = request.files.get("file")

    if not user_id or not file:
        return jsonify({"error": "User ID and a file are required"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "invalid file format or content"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    try:
        with open(file_path, "r") as f:
            domains = [line.strip() for line in f if line.strip()]
    except Exception:
        os.remove(file_path)  # Clean up in case of an error
        return jsonify({"error": "invalid file format or content"}), 400

    for domain in domains:
        service.add_domain(user_id, domain)

    # Clean up uploaded file
    os.remove(file_path)
    return jsonify({"message": "Bulk Upload Successful"})

@app.route("/health", methods=["GET"])
def health_check():
    try:
        # Perform a simple check, e.g., ensuring the repository is accessible
        repository_status = repository.check_health()
        if repository_status:
            return jsonify({"status": "healthy"}), 200
        else:
            return jsonify({"status": "unhealthy"}), 500
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)