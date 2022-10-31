import React from "react";
import {Provider} from "react-redux";
import TestPlanActions from "./TestPlanActions";
import TestPlanList from "./TestPlanList";

const App = ({store}) => {
    return(
        <Provider store={store}>
            <div className="p-3">
                <div className=" p-3 bg-white">
                    <TestPlanActions/>
                    <hr/>
                    <TestPlanList/>
                </div>
            </div>
        </Provider>
    )
}

export default App