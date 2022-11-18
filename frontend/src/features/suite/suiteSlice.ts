import {createSlice} from "@reduxjs/toolkit";
import {ISuiteResponse} from "./suiteApi";

interface ISuiteState {
    suite: ISuiteResponse | null
}

const initialState: ISuiteState = {
    suite: null
}

export const suiteSlice = createSlice({
    name: 'suite',
    initialState,
    reducers: {

    }
})