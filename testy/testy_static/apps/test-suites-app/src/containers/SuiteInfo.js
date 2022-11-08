import React, {useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {getSuite} from "../actions/suiteinfo";
import {SuiteInfo as SI} from "../components/SuiteInfo";
import {TestCaseDetail} from "./TestCaseDetail";
import AddEditCaseModal from "./modals/AddEditCaseModal";

const SuiteInfo = () => {
    const suite_active = useSelector(state => state.treesuites.active)
    const suiteinfo = useSelector(state => state.suiteinfo)
    const active_test_case = useSelector(state => state.testcase.active)
    const dispatch = useDispatch()

    useEffect(() => {
        dispatch(getSuite(suite_active))
    }, [suite_active])

    return (
        <>
            <div className="p-3">
                <div className="bg-white p-3">
                    <div className="row">
                        <div className="col">
                            {
                                suiteinfo.error
                                    ? <p>Error.</p>
                                    : suiteinfo.pending
                                        ? <p>Loading...</p>
                                        : <SI suite={suiteinfo.suite}/>
                            }
                        </div>
                        {active_test_case ? <TestCaseDetail/> : ''}
                    </div>
                </div>
            </div>

            <AddEditCaseModal/>
        </>
    )
}

export default SuiteInfo