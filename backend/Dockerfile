# Use a Python base image
FROM python:3.12-alpine

# Set the working directory in the container to /code
WORKDIR /code

# Copy the requirements.txt file to the container
# Make sure to use the correct path relative to the Dockerfile's location
COPY requirements.txt .

# Install dependencies
RUN pip3 install -r requirements.txt

# Copy the entire app directory to the container
COPY app .

# Set environment variables
ENV FLASK_APP=base.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["flask", "run"]
