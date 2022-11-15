import {createApi} from "@reduxjs/toolkit/dist/query/react";
import {baseQueryWithReauth} from "../../../app/apiSlice";

export interface IUserResponse {
    id: string,
    username: string
}

export const usersApi = createApi({
    reducerPath: 'usersApi',
    baseQuery: baseQueryWithReauth,
    endpoints: builder => ({
        getUsers: builder.query<IUserResponse[], void>({
            query: () => 'v1/users/',
        })
    })
})

export const {useGetUsersQuery} = usersApi;