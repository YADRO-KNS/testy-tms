import React, {useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {hideAddCaseModal, hideCaseDetail, showCaseDetail} from "../../actions/testcase";
import {useForm} from "react-hook-form";
import AlertError from "../../components/AlertError";
import {patchTestCase, patchTestSuite, postTestCase} from "../../api";
import {getSuite} from "../../actions/suiteinfo";
import {Button, Modal} from "react-bootstrap";

const AddEditCaseModal = () => {
    const dispatch = useDispatch()
    const [errors, setErrors] = useState({})
    const {register, handleSubmit, reset} = useForm();
    const isShowAddCaseModal = useSelector(state => state.testcase.add.isShowAddCaseModal)
    const isEditMode = useSelector(state => state.testcase.add.isEditMode)
    const active_suite = useSelector(state => state.treesuites.active)
    const activeTestCase = useSelector(state => state.testcase.active)

    const title = isEditMode ? `Edit Test Case '${activeTestCase.name}'` : 'Add Test Case'

    const onSubmit = async (data) => {
        return isEditMode
            ? await updateTestSuite(data)
            : await createTestSuite(data)
    }

    const createTestSuite = async (data) => {
        const response = await postTestCase({...data, project: PROJECT_ID, suite: active_suite})

        if (response.status === 201) {
            dispatch(hideAddCaseModal())
            dispatch(hideCaseDetail())
            reset()
            dispatch(getSuite(active_suite))
        } else {
            setErrors(response.data)
            console.log('Error: ', response)
        }
    }

    const updateTestSuite = async (data) => {
        const response = await patchTestCase(activeTestCase.id, data)

        if (response.status === 200) {
            dispatch(hideAddCaseModal())
            reset()
            dispatch(hideCaseDetail())
            dispatch(getSuite(active_suite))
            // TODO: добавить обновление детальной информации тест кейса
        } else {
            setErrors(response.data)
            console.log('Error: ', response)
        }
    }

    const showModal = () => {
        reset()
    }

    const hideModal = () => {
        reset()
        setErrors({})
        dispatch(hideAddCaseModal())
    }

    return (
        <Modal show={isShowAddCaseModal} onHide={hideModal} onShow={showModal}>
            <Modal.Header closeButton>
                <Modal.Title>{title}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <AlertError error={errors} fields={['name', 'setup', 'scenario', 'teardown', 'estimate']}/>

                <form className="needs-validation" onSubmit={handleSubmit(onSubmit)}>

                    <div className="form-group mb-3">
                        <label className="form-label">Name</label>
                        <input
                            type="text"
                            className={`form-control ${errors.name ? 'is-invalid' : ''}`}
                            defaultValue={isEditMode ? activeTestCase.name : ''}
                            {...register("name")}
                        />
                        {errors.name ? errors.name.map((error, index) => <p className="invalid-feedback"
                                                                            key={index}>{error}</p>) : ''}
                    </div>

                    <div className="form-group mb-3">
                        <label className="form-label">Setup</label>
                        <textarea
                            className={`form-control ${errors.setup ? 'is-invalid' : ''}`}
                            defaultValue={isEditMode ? activeTestCase.setup : ''}
                            {...register("setup")}
                        />
                        {errors.setup ? errors.setup.map((error, index) => <p className="invalid-feedback"
                                                                              key={index}>{error}</p>) : ''}
                    </div>

                    <div className="form-group mb-3">
                        <label className="form-label">Scenario *</label>
                        <textarea
                            className={`form-control ${errors.scenario ? 'is-invalid' : ''}`}
                            defaultValue={isEditMode ? activeTestCase.scenario : ''}
                            {...register("scenario")}
                        />
                        {errors.scenario ? errors.scenario.map((error, index) => <p
                            className="invalid-feedback"
                            key={index}>{error}</p>) : ''}
                    </div>

                    <div className="form-group mb-3">
                        <label className="form-label">Teardown</label>
                        <textarea
                            className={`form-control ${errors.teardown ? 'is-invalid' : ''}`}
                            defaultValue={isEditMode ? activeTestCase.teardown : ''}
                            {...register("teardown")}
                        />
                        {errors.teardown ? errors.teardown.map((error, index) => <p
                            className="invalid-feedback"
                            key={index}>{error}</p>) : ''}
                    </div>

                    <div className="form-group mb-3">
                        <label className="form-label">Estimate</label>
                        <input
                            type="text"
                            className={`form-control ${errors.estimate ? 'is-invalid' : ''}`}
                            defaultValue={isEditMode ? activeTestCase.estimate : ''}
                            {...register("estimate")}
                        />
                        {errors.estimate ? errors.estimate.map((error, index) => <p className="invalid-feedback"
                                                                                    key={index}>{error}</p>) : ''}
                    </div>

                </form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="default" onClick={hideModal}>
                    Cancel
                </Button>
                <Button variant="primary" onClick={handleSubmit(onSubmit)}>
                    {isEditMode ? "Update" : "Add"}
                </Button>
            </Modal.Footer>
        </Modal>
    )
}

export default AddEditCaseModal