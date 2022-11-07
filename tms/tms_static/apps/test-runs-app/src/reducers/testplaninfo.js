import {
    GET_TEST_PLAN_PENDING,
    GET_TEST_PLAN_SUCCESS,
    GET_TEST_PLAN_ERROR,
} from "../actions/testplaninfo";


const initialState = {
    pending: true,
    testplan: null,
    error: null,
}

const testplaninfo = (state = initialState, action) => {
    switch (action.type) {
        case GET_TEST_PLAN_PENDING:
            return {
                ...state,
                pending: true,
                error: null,
            }
        case GET_TEST_PLAN_SUCCESS:
            return {
                ...state,
                pending: false,
                testplan: action.payload,
                error: null
            }
        case GET_TEST_PLAN_ERROR:
            return {
                ...state,
                pending: false,
                error: action.error
            }
        default:
            return state;
    }
}

export default testplaninfo
