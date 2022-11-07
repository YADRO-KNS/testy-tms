import React from "react"
import {connect} from "react-redux";
import TestPlan from "../containers/TestPlan";

const NotSelectedTestPlan = () => {
    return (
        <div className="p-3 h-100">
            <div className="p-3 h-100 text-center">
                <p className="fs-1"><i className="bi bi-search"></i></p>
                <p className="fs-6">Select a test plan in the left list to see detailed information</p>
            </div>
        </div>
    )
}

const ContentBlock = ({treetestplans}) => {
    if (treetestplans.active) {
        return <TestPlan/>
    }

    return <NotSelectedTestPlan/>
}

const mapStateToProps = state => ({
    treetestplans: state.testplans
})

export default connect(mapStateToProps)(ContentBlock)