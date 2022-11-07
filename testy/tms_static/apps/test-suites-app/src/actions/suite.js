export const SHOW_ADD_SUITE_MODAL = 'SHOW_ADD_SUITE_MODAL';
export const HIDE_ADD_SUITE_MODAL = 'HIDE_ADD_SUITE_MODAL';

export const CREATE_SUITE_PENDING = 'CREATE_SUITE_PENDING';
export const CREATE_SUITE_SUCCESS = 'CREATE_SUITE_SUCCESS';
export const CREATE_SUITE_ERROR = 'CREATE_SUITE_ERROR';


export const showAddSuiteModal = (isEditMode = false) => {
    return {
        type: SHOW_ADD_SUITE_MODAL,
        isEditMode: isEditMode
    }
}

export const hideAddSuiteModal = () => {
    return {
        type: HIDE_ADD_SUITE_MODAL,
    }
}

export const createSuitePending = () => {
    return {
        type: CREATE_SUITE_PENDING
    }
}

export const createSuiteSuccess = () => {
    return {
        type: CREATE_SUITE_SUCCESS
    }
}

export const createSuiteError = (error) => {
    return {
        type: CREATE_SUITE_ERROR,
        error: error
    }
}