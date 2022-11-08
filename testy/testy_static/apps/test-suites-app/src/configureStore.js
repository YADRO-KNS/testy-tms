import createRootReducer from './reducers'
import { createStore, applyMiddleware } from 'redux'
import thunk from 'redux-thunk';
import {composeWithDevTools} from 'redux-devtools-extension/developmentOnly';

export default function configureStore(preloadedState) {
    const store = createStore(
        createRootReducer,
        preloadedState,
        composeWithDevTools(
            applyMiddleware(
                thunk,
            )
        )
    )

    return store
}