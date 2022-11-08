import {
    HIDE_ADD_CASE_MODAL,
    HIDE_CASE_DETAIL,
    SHOW_ADD_CASE_MODAL,
    SHOW_CASE_DETAIL
} from "../actions/testcase";

const initialState = {
    add: {
        isShowAddCaseModal: false,
        isEditMode: false
    },
    active: null,
}

const testcase = (state = initialState, action) => {
    switch (action.type) {
        case SHOW_CASE_DETAIL:
            return {
                ...state,
                active: action.payload
            }
        case HIDE_CASE_DETAIL:
            return {
                ...state,
                active: null
            }
        case SHOW_ADD_CASE_MODAL:
            return {
                ...state,
                add: {
                    ...state.add,
                    isShowAddCaseModal: true,
                    isEditMode: action.isEditMode
                }
            }
        case HIDE_ADD_CASE_MODAL:
            return {
                ...state,
                add: {
                    ...state.add,
                    isShowAddCaseModal: false,
                    isEditMode: false
                }
            }
        default:
            return state;
    }
}

export default testcase