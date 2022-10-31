import React, {Fragment, useState} from "react";
import {CaseList} from "./CaseList";
import {useDispatch} from "react-redux";
import {showAddCaseModal} from "../actions/testcase";
import DeleteConfirmation from "./shared/DeleteConfirmation";
import {deleteTestSuite} from "../api";
import {fetchSuites, setActiveSuite} from "../actions/treesuites";
import {showAddSuiteModal} from "../actions/suite";

export const SuiteInfo = ({suite}) => {
    const [displayConfirmationModal, setDisplayConfirmationModal] = useState(false)
    const [deleteMessage, setDeleteMessage] = useState(null);

    const hideConfirmationModal = () => {
        setDisplayConfirmationModal(false)
    }
    const showDeleteModal = () => {
        setDeleteMessage(`Are you sure you want to delete the test suite '${suite.name}'?`);
        setDisplayConfirmationModal(true)
    }

    const submitDelete = async () => {

        const response = await deleteTestSuite(suite.id)

        if (response.status === 204){
            setDisplayConfirmationModal(false)
            dispatch(setActiveSuite(null))
            dispatch(fetchSuites())
        } else {
            setDeleteMessage('An error has occurred.')
            console.log('Error: ', response)
        }
    }

    const dispatch = useDispatch()

    return (
        <Fragment>
            <p className={"fs-4"}>{suite.name}</p>

            <div>
                <button className="btn btn-outline-secondary me-2" onClick={() => dispatch(showAddSuiteModal(true))}>
                    <i className="bi bi-pencil-square me-2"></i>Change
                </button>
                <button className="btn btn-outline-danger" onClick={() => showDeleteModal()}>
                    <i className="bi bi-trash3 me-2"></i>Delete
                </button>
            </div>

            <hr/>
            <div className="btn-icon fs-4 mb-3">
                <i className="bi bi-plus-circle-fill pe-3 text-primary"
                   onClick={() => dispatch(showAddCaseModal())}></i>
                Add test case
            </div>
            <CaseList test_cases={suite.test_cases}/>

            <DeleteConfirmation showModal={displayConfirmationModal} hideModal={hideConfirmationModal}
                                message={deleteMessage} confirmModal={submitDelete}/>

        </Fragment>
    )
}