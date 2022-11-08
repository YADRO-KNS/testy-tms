import React, {useEffect, useState} from "react";
import {Button, Modal} from "react-bootstrap";
import {useDispatch, useSelector} from "react-redux";
import {
    fetchModalTestPlans,
    fetchParameters, fetchTestPlans,
    fetchTestSuites,
    hideAddEditTestPlanModal
} from "../actions/testplans";
import {useFieldArray, useForm, Controller} from "react-hook-form";
import CheckboxTree from 'react-checkbox-tree';
import "react-checkbox-tree/lib/react-checkbox-tree.css"
import {patchTestPlan, postTestPlan} from "../api";
import AlertError from "./AlertError";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.min.css"
import FieldErrors from "./FieldErrors";
import {getTestPlan} from "../actions/testplaninfo";

const AddEditTestPlanModal = () => {
    const [checkedTestCases, setCheckedTestCases] = useState([])
    const [expandedTestCases, setExpandedTestCases] = useState([])
    const [checkedParent, setCheckedParent] = useState([])
    const [expandedParent, setExpandedParent] = useState([])
    const [checkedParameters, setCheckedParameters] = useState([])
    const [expandedParameters, setExpandedParameters] = useState([])

    const dispatch = useDispatch()
    const [errors, setErrors] = useState({})
    const {register, control, handleSubmit, reset, setValue} = useForm();
    const addEditModalState = useSelector(state => state.testplans.modals.addEditModal)
    const testPlans = addEditModalState.testPlans
    const testSuites = addEditModalState.testSuites
    const isEditMode = addEditModalState.isEditMode
    const parameters = addEditModalState.parameters
    const isShow = addEditModalState.isShow
    const testPlan = useSelector(state => state.testplaninfo.testplan)

    const title = isEditMode ? `Edit Test Plan '${testPlan.name}'` : 'Add Test Plan'

    const clearForm = () => {
        reset()
        setErrors({})
        setCheckedTestCases([])
        setExpandedTestCases([])
        setCheckedParent([])
        setExpandedParent([])
        setCheckedParameters([])
        setExpandedParameters([])
    }

    const hideModel = () => {
        clearForm()
        dispatch(hideAddEditTestPlanModal())
    }

    const showModal = () => {
        reset()
    }

    useEffect(() => {
        if (isShow) {
            reset({
                due_date: isEditMode ? new Date(testPlan.due_date) : new Date(),
                started_at: isEditMode ? new Date(testPlan.started_at) : new Date(),
            })

            if (isEditMode) {
                if (testPlan.parent) {
                    setCheckedParent([testPlan.parent])
                }

                if (testPlan.parameters) {
                    setCheckedParameters(testPlan.parameters)
                }

                if (testPlan.tests) {
                    setCheckedTestCases(testPlan.tests.map((test) => test.case.id))
                }
            }

            dispatch(fetchModalTestPlans())
            dispatch(fetchTestSuites())
            dispatch(fetchParameters())
        }
    }, [isShow])

    const icons = {
        check: <i className="bi bi-check-square"></i>,
        uncheck: <i className="bi bi-square"></i>,
        halfCheck: <i className="bi bi-check2-square"></i>,
        expandClose: <i className="bi bi-chevron-right"></i>,
        expandOpen: <i className="bi bi-chevron-down"></i>,
        parentClose: <i className="bi bi-folder2"></i>,
        parentOpen: <i className="bi bi-folder2-open"></i>,
        leaf: <i className="bi bi-journal-check"></i>
    };

    const updateTestPlan = async (data) => {
        const response = await patchTestPlan(testPlan.id, data)
        if (response.status === 200) {
            dispatch(hideAddEditTestPlanModal())
            dispatch(getTestPlan(testPlan.id))
            reset()
            dispatch(fetchTestPlans())
        } else {
            setErrors(response.data)
            console.log('Error: ', response)
        }
    }

    const addTestPLan = async (data) => {
        const response = await postTestPlan({...data, project: PROJECT_ID})

        if (response.status === 201) {
            dispatch(hideAddEditTestPlanModal())
            clearForm()
            dispatch(fetchTestPlans())
        } else {
            setErrors(response.data)
            console.log('Error: ', response)
        }
    }

    const onSubmit = async (data) => {
        return isEditMode
            ? await updateTestPlan(data)
            : await addTestPLan(data)
    }

    const {
        fieldsTestCases,
        append: appendTestCases,
        remove: removeTestCases
    } = useFieldArray({control, name: "test_cases",});

    const {
        fieldsParameters,
        append: appendParameters,
        remove: removeParameters
    } = useFieldArray({control, name: "parameters"})

    const onCheckTestCases = (data) => {
        removeTestCases()
        data.filter((item) => !item.startsWith('ts')).map((item) => {
            appendTestCases(item)
        })
        setCheckedTestCases(data)
    }

    const onCheckParent = (data) => {
        const values = data.filter(item => !checkedParent.includes(item))
        setCheckedParent(values)
        setValue("parent", values.length ? values[0] : null)
    }

    const onCheckParameters = (data) => {
        removeParameters()
        appendParameters(data)
        setCheckedParameters(data)
    }

    return (
        <Modal size="lg" show={isShow} onHide={hideModel} onShow={showModal}>
            <Modal.Header closeButton>
                <Modal.Title>{title}</Modal.Title>
            </Modal.Header>
            <Modal.Body>

                <AlertError error={errors}
                            fields={['name', 'parent', 'parameters', 'test_cases', 'started_at', 'due_date']}/>

                <form onSubmit={handleSubmit(onSubmit)} className="needs-validation">

                    <div className="form-group mb-3">
                        <label className="form-label">Parent</label>
                        {testPlans.data
                            ? testPlans.data.length
                                ? <>
                                    <CheckboxTree
                                        checked={checkedParent}
                                        expanded={expandedParent}
                                        nodes={testPlans.data}
                                        onCheck={onCheckParent}
                                        onExpand={setExpandedParent}
                                        icons={icons}
                                        noCascade={true}
                                    />
                                    <input type="hidden" {...register("parent")}
                                           defaultValue={isEditMode ? testPlan.parent : null}/>
                                </> : <p className="text-muted">No test plans</p>
                            : <p>Loading...</p>
                        }
                        <FieldErrors errors={errors.parent}/>

                    </div>

                    <div className="form-group mb-3 col-6">
                        <label className="form-label">Name</label>
                        <input
                            type="text"
                            className={`form-control ${errors.name ? 'is-invalid' : ''}`}
                            defaultValue={isEditMode ? testPlan.name : ''}
                            {...register("name")}
                        />
                        <FieldErrors errors={errors.name}/>
                    </div>

                    {!isEditMode

                        ? <div className="form-group mb-3">
                            <label className="form-label">Parameters</label>
                            {parameters.data
                                ? <CheckboxTree
                                    checked={checkedParameters}
                                    expanded={expandedParameters}
                                    nodes={parameters.data}
                                    onCheck={onCheckParameters}
                                    onExpand={setExpandedParameters}
                                    icons={icons}
                                />
                                : <p>Loading...</p>
                            }

                            {
                                fieldsParameters && fieldsParameters.map(
                                    (item, index) => <input key={item}
                                                            type="hidden" {...register(`parameters.${index}.value`)} />
                                )
                            }
                            <div className={`${errors.parameters ? 'is-invalid' : ''}`}></div>
                            <FieldErrors errors={errors.parameters}/>
                        </div>
                        : <></>
                    }
                    <div className="form-group mb-3">
                        <label className="form-label">Test Cases</label>
                        {testSuites.data
                            ? <CheckboxTree
                                checked={checkedTestCases}
                                expanded={expandedTestCases}
                                nodes={testSuites.data}
                                onCheck={onCheckTestCases}
                                onExpand={setExpandedTestCases}
                                icons={icons}
                            />
                            : <p>Loading...</p>}
                        {
                            fieldsTestCases && fieldsTestCases.map(
                                (item, index) => <input key={item}
                                                        type="hidden" {...register(`test_cases.${index}.value`)} />
                            )
                        }
                        <div className={`${errors.test_cases ? 'is-invalid' : ''}`}></div>
                        <FieldErrors errors={errors.test_cases}/>
                    </div>

                    <div className="row">

                        <div className="form-group mb-3 col-6">
                            <label className="form-label">Started date</label>
                            <Controller
                                control={control}
                                name='started_at'
                                render={({field}) => (
                                    <DatePicker
                                        dateFormat="dd.MM.yyyy"
                                        onChange={(date) => field.onChange(date)}
                                        selected={field.value}
                                        className={`form-control ${errors.started_at ? 'is-invalid' : ''}`}
                                    />
                                )}
                            />
                            <div className={`${errors.started_at ? 'is-invalid' : ''}`}></div>
                            <FieldErrors errors={errors.started_at}/>
                        </div>

                        <div className="form-group mb-3 col-6">
                            <label className="form-label">Due date</label>
                            <Controller
                                control={control}
                                name='due_date'
                                render={({field}) => (
                                    <DatePicker
                                        dateFormat="dd.MM.yyyy"
                                        onChange={field.onChange}
                                        selected={field.value}
                                        className={`form-control ${errors.due_date ? 'is-invalid' : ''}`}
                                    />
                                )}
                            />
                            <div className={`${errors.due_date ? 'is-invalid' : ''}`}></div>
                            <FieldErrors errors={errors.due_date}/>
                        </div>
                    </div>
                </form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="default" onClick={hideModel}>Cancel</Button>
                <Button variant="primary" onClick={handleSubmit(onSubmit)}>{isEditMode ? "Update" : "Add"}</Button>
            </Modal.Footer>
        </Modal>
    )
}

export default AddEditTestPlanModal