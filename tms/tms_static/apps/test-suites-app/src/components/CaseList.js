import React, {useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {showCaseDetail} from "../actions/testcase";
import testcase from "../reducers/testcase";


export const CaseRow = ({test_case}) => {
    const dispatch = useDispatch()
    const activeTestCase = useSelector(state => state.testcase.active)

    return (
        <tr onClick={() => dispatch(showCaseDetail(test_case))} className={`${activeTestCase === test_case ? 'table-light' : ''}`}>
            <td>{test_case.name}</td>
            <td>{test_case.estimate}</td>
            <td className="text-end">
                <i className={`bi bi-caret-${activeTestCase === test_case ? 'left' : 'right'}`}></i>
            </td>
        </tr>
    )
}

export const CaseTable = ({test_cases}) => {
    return (
        <table className="table table-hover border-light">
            <thead>
            <tr>
                <th scope="col">Name</th>
                <th scope="col">Estimate</th>
                <th scope="col"></th>
            </tr>
            </thead>
            <tbody>
                {test_cases.map((test_case) => <CaseRow key={test_case.id} test_case={test_case} />)}
            </tbody>
        </table>
    )
}

export const EmptyCaseList = () => {
    return <p className="text-center">Empty case list</p>
}

export const CaseList = ({test_cases}) => {
    if (test_cases.length) {
        return <CaseTable test_cases={test_cases}/>
    }

    return <EmptyCaseList/>
}