import React from "react";
import {Breadcrumb, Layout} from "antd";
import {PageHeader} from 'antd';
import UsersTable from "../../../features/administration/users/UsersTable";

const {Content} = Layout

const Users = () => {

    const breadcrumbItems = [
        <Breadcrumb.Item key="administration">
            Administration
        </Breadcrumb.Item>,
        <Breadcrumb.Item key="users">
            Users
        </Breadcrumb.Item>,
    ]

    return (
        <>
            <PageHeader
                breadcrumbRender={() => <Breadcrumb>{breadcrumbItems}</Breadcrumb>}
                title="Users"
            >
            </PageHeader>

            <Content style={{margin: '24px'}}>
                <div className="site-layout-background" style={{padding: 24, minHeight: 360}}>
                    <UsersTable/>
                </div>
            </Content>
        </>
    )
}

export default Users