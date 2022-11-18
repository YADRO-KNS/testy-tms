import {createApi} from "@reduxjs/toolkit/dist/query/react";
import {baseQueryWithReauth} from "../../app/apiSlice";

export interface ISuiteResponse {
    id: string,
    name: string,
    parent: string | null
}

export const suiteApi = createApi({
    reducerPath: 'suiteApi',
    baseQuery: baseQueryWithReauth,
    endpoints: builder => ({
        getSuite: builder.query<ISuiteResponse[], any>({
            query: (suiteId) => ({
                url: `v1/suites/${suiteId}/`,
            })
        }),
        createSuite: builder.mutation<ISuiteResponse, any>({
            query: (body) => ({
                url: `v1/suites/`,
                method: 'POST',
                body,
            })
        }),
    })
})

export const {
    useGetSuiteQuery,
    useCreateSuiteMutation,
} = suiteApi