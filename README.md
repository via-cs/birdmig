# Usage

## Prerequisites

Your terminal should be running commands in the root directory of this project.

Ensure that your terminal supports both `pip` and `npm` commands.

## Starting the backend
```
pip install -r backend/requirements.txt
fastapi dev backend/app/base.py
```
  - Access docs by navigating to ```localhost:8000/docs``` on your web browser
  - To run the backend for debugging purposes, run ```uvicorn backend.app.base:app --reload``` in your terminal.
    - Note that this only runs the backend. It can not be navigated to on the web browser, nor will documentation be available.

## Starting the frontend

```
npm install
npm start
```
- These commands should install all required packages for the webpage, as well as start the frontend. The webpage should automatically open in your default browser under the tab "Birdmig".
  - This process may take a few minutes.

# To run Docker with all applications
- Ensure that the Docker daemon is running
  - Opening the Docker desktop app is the easiest way to ensure this step
- Build and run the containers with the command: ```docker-compose up -d --no-deps --build```
- Go to ```http://localhost:3000``` to observe changes.

# Running React Tests
This project uses [Jest](https://jestjs.io/) alongside [@testing-library/react](https://testing-library.com/docs/react-testing-library/intro) for testing React components.

## Prerequisites

Before running tests, make sure you have:

- Node.js installed on your system.
- All the project dependencies installed. If you haven't done so already, you can install them by running `npm install` in the project's root directory.

## Running All Tests

To run all the tests in the project, you can use the following command:

```sh
npm test
```

Running Tests with Coverage
To run tests and generate a coverage report, you can use the following command:

```sh
npm test -- --coverage
```
This will not only test your components but also provide a detailed report of your test coverage.

## Writing New Tests
Test files are located alongside the components they are testing, with a `.test.js` or `.test.jsx` file extension. For example, if you have a component in `src/components/MyComponent.js`, its tests should be in `src/components/MyComponent.test.js`.

