# Dockerfile for the front end of the application.

# Start an image with node base image.
# node:18 is essentially node.js to help construct the web file.
FROM node:18-alpine

# Sets the /app directory, or the CWDir.
WORKDIR /app

# Copy contents of package.json files for utility to run the front end locally.
COPY package*.json ./

# Run additional commands for startup
RUN npm install && \
npm install d3

COPY . ./

# Begin the program
ENTRYPOINT [ "npm",  "start" ]