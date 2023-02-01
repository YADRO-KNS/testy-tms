## The client part of the test management system - TestY.

The frontend is implemented in the TypeScript programming language using the [React](https://reactjs.org/) 
library and a set of [MUI](https://mui.com/) components.

### Launch in development mode.

For development, you can run the following commands in the root of the frontend directory:

`npm install` - to install dependencies

`npm start` - to launch the application

### Testing the client part.
Implemented end-to-end (E2E) testing using the [cypress](https://www.cypress.io/) library.
For testing, you can use the following commands:

`npm run test:cypress` - run tests in the terminal

`npm run open:cypress` - open the cypress interface for testing with a visual display

### Launch the application in a docker containers.

To run the application in the docker containers, you can run the following command in the root 
of the testy-tms directory:

`docker-compose up`