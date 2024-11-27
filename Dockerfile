# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY src/ .

# Expose the port that your app runs on (8000 in this case)
EXPOSE 8000

# Command to run your application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "main:app"]