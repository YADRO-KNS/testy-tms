import React from "react";
import {Provider} from "react-redux";
import TestPlanActions from "./TestPlanActions";
import TestPlanContent from "./TestPlanContent";

const App = ({store}) => {
    return(
        <Provider store={store}>
            <div className="p-3">
                <div className=" p-3 bg-white">
                    <TestPlanActions/>
                    <hr/>
                    <TestPlanContent/>
                </div>
            </div>
        </Provider>
    )
}

export default App