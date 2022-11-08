import React from "react";
import {showAddSuiteModal} from "../actions/suite";
import {useDispatch} from "react-redux";

const AddSuiteBtn = () => {
    const dispatch = useDispatch()

    return (
        <div className="btn-icon fs-3 mb-3">
            <i className="bi bi-plus-circle-fill pe-3 text-primary" onClick={() => dispatch(showAddSuiteModal())}></i>
            Add test suite
        </div>
    )
}

export default AddSuiteBtn