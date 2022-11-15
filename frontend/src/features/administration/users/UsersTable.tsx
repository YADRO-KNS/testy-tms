import React from "react";
import {IUserResponse, useGetUsersQuery} from "./usersApi";
import {Table, Tag} from "antd";
import ContainerLoader from "../../../components/Loader/ContainerLoader";
import {ColumnsType} from "antd/es/table";
import TagBoolean from "../../../components/TagBoolean";


export const UsersTable: React.FC = () => {

    const {data: users, isLoading} = useGetUsersQuery();

    const columns: ColumnsType<IUserResponse> = [
        {
            title: 'Username',
            dataIndex: 'username',
            key: 'username',
        },
        {
            title: 'Email',
            dataIndex: 'email',
            key: 'email',
        },
        {
            title: 'First name',
            dataIndex: 'first_name',
            key: 'first_name',
        },
        {
            title: 'Last name',
            dataIndex: 'last_name',
            key: 'last_name',
        },
        {
            title: 'Active',
            dataIndex: 'is_active',
            key: 'is_active',
            render: is_active => <TagBoolean value={is_active} trueText="ACTIVE" falseText="NOT ACTIVE" />
        },
    ];

    if (isLoading) {
        return <ContainerLoader/>
    }

    return <Table dataSource={users} columns={columns}/>
}

export default UsersTable