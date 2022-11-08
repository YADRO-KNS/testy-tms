import axios from "axios";
import {getTestCaseURL} from "../api";

export const SHOW_ADD_CASE_MODAL = 'SHOW_ADD_CASE_MODAL';
export const HIDE_ADD_CASE_MODAL = 'HIDE_ADD_CASE_MODAL';

export const SHOW_CASE_DETAIL = 'SHOW_CASE_DETAIL'
export const HIDE_CASE_DETAIL = 'HIDE_CASE_DETAIL'


export const showCaseDetail = (payload) => {
    return {
        type: SHOW_CASE_DETAIL,
        payload: payload
    }
}

export const hideCaseDetail = () => {
    return {
        type: HIDE_CASE_DETAIL
    }
}

export const showAddCaseModal = (isEditMode = false) => {
    return {
        type: SHOW_ADD_CASE_MODAL,
        isEditMode: isEditMode
    }
}

export const hideAddCaseModal = () => {
    return {
        type: HIDE_ADD_CASE_MODAL
    }
}

