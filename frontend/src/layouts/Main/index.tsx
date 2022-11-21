import React, {FC, useContext, useState} from "react";
import {Layout, Menu} from "antd";
import {PieChartOutlined, SettingOutlined, TableOutlined, UserOutlined} from "@ant-design/icons"
import "./index.css"
import {Link, Outlet} from "react-router-dom"
import Footer from "../Footer";

const {Header, Content, Sider} = Layout;

export const MenuContext = React.createContext<any>("")

const Main: FC = () => {
    const [collapsed, setCollapsed] = useState(false);
    const [activeMenu, setActiveMenu] = useState([])
    const [openSubMenu, setOpenSubMenu] = useState<any>([])

    return (
        <Layout style={{minHeight: '100vh'}}>
            <Sider collapsible collapsed={collapsed} onCollapse={value => setCollapsed(value)}>
                <div className="logo">
                    TestY
                </div>

                <Menu selectedKeys={activeMenu} onOpenChange={setOpenSubMenu} openKeys={openSubMenu} theme="dark" mode="inline">
                    <Menu.Item key="dashboard" icon={<PieChartOutlined/>}>
                        <Link to="/">Dashboard</Link>
                    </Menu.Item>
                    <Menu.SubMenu title="Administration" key="administration" icon={<SettingOutlined/>}>
                        <Menu.Item icon={<TableOutlined/>} key="administration.projects">
                            <Link to="/administration/projects">Projects</Link>
                        </Menu.Item>
                        <Menu.Item icon={<UserOutlined/>} key="administration.users">
                            <Link to="/administration/users">Users</Link>
                        </Menu.Item>
                    </Menu.SubMenu>
                </Menu>

            </Sider>
            <Layout className="site-layout">
                <Header className="site-layout-background" style={{padding: 0}}/>
                <Content>
                    <MenuContext.Provider value={{activeMenu, setActiveMenu, openSubMenu, setOpenSubMenu}}>
                        <Outlet/>
                    </MenuContext.Provider>
                </Content>
                <Footer/>
            </Layout>
        </Layout>
    )
}

export default Main