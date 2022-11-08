import React, {useEffect} from "react"
import {connect} from "react-redux";
import {fetchTestPlans} from "../actions/testplans";
import ConnectedTreeNode from "./TreeNode";

const TreeTestPlans = ({treetestplans, fetchTestPlans}) => {
    useEffect(fetchTestPlans, [])

    return (
        <div className="py-4 pt-0">
            <div className="tree"> {
                treetestplans.error
                    ? <p>Error.</p>
                    : treetestplans.pending
                        ? <p>Загрузка...</p>
                        : treetestplans.testplans && treetestplans.testplans.length
                            ? treetestplans.testplans.map(testplan => <ConnectedTreeNode testplan={testplan} key={testplan.id}/>)
                            : <p>No test plans</p>
            }
            </div>
        </div>
    )
}

const mapStateToProps = state => ({
    treetestplans: state.testplans
})

const mapDispatchToProps = dispatch => ({
    fetchTestPlans: () => {
        dispatch(fetchTestPlans())
    },
})

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(TreeTestPlans);