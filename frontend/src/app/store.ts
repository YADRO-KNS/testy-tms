import {configureStore} from '@reduxjs/toolkit'
import {currentProjectReducer} from "../features/currentProject/currentProjectSlice";
import storage from 'redux-persist/lib/storage/session';
import {persistReducer, persistStore} from 'redux-persist'

const persistConfig = {
    key: 'root',
    storage: storage,
}

const persistedReducer = persistReducer(persistConfig, currentProjectReducer)

export const store = configureStore({
    reducer: {
        currentProject: persistedReducer
    },
})

export const persistor = persistStore(store)

// Infer the `RootState` type from the store itself
export type RootState = ReturnType<typeof store.getState>
