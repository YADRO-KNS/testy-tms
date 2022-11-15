import React from "react";
import {Layout} from "antd";
import {PageHeader} from 'antd';
import UsersTable from "../../features/administration/users/UsersTable";

const {Content} = Layout

const Users = () => {

    const routes = [
        {
            path: '#',
            breadcrumbName: 'Administration',
        },
        {
            path: '#',
            breadcrumbName: 'Users',
        },
    ];

    return (
        <>
            <PageHeader
                breadcrumb={{routes}}
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