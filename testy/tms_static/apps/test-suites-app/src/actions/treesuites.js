import axios from "axios";
import {getTestSuitesURL} from "../api";

export const FETCH_SUITES_PENDING = 'FETCH_SUITES_PENDING';
export const FETCH_SUITES_SUCCESS = 'FETCH_SUITES_SUCCESS';
export const FETCH_SUITES_ERROR = 'FETCH_SUITES_ERROR';
export const SET_ACTIVE_SUITE = 'SET_ACTIVE_SUITE';

export const setActiveSuite = suite_id => {
    return {
        type: SET_ACTIVE_SUITE,
        suite_id: suite_id
    }
}

function fetchSuitesPending() {
    return {
        type: FETCH_SUITES_PENDING
    }
}

function fetchSuitesSuccess(payload) {
    return {
        type: FETCH_SUITES_SUCCESS,
        payload: payload
    }
}

function fetchSuitesError(error) {
    return {
        type: FETCH_SUITES_ERROR,
        error: error
    }
}

export const fetchSuites = () => {
    return dispatch => {
        dispatch(fetchSuitesPending())

        axios.get(
            getTestSuitesURL(),
        ).then(response => {
            dispatch(fetchSuitesSuccess(response.data))
        }).catch(thrown => {
            console.log('Error fetch suites', thrown)
            dispatch(fetchSuitesError(thrown))
        });
    }
}