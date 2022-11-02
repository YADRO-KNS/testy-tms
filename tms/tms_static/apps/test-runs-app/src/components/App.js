import React from "react";
import {Provider} from "react-redux";
import TestPlanActions from "./TestPlanActions";
import TestPlanContent from "./TestPlanContent";

const App = ({store}) => {
    return(
        <Provider store={store}>
            <div className="p-4">
                <TestPlanActions/>
                <TestPlanContent/>
            </div>
        </Provider>
    )
}

export default App