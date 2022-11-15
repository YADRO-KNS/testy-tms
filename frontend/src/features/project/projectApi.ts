import {createApi} from "@reduxjs/toolkit/dist/query/react";
import {baseQueryWithReauth} from "../../app/apiSlice";

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
        })
    })
})

export const {useGetProjectsQuery} = projectApi;