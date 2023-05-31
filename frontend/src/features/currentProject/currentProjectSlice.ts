import {createSlice} from '@reduxjs/toolkit'
import type {PayloadAction} from '@reduxjs/toolkit'
import {project} from "../../components/models.interfaces";

export interface CurrentProjectState {
    value: project | null
}

const initialState: CurrentProjectState = {
    value: null,
}

export const currentProjectSlice = createSlice({
    name: 'currentProject',
    initialState,
    reducers: {
        put: (state, action: PayloadAction<project>) => {
            console.log(state.value)
            return {...state, value: action.payload}
        },
        remove: (state) => {
            return {...state, value: null}
        },
    },
})

// Action creators are generated for each case reducer function
export const {put, remove} = currentProjectSlice.actions

export const currentProjectReducer = currentProjectSlice.reducer