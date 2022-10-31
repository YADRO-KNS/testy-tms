import React, {useState} from "react";
import {Col, Row} from "react-bootstrap";
import TestDetail from "./TestDetail";
import TestPlanDetail from "./TestPlanDetail";

const TestPlanContent = () => {
    const [isShowTestPlanDetail, setIsShowTestPlanDetail] = useState(false)
    const [isShowTestDetail, setIsShowTestDetail] = useState(false)

    return (
        <Row>
            <Col>
                <p>TreeView Test Plans</p>
            </Col>
            {isShowTestPlanDetail ? <Col><TestPlanDetail/></Col> : ""}
            {isShowTestDetail ? <Col><TestDetail/></Col> : ""}
        </Row>
    )
}

export default TestPlanContent