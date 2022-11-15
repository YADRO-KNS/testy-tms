import {createSlice} from "@reduxjs/toolkit";
import {RootState} from "../../app/store";

export interface IUser {
    username: string,
    email: string
}

export interface authState {
    user: IUser | null,
    accessToken: string | null,
    refreshToken: string | null,
}

const initialState: authState = {
    user: null,
    accessToken: null,
    refreshToken: null,
}

export const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setCredentials: (state, action) => {
            const {access, refresh} = action.payload
            if (access) {
                state.accessToken = access
            }
            state.refreshToken = refresh
        },
        logout: () => initialState,
    }
})

export const {setCredentials, logout} = authSlice.actions;

export default authSlice.reducer;

export const selectAccessToken = (state: RootState) => state.auth.accessToken;
export const selectRefreshToken = (state: RootState) => state.auth.refreshToken;