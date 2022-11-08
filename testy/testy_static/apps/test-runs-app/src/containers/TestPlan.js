import React, {Fragment, useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {getTestPlan} from "../actions/testplaninfo";
import TestPlanDetail from "../components/TestPlanDetail";
import {TestDetails} from "../components/TestDetails";

const TestPlan = () => {
    const testplan_active = useSelector(state => state.testplans.active)
    const testplaninfo = useSelector(state => state.testplaninfo)
    const active_test = useSelector(state => state.test.active)

    const dispatch = useDispatch()

    useEffect(() => {
        dispatch(getTestPlan(testplan_active))
    }, [testplan_active])

    return (
        <div className="bg-white">
            <div className="row p-3">
                <div className="col">
                    {
                        testplaninfo.error
                        ? <p>Error.</p>
                        : testplaninfo.pending
                            ? <p>Loading...</p>
                            : <TestPlanDetail testplan={testplaninfo.testplan}/>
                    }
                </div>
                {active_test ? <TestDetails active_test={active_test}/> : ''}
            </div>
        </div>
    )
}

export default TestPlan