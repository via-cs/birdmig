# Dockerfile for the front end of the application.

# Start with the Node.js 18 Alpine image
FROM node:18-alpine

# Set the working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies listed in package.json
# Include specific additional packages needed for the project
RUN npm install && \
    npm install d3 && \
    npm install react-cookie && \
    npm install leaflet react-leaflet leaflet-arrowheads leaflet-polylinedecorator && \
    npm install --save-dev @testing-library/react @testing-library/jest-dom jest-fetch-mock && \
    npm install --save-dev @testing-library/jest-dom



# Copy the rest of the application
COPY . .

# The application is started with npm start
# This should keep the container running as it launches the app
ENTRYPOINT ["npm", "start"]
