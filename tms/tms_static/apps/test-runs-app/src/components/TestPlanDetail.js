import React, {Fragment, useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {getTestPlan} from "../actions/testplaninfo";
import {TestList} from "./TestList"

const TestPlanDetail = ({testplan}) => {
    const dispatch = useDispatch()

    return (
        <Fragment>
            <p className={"fs-4"}>{testplan.name}</p>
            <div>
                <button className="btn btn-outline-secondary me-2">
                    <i className="bi bi-pencil-square me-2"></i>Change
                </button>
                <button className="btn btn-outline-danger">
                    <i className="bi bi-trash3 me-2"></i>Delete
                </button>
            </div>
            <hr/>
            <div>
                <TestList tests={testplan.tests}/>
            </div>
        </Fragment>
    )
}

export default TestPlanDetail