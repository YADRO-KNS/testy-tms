import axios from "axios";
import {getTestPlansURL} from "../api";

export const FETCH_TEST_PLANS_PENDING = 'FETCH_TEST_PLANS_PENDING';
export const FETCH_TEST_PLANS_SUCCESS = 'FETCH_TEST_PLANS_SUCCESS';
export const FETCH_TEST_PLANS_ERROR = 'FETCH_TEST_PLANS_ERROR';

export const SET_ACTIVE_TEST_PLAN = 'SET_ACTIVE_TEST_PLAN';


export const setActiveTestPlan = test_plan_id => {
    return {
        type: SET_ACTIVE_TEST_PLAN,
        test_plan_id: test_plan_id
    }
}

function fetchTestPlansPending() {
    return {
        type: FETCH_TEST_PLANS_PENDING
    }
}

function fetchTestPlansSuccess(payload) {
    return {
        type: FETCH_TEST_PLANS_SUCCESS,
        payload: payload
    }
}

function fetchTestPlansError(error) {
    return {
        type: FETCH_TEST_PLANS_ERROR,
        error: error
    }
}

export const fetchTestPlans = () => {
    return dispatch => {
        dispatch(fetchTestPlansPending())

        axios.get(
            getTestPlansURL(),
        ).then(response => {
            dispatch(fetchTestPlansSuccess(response.data))
        }).catch(thrown => {
            console.log('Error fetch test plans', thrown)
            dispatch(fetchTestPlansError(thrown))
        });
    }
}