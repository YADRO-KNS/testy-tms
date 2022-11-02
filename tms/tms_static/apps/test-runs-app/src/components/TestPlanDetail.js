import React, {Fragment, useEffect, useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {getTestPlan} from "../actions/testplaninfo";
import {TestList} from "./TestList"
import {setActiveTestPlan, fetchTestPlans} from "../actions/testplans";
import {deleteTestPlan} from "../api";
import DeleteConfirmation from "./shared/DeleteConfirmation";

const TestPlanDetail = ({testplan}) => {
    const [displayConfirmationModal, setDisplayConfirmationModal] = useState(false)
    const [deleteMessage, setDeleteMessage] = useState(null);
    const dispatch = useDispatch()

    const hideConfirmationModal = () => {
        setDisplayConfirmationModal(false)
    }
    const showDeleteModal = () => {
        setDeleteMessage(`Are you sure you want to delete the test plan '${testplan.name}'?`);
        setDisplayConfirmationModal(true)
    }

    const submitDelete = async () => {
        const response = await deleteTestPlan(testplan.id)

        if (response.status === 204){
            setDisplayConfirmationModal(false)
            dispatch(setActiveTestPlan(null))
            dispatch(fetchTestPlans())
        } else {
            setDeleteMessage('An error has occurred.')
            console.log('Error: ', response)
        }
    }

    return (
        <Fragment>
            <p className={"fs-4"}>{testplan.title}</p>
            <div>
                <button className="btn btn-outline-secondary me-2">
                    <i className="bi bi-pencil-square me-2"></i>Change
                </button>
                <button className="btn btn-outline-danger" onClick={() => showDeleteModal()}>
                    <i className="bi bi-trash3 me-2"></i>Delete
                </button>
            </div>
            <hr/>
            <div>
                <TestList tests={testplan.tests}/>
            </div>
            <DeleteConfirmation showModal={displayConfirmationModal} hideModal={hideConfirmationModal}
                                message={deleteMessage} confirmModal={submitDelete}/>
        </Fragment>
    )
}

export default TestPlanDetail