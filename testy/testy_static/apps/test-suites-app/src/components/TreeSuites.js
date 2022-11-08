import React, {useEffect} from "react"
import {connect} from "react-redux";
import {fetchSuites} from "../actions/treesuites";
import ConnectedTreeNode from "./TreeNode";
import AddSuiteBtn from "./AddSuiteBtn";
import AddEditSuiteModal from "./modals/AddEditSuiteModal";

const TreeSuites = ({treesuites, fetchSuites}) => {
    useEffect(fetchSuites, [])

    return (
        <div className="p-4">

            <AddSuiteBtn/>
            <AddEditSuiteModal />
            <div className="tree"> {
                treesuites.error
                    ? <p>Error.</p>
                    : treesuites.pending
                        ? <p>Загрузка...</p>
                        : treesuites.suites && treesuites.suites.length
                            ? treesuites.suites.map(suite => <ConnectedTreeNode suite={suite} key={suite.id}/>)
                            : <p>Нет данных</p>
            }
            </div>
        </div>
    )
}

const mapStateToProps = state => ({
    treesuites: state.treesuites
})

const mapDispatchToProps = dispatch => ({
    fetchSuites: () => {
        dispatch(fetchSuites())
    },
})

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(TreeSuites);