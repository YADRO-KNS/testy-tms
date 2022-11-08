import {
    GET_SUITE_ERROR,
    GET_SUITE_PENDING,
    GET_SUITE_SUCCESS,
} from "../actions/suiteinfo";


const initialState = {
    pending: true,
    suite: null,
    error: null,
}

const suiteinfo = (state = initialState, action) => {
    switch (action.type) {
        case GET_SUITE_PENDING:
            return {
                ...state,
                pending: true,
                error: null,
            }
        case GET_SUITE_SUCCESS:
            return {
                ...state,
                pending: false,
                error: null,
                suite: action.payload
            }
        case GET_SUITE_ERROR:
            return {
                ...state,
                pending: false,
                error: action.error
            }
        default:
            return state;
    }
}

export default suiteinfo