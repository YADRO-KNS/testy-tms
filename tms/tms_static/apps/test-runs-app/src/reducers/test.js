import {
    SHOW_TEST_DETAIL,
    HIDE_TEST_DETAIL,
    SHOW_ADD_TEST_RESULT_MODAL,
    HIDE_ADD_TEST_RESULT_MODAL,
    GET_TEST_RESULT_OPTIONS_PENDING,
    GET_TEST_RESULT_OPTIONS_SUCCESS,
    GET_TEST_RESULT_OPTIONS_ERROR,
} from "../actions/test";

const initialState = {
    add: {
        isShowAddTestResultModal: false,
        pending: true,
        resultOptions: null,
        error: null,
    },
    active: null,
}

const test = (state = initialState, action) => {
    switch (action.type) {
        case SHOW_TEST_DETAIL:
            return {
                ...state,
                active: action.payload
            }
        case HIDE_TEST_DETAIL:
            return {
                ...state,
                active: null
            }
        case SHOW_ADD_TEST_RESULT_MODAL:
            return {
                ...state,
                add: {
                    ...state.add,
                    isShowAddTestResultModal: true
                }
            }
        case GET_TEST_RESULT_OPTIONS_PENDING:
            return {
                ...state,
                add: {
                    ...state.add,
                    pending: true,
                    error: null,
                }
            }
        case GET_TEST_RESULT_OPTIONS_ERROR:
            return {
                ...state,
                add: {
                    ...state.add,
                    pending: false,
                    error: action.error
                }
            }
        case GET_TEST_RESULT_OPTIONS_SUCCESS:
            return {
                ...state,
                add: {
                    ...state.add,
                    pending: false,
                    error: null,
                    resultOptions: action.payload
                }
            }
        case HIDE_ADD_TEST_RESULT_MODAL:
            return {
                ...state,
                add: {
                    ...state.add,
                    isShowAddTestResultModal: false
                }
            }
        default:
            return state;
    }
}

export default test