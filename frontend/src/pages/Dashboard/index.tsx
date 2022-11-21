import React, {useContext, useEffect} from "react";
import {Layout} from "antd";
import ProjectCards from "./ProjectCards";
import {MenuContext} from "../../layouts/Main";

const {Content} = Layout

const Dashboard = () => {
    const {setActiveMenu} = useContext(MenuContext)
    useEffect(() => {
        setActiveMenu(["dashboard"])
    }, [])
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