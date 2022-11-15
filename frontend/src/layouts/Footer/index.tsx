import React from "react";
import {Layout} from "antd";
import {CopyrightCircleOutlined} from '@ant-design/icons'

const {Footer} = Layout;

const FooterView = () => {
    return (
        <Footer style={{textAlign: 'center'}}>TestY TMS (0.1.0) Copyright <CopyrightCircleOutlined/> 2022. All rights reserved.</Footer>
    )
}

export default FooterView