import React from "react";
import ReactDOM from 'react-dom'
import App from "./components/App"
import configureStore from "./configureStore";

const store = configureStore()

ReactDOM.render(
    <App store={store} />,
    document.getElementById("test-suites-app")
)