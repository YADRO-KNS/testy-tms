import React, {useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {hideAddTestResultModal, hideTestDetail, showAddTestResultModal, getTestResultOptions} from "../../actions/test";
import {useForm} from "react-hook-form";
import {Button, Modal} from "react-bootstrap";
import {postTestResult} from "../../api";
import {getTestPlan} from "../../actions/testplaninfo"


const AddTestResultModal = () => {
    const dispatch = useDispatch()
    const [errors, setErrors] = useState({})
    const {register, handleSubmit, reset} = useForm();
    const isShowAddTestResultModal = useSelector(state => state.test.add.isShowAddTestResultModal)
    const result_options = useSelector(state => state.test.add.resultOptions)
    const active_test = useSelector(state => state.test.active)

    const showModal = () => {
        reset()
        dispatch(getTestResultOptions())
    }

    const hideModal = () => {
        reset()
        setErrors({})
        dispatch(hideAddTestResultModal())
    }

    const onSubmit = async (data) => {
        await addTestResult(data)
    }

    const addTestResult = async (data) => {
        const response = await postTestResult({...data, project: PROJECT_ID, test: active_test.id, user: USER_ID})

        if (response.status === 201) {
            dispatch(hideAddTestResultModal())
            reset()
            dispatch(hideTestDetail())
            dispatch(getTestPlan(active_test.plan))
        } else {
            setErrors(response.data)
            console.log('Error: ', response)
        }
    }

    return (
        <Modal show={isShowAddTestResultModal} onHide={hideModal} onShow={showModal}>
            <Modal.Header closeButton>
                <Modal.Title>Add result for `{active_test.case.name}`</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <form className="needs-validation">
                    <div className="form-group mb-3">
                        <label className="form-label">Status</label>
                        <select
                            name="status" className={`form-select ${errors.status ? 'is-invalid' : ''}`}
                            {...register("status")}>
                            <option value="">Select status</option>
                            {result_options && result_options.map(option =>
                                <option value={option.id} key={option.id}>{option.status}</option>)}
                        </select>
                        {errors.status ? errors.status.map((error, index) =>
                                <div className="invalid-feedback" key={index}>{error}</div>) : ''}
                    </div>
                    <div className="form-group mb-3">
                        <label className="form-label">Comment</label>
                        <textarea
                            type="text" rows="3"
                            className={`form-control ${errors.name ? 'is-invalid' : ''}`}
                            {...register("comment")}
                        />
                        {errors.name ? errors.name.map((error, index) => <p className="invalid-feedback"
                                                                            key={index}>{error}</p>) : ''}
                    </div>
                </form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="default" onClick={hideModal}>
                    Cancel
                </Button>
                <Button variant="primary" onClick={handleSubmit(onSubmit)}>
                    Add result
                </Button>
            </Modal.Footer>
        </Modal>
    )
}

export default AddTestResultModal;