import React, {Fragment, useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {showTestDetail} from "../actions/test";
import Badge from 'react-bootstrap/Badge';
import {getStatusBadgeColor} from "./TestList"
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';


const TestResultRow = ({result}) => {
    const [isVisible, setIsVisible] = useState(false);

    const handleClick = () => {
        setIsVisible(!isVisible);
    }

    return (
        <Fragment>
            <tr onClick={handleClick}>
                <td>
                    <Badge bg={getStatusBadgeColor(result.status)}>
                        {result.status}
                    </Badge>
                </td>
                <td>{result.user}</td>
                <td>{result.updated_at}</td>
                <td className="text-end">
                    <i className={`bi bi-caret-${isVisible ? 'up' : 'down'}`}></i>
                </td>
            </tr>
            {isVisible &&
                <tr>
                    <td className="p-3 pb-1 bg-light" colSpan="12">
                        <Form>
                            <Form.Group as={Row} className="mb-3">
                                <Form.Label column sm="3" className="opacity-50">
                                    Comment
                                </Form.Label>
                                <Col sm="9">
                                    <Form.Control as="textarea" rows={3} readOnly value={result.comment || "--"}
                                        className="bg-light border disabled"/>
                                </Col>
                            </Form.Group>
                            <Form.Group as={Row} className="mb-3">
                                <Form.Label column sm="4" className="opacity-50">
                                    Test Case Version
                                </Form.Label>
                                <Col sm="8">
                                    <Form.Control plaintext readOnly disabled={true}
                                        value={result.test_case_version || "--"}/>
                                </Col>
                            </Form.Group>
                        </Form>
                    </td>
                </tr>
            }
        </Fragment>
    )
}

const TestsResultsTable = ({test_results}) => {
    return (
        <table className="table table-hover border-light">
            <thead>
            <tr>
                <th scope="col">Status</th>
                <th scope="col">User</th>
                <th scope="col">Date</th>
            </tr>
            </thead>
            <tbody>
                {test_results.map((result) => <TestResultRow key={result.id} result={result} />)}
            </tbody>
        </table>
    )
}

const EmptyTestResultsList = () => {
    return <p className="text-center">There are no results.</p>
}

export const TestResultsList = ({test_results}) => {
    if (test_results.length) {
        return <TestsResultsTable test_results={test_results}/>
    }

    return <EmptyTestResultsList/>
}