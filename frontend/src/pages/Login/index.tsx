import React from 'react';
import Auth from "../../features/auth/Auth";
import {Row, Col} from "antd";

const Login: React.FC = () => {
    return (
        <Row justify="center" align="middle" style={{minHeight: '100vh'}}>
            <Col xl={6} lg={8} md={10} sm={12} xs={24}>
                <div>
                    <h1 style={{marginBottom: 24, textAlign: "center"}}>TestY</h1>
                </div>
                <Auth/>
            </Col>
        </Row>
    )
};

export default Login;