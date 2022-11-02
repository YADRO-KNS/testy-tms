import {
    FETCH_TEST_PLANS_PENDING,
    FETCH_TEST_PLANS_SUCCESS,
    FETCH_TEST_PLANS_ERROR,
    SET_ACTIVE_TEST_PLAN
} from "../actions/testplans";


const initialState = {
    pending: true,
    testplans: null,
    error: null,
    active: null
}


const testplans = (state = initialState, action) => {
    switch (action.type) {
        case SET_ACTIVE_TEST_PLAN:
            return {
                ...state,
                active: action.test_plan_id
            }
        case FETCH_TEST_PLANS_PENDING:
            return {
                ...state,
                pending: true,
                error: null,
            }
        case FETCH_TEST_PLANS_SUCCESS:
            return {
                ...state,
                pending: false,
                error: null,
                testplans: action.payload
            }
        case FETCH_TEST_PLANS_ERROR:
            return {
                ...state,
                pending: false,
                error: action.error
            }
        default:
            return state;
    }
}

export default testplans