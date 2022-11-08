import React, {useEffect, useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {useForm} from "react-hook-form";
import {hideAddSuiteModal} from "../../actions/suite";
import AlertError from "../AlertError";
import {patchTestSuite, postTestSuite} from "../../api";
import {fetchSuites} from "../../actions/treesuites";
import ConnectedTreeOptions from "../TreeOptions";
import {Button, Modal} from "react-bootstrap";
import {getSuite} from "../../actions/suiteinfo";


const AddEditSuiteModal = () => {
    const dispatch = useDispatch()
    const [errors, setErrors] = useState({})
    const {register, handleSubmit, reset} = useForm();

    const suite = useSelector(state => state.suite)
    const treesuites = useSelector(state => state.treesuites)
    const activeTestSuite = useSelector(state => state.suiteinfo.suite)

    const title = suite.isEditMode ? `Edit Test Suite '${activeTestSuite.name}'` : 'Add Test Suite'

    const onSubmit = async (data) => {
        return suite.isEditMode
            ? await updateSuite(data)
            : await createSuite(data)
    }

    const createSuite = async (data) => {
        const response = await postTestSuite({...data, project: PROJECT_ID})

        if (response.status === 201) {
            dispatch(hideAddSuiteModal())
            reset()
            dispatch(fetchSuites())
        } else {
            setErrors(response.data)
            console.log('Error: ', response)
        }
    }

    const updateSuite = async (data) => {
        const response = await patchTestSuite(activeTestSuite.id, data)
        if (response.status === 200) {
            dispatch(hideAddSuiteModal())
            dispatch(getSuite(activeTestSuite.id))
            reset()
            dispatch(fetchSuites())
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
        dispatch(hideAddSuiteModal())
    }

    return (
        <Modal show={suite.isShowAddSuiteModal} onHide={hideModal} onShow={showModal}>
            <Modal.Header closeButton>
                <Modal.Title>{title}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <AlertError error={errors} fields={['name', 'parent']}/>
                <form onSubmit={handleSubmit(onSubmit)} className="needs-validation">
                    <div className="form-group mb-3">
                        <label className="form-label">Parent</label>
                        <select
                            name="parent"
                            className={`form-select ${errors.parent ? 'is-invalid' : ''}`}
                            defaultValue={suite.isEditMode ? activeTestSuite.parent : null}
                            {...register("parent")}
                        >
                            <option value="">Select parent test suite</option>
                            {treesuites.suites && treesuites.suites.map(suite => <ConnectedTreeOptions
                                key={suite.id} item={suite}/>)}
                        </select>
                        {errors.parent ? errors.parent.map((error, index) => <p className="invalid-feedback"
                                                                                key={index}>{error}</p>) : ''}
                    </div>

                    <div className="form-group mb-3">
                        <label className="form-label">Name</label>
                        <input
                            type="text"
                            className={`form-control ${errors.name ? 'is-invalid' : ''}`}
                            defaultValue={suite.isEditMode ? activeTestSuite.name : ''}
                            {...register("name")}
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
                    {suite.isEditMode ? "Update" : "Add"}
                </Button>
            </Modal.Footer>
        </Modal>
    )
}

export default AddEditSuiteModal;