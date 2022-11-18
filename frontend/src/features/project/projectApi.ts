import {createApi} from "@reduxjs/toolkit/dist/query/react";
import {baseQueryWithReauth} from "../../app/apiSlice";
import {ISuiteResponse} from "../suite/suiteApi";
import {DataNode} from 'antd/es/tree';

export interface IProjectResponse {
    id: string,
    name: string,
    description: string
}

export const projectApi = createApi({
    reducerPath: 'projectApi',
    baseQuery: baseQueryWithReauth,
    endpoints: builder => ({
        getProjects: builder.query<IProjectResponse[], void>({
            query: () => 'v1/projects/',
        }),
        getProject: builder.query<IProjectResponse, string>({
            query: (projectId) => `v1/projects/${projectId}/`,
        }),
        getProjectSuites: builder.query<DataNode[], any>({
            query: (projectId) => `v1/projects/${projectId}/suites/`,
        }),
    })
})

export const {
    useGetProjectsQuery,
    useGetProjectQuery,
    useGetProjectSuitesQuery,
    useLazyGetProjectSuitesQuery
} = projectApi;