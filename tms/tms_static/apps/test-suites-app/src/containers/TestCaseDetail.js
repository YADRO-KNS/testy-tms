import React, {useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {hideCaseDetail, showAddCaseModal} from "../actions/testcase";
import DeleteConfirmation from "../components/shared/DeleteConfirmation";
import {deleteTestCase} from "../api";
import {getSuite} from "../actions/suiteinfo";


export const TestCaseDetail = () => {
    const [displayConfirmationModal, setDisplayConfirmationModal] = useState(false)
    const [deleteMessage, setDeleteMessage] = useState(null);

    const dispatch = useDispatch()
    const active_test_case = useSelector(state => state.testcase.active)
    const suite_active = useSelector(state => state.suiteinfo.suite)

    const hideConfirmationModal = () => {
        setDisplayConfirmationModal(false)
    }

    const showDeleteModal = () => {
        setDeleteMessage(`Are you sure you want to delete the test case '${active_test_case.name}'?`);
        setDisplayConfirmationModal(true)
    }

    const handleClickClose = () => {
        dispatch(hideCaseDetail())
    }

    const submitDelete = async () => {
        const response = await deleteTestCase(active_test_case.id)

        if (response.status === 204) {
            setDisplayConfirmationModal(false)
            dispatch(hideCaseDetail())
            dispatch(getSuite(suite_active.id))
        } else {
            setDeleteMessage('An error has occurred.')
            console.log('Error: ', response)
        }
    }

    return (
        <div className="col border-start ps-3">
            <div className="hstack">
                <p className="fs-5 m-0">{active_test_case.name}</p>
                <button
                    type="button"
                    className="btn-close ms-auto"
                    aria-label="Close"
                    onClick={handleClickClose}
                ></button>
            </div>

            <hr className="mt-2"/>

            <p className="pt-3 mb-1 opacity-50">Name</p>
            <p>{active_test_case.name}</p>

            <p className="pt-3 mb-1 opacity-50">Setup</p>
            <pre>{active_test_case.setup}</pre>

            <p className="pt-3 mb-1 opacity-50">Scenario</p>
            <pre>{active_test_case.scenario}</pre>

            <p className="pt-3 mb-1 opacity-50">Teardown</p>
            <pre>{active_test_case.teardown}</pre>

            <p className="pt-3 mb-1 opacity-50">Estimate</p>
            <p>{active_test_case.estimate}</p>

            <hr/>

            <div>
                <button className="btn btn-outline-secondary me-2" onClick={() => dispatch(showAddCaseModal(true))}>
                    <i className="bi bi-pencil-square me-2"></i>Change
                </button>
                <button className="btn btn-outline-danger" onClick={() => showDeleteModal()}>
                    <i className="bi bi-trash3 me-2"></i>Delete
                </button>
            </div>

            <DeleteConfirmation
                showModal={displayConfirmationModal}
                hideModal={hideConfirmationModal}
                message={deleteMessage} confirmModal={submitDelete}
            />

        </div>
    )
}