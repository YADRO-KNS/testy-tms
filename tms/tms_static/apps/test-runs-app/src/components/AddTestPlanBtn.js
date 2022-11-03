import React from "react";
import {useDispatch} from "react-redux";

const AddTestPlanBtn = () => {
    const dispatch = useDispatch()

    return (
        <div className="btn-icon fs-3 mb-3">
            <i className="bi bi-plus-circle-fill pe-3 text-primary"></i>
            Add test plan
        </div>
    )
}

export default AddTestPlanBtn