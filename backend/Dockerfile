# Use a Python base image
FROM python:3.12-alpine

# Set the working directory in the container to /code
WORKDIR /code

# Install system dependencies for GEOS, pip, and building Python packages
# Including gcc, musl-dev for compiling, and geos-dev for Shapely
RUN apk add --no-cache gcc musl-dev geos-dev

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install dependencies listed in requirements.txt
RUN pip3 install -r requirements.txt

# Copy the entire backend directory to the container
COPY . .

# Ensure the data directory is properly copied
COPY app/data/ /code/data/

# Set environment variables
ENV FLASK_APP=app/base.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["flask", "run"]
