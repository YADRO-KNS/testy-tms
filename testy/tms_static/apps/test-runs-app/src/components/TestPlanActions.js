import React from "react";
import {useDispatch} from "react-redux";
import {showAddEditTestPlanModal} from "../actions/testplans";

export const AddTestPLanButton = () => {
    const dispatch = useDispatch()
    return (
        <div className="btn-icon fs-3 mb-3">
            <i className="bi bi-plus-circle-fill pe-3 text-primary" onClick={() => dispatch(showAddEditTestPlanModal())}></i>
            Test plan
        </div>
    )
}

const
    TestPlanActions = () => {
        return (
            <div className="hstack">
                <AddTestPLanButton/>
            </div>
        )
    }

export default TestPlanActions