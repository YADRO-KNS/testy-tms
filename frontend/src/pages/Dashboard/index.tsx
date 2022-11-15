import React from "react";
import {Layout} from "antd";
import ProjectCards from "./ProjectCards";

const {Content} = Layout

const Dashboard = () => {
    return (
        <>
            <Content style={{margin: '24px'}}>
                <div className="site-layout-background" style={{padding: 24, minHeight: 180}}>
                    <p>Overview</p>
                </div>
            </Content>

            <Content style={{margin: '24px'}}>
                <div className="site-layout-background" style={{padding: 24, minHeight: 360}}>
                    <ProjectCards/>
                </div>
            </Content>
        </>
    )
}

export default Dashboard