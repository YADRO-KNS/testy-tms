import React from "react";
import TreeSuites from "./TreeSuites";
import ContentBlock from "./ContentBlock";
import {Provider} from "react-redux";

const App = ({store}) => {
    return (
        <Provider store={store}>
            <div className="row">
                <div className="col-3">
                    <TreeSuites/>
                </div>
                <div className="col-9">
                    <ContentBlock/>
                </div>
            </div>
        </Provider>
    )
}

export default App