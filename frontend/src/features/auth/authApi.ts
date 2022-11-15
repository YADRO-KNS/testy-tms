import {baseQueryWithReauth} from "../../app/apiSlice";
import {createApi} from "@reduxjs/toolkit/dist/query/react";

export const authApi = createApi({
    reducerPath: 'authApi',
    baseQuery: baseQueryWithReauth,
    endpoints: builder => ({
        login: builder.mutation({
            query: credentials => ({
                url: 'token/',
                method: 'POST',
                body: {...credentials}
            })
        })
    })
})

export const {useLoginMutation} = authApi