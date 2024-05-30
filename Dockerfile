# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the environment variables for Flask
ENV FLASK_APP=app.app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Expose the port the app runs on
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run"]