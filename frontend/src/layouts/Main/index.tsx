import React, {FC, useState} from "react";
import {Layout, Menu} from "antd";
import {PieChartOutlined, SettingOutlined, TableOutlined, UserOutlined} from "@ant-design/icons"
import "./index.css"
import {Link, Outlet} from "react-router-dom"
import Footer from "../Footer";

const {Header, Content, Sider} = Layout;


const Main: FC = () => {
    const [collapsed, setCollapsed] = useState(false);

    return (
        <Layout style={{minHeight: '100vh'}}>
            <Sider collapsible collapsed={collapsed} onCollapse={value => setCollapsed(value)}>
                <div className="logo">
                    TestY
                </div>
                <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline">
                    <Menu.Item key="1" icon={<PieChartOutlined/>}>
                        <Link to="/">Dashboard</Link>
                    </Menu.Item>
                    <Menu.SubMenu title="Administration" key="sub1" icon={<SettingOutlined/>}>
                        <Menu.Item icon={<TableOutlined/>} key="2">
                            <Link to="/administration/projects">Projects</Link>
                        </Menu.Item>
                        <Menu.Item icon={<UserOutlined/>} key="3">
                            <Link to="/administration/users">Users</Link>
                        </Menu.Item>
                    </Menu.SubMenu>
                </Menu>
            </Sider>
            <Layout className="site-layout">
                <Header className="site-layout-background" style={{padding: 0}}/>
                <Content>
                    <Outlet/>
                </Content>
                <Footer/>
            </Layout>
        </Layout>
    )
}

export default Main