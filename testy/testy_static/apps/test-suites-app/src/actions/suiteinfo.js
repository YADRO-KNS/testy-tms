import axios from "axios";
import {getTestSuiteInfoURL, getTestSuitesURL, getTestSuiteURL} from "../api";

export const GET_SUITE_PENDING = 'GET_SUITE_PENDING';
export const GET_SUITE_SUCCESS = 'GET_SUITE_SUCCESS';
export const GET_SUITE_ERROR = 'GET_SUITE_ERROR';

export const SHOW_DELETE_SUITE_MODAL = 'SHOW_DELETE_SUITE_MODAL'
export const HIDE_DELETE_SUITE_MODAL = 'HIDE_DELETE_SUITE_MODAL'

function getSuitePending() {
    return {
        type: GET_SUITE_PENDING
    }
}

function getSuiteSuccess(payload) {
    return {
        type: GET_SUITE_SUCCESS,
        payload: payload
    }
}

function getSuiteError(error) {
    return {
        type: GET_SUITE_ERROR,
        error: error
    }
}

export const getSuite = (suite_id) => {
    return dispatch => {
        dispatch(getSuitePending())

        axios.get(
            getTestSuiteURL(suite_id),
        ).then(response => {
            dispatch(getSuiteSuccess(response.data))
        }).catch(thrown => {
            console.log('Error get suite', thrown)
            dispatch(getSuiteError(thrown))
        });
    }
}