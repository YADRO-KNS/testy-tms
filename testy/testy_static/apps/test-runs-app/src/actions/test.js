import axios from "axios";
import {getTestResultOptionsURL} from "../api";

export const SHOW_TEST_DETAIL = 'SHOW_TEST_DETAIL'
export const HIDE_TEST_DETAIL = 'HIDE_TEST_DETAIL'

export const SHOW_ADD_TEST_RESULT_MODAL = 'SHOW_ADD_TEST_RESULT_MODAL'
export const HIDE_ADD_TEST_RESULT_MODAL = 'HIDE_ADD_TEST_RESULT_MODAL'

export const GET_TEST_RESULT_OPTIONS_PENDING = 'GET_TEST_RESULT_OPTIONS_PENDING';
export const GET_TEST_RESULT_OPTIONS_SUCCESS = 'GET_TEST_RESULT_OPTIONS_SUCCESS';
export const GET_TEST_RESULT_OPTIONS_ERROR = 'GET_TEST_RESULT_OPTIONS_ERROR';


export const showTestDetail = (payload) => {
    return {
        type: SHOW_TEST_DETAIL,
        payload: payload
    }
}

export const hideTestDetail = () => {
    return {
        type: HIDE_TEST_DETAIL
    }
}


export const showAddTestResultModal = () => {
    return {
        type: SHOW_ADD_TEST_RESULT_MODAL,
    }
}

export const hideAddTestResultModal = () => {
    return {
        type: HIDE_ADD_TEST_RESULT_MODAL
    }
}


function getTestResultOptionsPending() {
    return {
        type: GET_TEST_RESULT_OPTIONS_PENDING
    }
}

function getTestResultOptionsSuccess(payload) {
    return {
        type: GET_TEST_RESULT_OPTIONS_SUCCESS,
        payload: payload
    }
}

function getTestResultOptionsError(error) {
    return {
        type: GET_TEST_RESULT_OPTIONS_ERROR,
        error: error
    }
}

export const getTestResultOptions = () => {
    return dispatch => {
        dispatch(getTestResultOptionsPending())

        axios.get(
            getTestResultOptionsURL(),
        ).then(response => {
            dispatch(getTestResultOptionsSuccess(response.data))
        }).catch(thrown => {
            console.log('Error get test result options', thrown)
            dispatch(getTestResultOptionsError(thrown))
        });
    }
}