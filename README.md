# Usage

## To start the Flask Backend:
- cd into /birdmig/backend
- enter ```flask run``` in your terminal

## To start the React Frontend:

- cd into /birdmig
- enter ```npm start``` in your terminal

## To run the Docker image:
- Ensure that flask is running in the background. (Refer to the Flask section above)
- Open Docker Desktop App
- Build the docker file: docker build -t bird_migration .
- ```Docker run -d -p destination_port:source_destination --name bird_migration bird_migration```
- Navigate to Docker App, and select container bird_migration.
- Scroll up until you see options to view image on browser.
- Open ```http://localhost:<destination_port>```