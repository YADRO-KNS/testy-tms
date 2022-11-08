import {
    CREATE_SUITE_ERROR,
    CREATE_SUITE_PENDING, CREATE_SUITE_SUCCESS,
    HIDE_ADD_SUITE_MODAL,
    SHOW_ADD_SUITE_MODAL
} from "../actions/suite";

const initialState = {
    isShowAddSuiteModal: false,
    isEditMode: false,
    pending: true,
    error: {},
}

const treesuites = (state = initialState, action) => {
    switch (action.type) {
        case CREATE_SUITE_PENDING:
            return {
                ...state,
                pending: true,
                error: {},
            }
        case CREATE_SUITE_SUCCESS:
            return {
                ...state,
                pending: false,
                error: {}
            }
        case CREATE_SUITE_ERROR:
            return {
                ...state,
                pending: false,
                error: action.error
            }
        case SHOW_ADD_SUITE_MODAL:
            return {
                ...state,
                isShowAddSuiteModal: true,
                isEditMode: action.isEditMode
            }
        case HIDE_ADD_SUITE_MODAL:
            return {
                ...state,
                isShowAddSuiteModal: false,
                isEditMode: false
            }
        default:
            return state;
    }
}

export default treesuites