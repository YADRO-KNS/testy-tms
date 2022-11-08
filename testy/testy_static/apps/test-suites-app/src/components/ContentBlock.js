import React from "react"
import {connect} from "react-redux";
import SuiteInfo from "../containers/SuiteInfo";

const NotSelectedSuite = () => {
    return (
        <div className="p-3 h-100">
            <div className=" p-3 h-100 text-center">
                <p className="fs-1"><i className="bi bi-search"></i></p>
                <p className="fs-6">Select a test suite in the left list to see detailed information</p>
            </div>
        </div>
    )
}

const ContentBlock = ({treesuites}) => {
    if (treesuites.active) {
        return <SuiteInfo/>
    }

    return <NotSelectedSuite/>
}

const mapStateToProps = state => ({
    treesuites: state.treesuites
})

export default connect(mapStateToProps)(ContentBlock)