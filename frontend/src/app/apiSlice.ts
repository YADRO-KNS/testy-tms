import {fetchBaseQuery} from "@reduxjs/toolkit/dist/query/react";
import {setCredentials, logout} from "../features/auth/authSlice";
import type {
    BaseQueryFn,
    FetchArgs,
    FetchBaseQueryError,
} from '@reduxjs/toolkit/query'
import {RootState} from "./store";

const baseQuery = fetchBaseQuery({
    baseUrl: `${process.env.REACT_APP_API_ROOT}/api/`,
    credentials: 'include',
    prepareHeaders: (headers, {getState}) => {
        const accessToken = (getState() as RootState).auth.accessToken
        if (accessToken) {
            headers.set('Authorization', `Bearer ${accessToken}`)
        }
        return headers
    }
})

export const baseQueryWithReauth: BaseQueryFn<string | FetchArgs,
    unknown,
    FetchBaseQueryError> = async (args, api, extraOptions) => {
    let result = await baseQuery(args, api, extraOptions)
    if (result?.error?.status === 401) {
        console.log('sending refresh token')
        const refreshResult = await baseQuery({
            url: 'token/refresh/',
            method: 'POST',
            body: {'refresh': (api.getState() as RootState).auth.refreshToken}
        }, api, extraOptions)
        console.log(refreshResult)
        if (refreshResult?.data) {
            api.dispatch(setCredentials({...refreshResult.data}))
            result = await baseQuery(args, api, extraOptions)
        } else {
            api.dispatch(logout())
            window.location.href = '/login';
        }
    }

    return result
}