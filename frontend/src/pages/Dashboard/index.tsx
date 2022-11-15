import React from "react";
import {Layout} from "antd";

const {Content} = Layout

const Dashboard = () => {
    return (
        <>
            <Content style={{margin: '24px'}}>
                <div className="site-layout-background" style={{padding: 24, minHeight: 360}}>
                    <p>Dashboard</p>
                </div>
            </Content>
        </>
    )
}

export default Dashboard