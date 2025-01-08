# Use Python 3.12.8-slim as the base image
FROM python:3.12.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application files to the working directory
COPY . .


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Expose the port your application will run on (e.g., 5000 for Flask)
EXPOSE 8080 

# Define the command to run your application
# Adjust this line based on your application entry point
CMD ["python", "certis_app.py"]

