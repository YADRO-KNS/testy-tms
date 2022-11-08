import React from "react";
import {useDispatch, useSelector} from "react-redux";
import {hideTestDetail} from "../actions/test";
import {TestResultsList} from "./TestResultsList";
import Badge from 'react-bootstrap/Badge';
import {showAddTestResultModal} from "../actions/test";
import AddTestResultModal from "./modals/AddTestResultModal";

export const TestDetails = () => {
    const dispatch = useDispatch()
    const active_test = useSelector(state => state.test.active)

    const handleClickClose = () => {
        dispatch(hideTestDetail())
    }

    return (
        <div className="col border-start ps-3">
            <div className="hstack">
                <p className="fs-5 m-0">{active_test.case.name}</p>
                <button
                    type="button"
                    className="btn-close ms-auto"
                    aria-label="Close"
                    onClick={handleClickClose}
                ></button>
            </div>

            <hr className="mt-2"/>

            <div className="p-2">
                <div className="bg-light">
                    <p className="mb-1 opacity-50">Estimate</p>
                    <p className="mb-1">{active_test.case.estimate}</p>
                </div>

                <p className="pt-3 mb-1 opacity-50">Setup</p>
                <pre>{active_test.case.setup}</pre>

                <p className="pt-3 mb-1 opacity-50">Scenario</p>
                <pre>{active_test.case.scenario}</pre>

                <p className="pt-3 mb-1 opacity-50">Teardown</p>
                <pre>{active_test.case.teardown}</pre>
            </div>

            <p className="fs-6 m-0 pt-2">Results</p>
            <hr className="mt-2"/>
            <div className="text-end">
                <button className="btn btn-outline-secondary me-2" onClick={() => dispatch(showAddTestResultModal())}>
                    <i className="bi bi-pencil-square me-2"></i>Add result
                </button>
            </div>
            <TestResultsList test_results={active_test.test_results}/>
            <AddTestResultModal/>
        </div>
    )
}