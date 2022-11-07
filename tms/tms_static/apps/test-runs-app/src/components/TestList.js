import React from "react";
import {useDispatch, useSelector} from "react-redux";
import {showTestDetail} from "../actions/test";
import Badge from 'react-bootstrap/Badge';


export const getStatusBadgeColor = (status) => {
    switch (status) {
        case 'Failed':
            return 'danger'
        case 'Passed':
            return 'success'
        case 'Skipped':
            return 'secondary'
        case 'Broken', 'Blocked':
            return 'warning'
        default:
            return 'dark';
    }
}


const TestRow = ({test}) => {
    const activeTest = useSelector(state => state.test.active)
    const dispatch = useDispatch()

    return (
        <tr onClick={() => dispatch(showTestDetail(test))}  className={`${activeTest === test ? 'table-light' : ''}`}>
            <td>{test.case.name}</td>
            <td>
                <Badge bg={getStatusBadgeColor(test.current_result || 'Untested')}>
                    {test.current_result || 'Untested'}
                </Badge>
            </td>
            <td className="text-end">
                <i className={`bi bi-caret-${activeTest === test ? 'left' : 'right'}`}></i>
            </td>
        </tr>
    )
}

const TestsTable = ({tests}) => {
    return (
        <table className="table table-hover border-light">
            <thead>
            <tr>
                <th scope="col">Name</th>
                <th scope="col">Current Status</th>
                <th scope="col"></th>
            </tr>
            </thead>
            <tbody>
                {tests.map((test) => <TestRow key={test.id} test={test} />)}
            </tbody>
        </table>
    )
}

const EmptyTestList = () => {
    return <p className="text-center">There are no tests.</p>
}

export const TestList = ({tests}) => {
    if (tests.length) {
        return <TestsTable tests={tests}/>
    }

    return <EmptyTestList/>
}