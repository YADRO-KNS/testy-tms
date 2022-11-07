import axios from "axios";
import {getTestPlanURL} from "../api";

export const GET_TEST_PLAN_PENDING = 'GET_TEST_PLAN_PENDING';
export const GET_TEST_PLAN_SUCCESS = 'GET_TEST_PLAN_SUCCESS';
export const GET_TEST_PLAN_ERROR = 'GET_TEST_PLAN_ERROR';


function getTestPlanPending() {
    return {
        type: GET_TEST_PLAN_PENDING
    }
}

function getTestPlanSuccess(payload) {
    return {
        type: GET_TEST_PLAN_SUCCESS,
        payload: payload
    }
}

function getTestPlanError(error) {
    return {
        type: GET_TEST_PLAN_ERROR,
        error: error
    }
}

export const getTestPlan = (test_plan_id) => {
    return dispatch => {
        dispatch(getTestPlanPending())

        axios.get(
            getTestPlanURL(test_plan_id),
        ).then(response => {
            dispatch(getTestPlanSuccess(response.data))
        }).catch(thrown => {
            console.log('Error get test plan', thrown)
            dispatch(getTestPlanError(thrown))
        });
    }
}