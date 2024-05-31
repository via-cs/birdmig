# Usage

## To start the Flask Backend:
- cd into /birdmig/backend/app
- enter ```uvicorn base:app --reload``` in your terminal

## To start the React Frontend:

- cd into /birdmig
- enter ```npm start``` in your terminal

# To run Docker with all applications
- Ensure that the Docker daemon is running
  - Opening the Docker desktop app is the easiest way to ensure this step
- ```cd``` into ```/birdmig```
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


