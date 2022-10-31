import {
    FETCH_SUITES_ERROR,
    FETCH_SUITES_PENDING,
    FETCH_SUITES_SUCCESS,
    SET_ACTIVE_SUITE
} from "../actions/treesuites";

const initialState = {
    isShowAddSuiteModal: false,
    pending: true,
    suites: null,
    error: null,
    active: null,
}

const treesuites = (state = initialState, action) => {
    switch (action.type) {
        case SET_ACTIVE_SUITE:
            return {
                ...state,
                active: action.suite_id
            }
        case FETCH_SUITES_PENDING:
            return {
                ...state,
                pending: true,
                error: null,
            }
        case FETCH_SUITES_SUCCESS:
            return {
                ...state,
                pending: false,
                error: null,
                suites: action.payload
            }
        case FETCH_SUITES_ERROR:
            return {
                ...state,
                pending: false,
                error: action.error
            }
        default:
            return state;
    }
}

export default treesuites