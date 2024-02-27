# Start an image with node base image.
# node:18 is essentially node.js to help construct the web file.
FROM --platform=$BUILDPLATFORM python:3.12-alpine AS builder

# Sets the /app directory, or the CWDir.
WORKDIR /app

# Copy contents of package.json files for utility.
COPY requirements.txt requirements.txt


# Run additional commands for startup
RUN pip3 install -r requirements.txt

COPY . ./

# Begin the program
#CMD [ "npm" ]
ENTRYPOINT [ "flask", "run" ]
#CMD [ "flask", "run"]

# Expose the service port for 
EXPOSE 3000