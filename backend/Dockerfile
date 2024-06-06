# Use a Python base image
FROM python:3.9-slim

# Set the working directory in the container to /code
WORKDIR /code

# Install system dependencies for GEOS, pip, and building Python packages
# Including gcc, musl-dev for compiling, and libgeos-dev for Shapely
RUN apt-get update && \
    apt-get install -y gcc musl-dev libgeos-dev

# Install numpy first to avoid conflicts
RUN pip install numpy
RUN pip install scikit-learn

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install dependencies listed in requirements.txt
RUN pip install -r requirements.txt

# Copy the entire backend directory to the container
COPY . .

# Ensure the data directory is properly copied
COPY app/data/ /code/data/

COPY app/models/ /code/models/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["fastapi", "dev", "base.py"]