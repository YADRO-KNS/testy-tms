import {
    FETCH_PARAMETERS_ERROR,
    FETCH_PARAMETERS_PENDING, FETCH_PARAMETERS_SUCCESS,
    FETCH_MODAL_TEST_PLANS_PENDING,
    FETCH_MODAL_TEST_PLANS_ERROR,
    FETCH_MODAL_TEST_PLANS_SUCCESS,
    FETCH_TEST_SUITES_ERROR,
    FETCH_TEST_SUITES_PENDING,
    FETCH_TEST_SUITES_SUCCESS,
    HIDE_ADD_EDIT_TEST_PLAN_MODAL,
    SHOW_ADD_EDIT_TEST_PLAN_MODAL
} from "../actions/testplans";

const initialState = {
    modals: {
        addEditModal: {
            isShow: false,
            isEditMode: false,
            parentTestPlan: null,
            testPlans: {
                pending: false,
                error: null,
                data: null
            },
            testSuites: {
                pending: false,
                error: null,
                data: null
            },
            parameters: {
                pending: false,
                error: null,
                data: null
            }
        }
    }
}

const makeParametersForTreeView = (items) => {
    const result = []

    items.map((item) => {
        const parameter = {value: item.id, label: item.data}

        if (item.group_name === '') {
            result.push(parameter)
        } else {
            const index = result.findIndex(i => i.label === item.group_name)

            if (index === -1) {
                result.push({
                    value: item.group_name,
                    label: item.group_name,
                    children: [parameter]
                })
            } else {
                result[index].children.push(parameter)
            }
        }
    })

    return result
}

const makeTestPlansForTreeView = (items) => {
    return items.map((item) => {
        return {
            value: item.id,
            label: item.name,
            children: item.children.length ? makeTestPlansForTreeView(item.children) : null
        }
    })
}

const makeTestSuitesForTreeView = (items, cases = []) => {
    const testSuites = items.map((item) => {
        return {
            value: `ts-${item.id}`,
            label: item.name,
            children: makeTestSuitesForTreeView(item.children, item.test_cases),
        }
    })

    const testCases = cases.map((item) => {
        return {
            value: item.id,
            label: item.name,
        }
    })

    return testSuites.concat(testCases)
}

const testplans = (state = initialState, action) => {
    switch (action.type) {
        case SHOW_ADD_EDIT_TEST_PLAN_MODAL:
            return {
                ...state,
                modals: {
                    ...state.modals,
                    addEditModal: {
                        ...state.modals.addEditModal,
                        isShow: true,
                        isEditMode: action.isEditMode
                    }
                }
            }
        case HIDE_ADD_EDIT_TEST_PLAN_MODAL:
            return {
                ...state,
                modals: {
                    ...state.modals,
                    addEditModal: {
                        ...state.modals.addEditModal,
                        isShow: false,
                        isEditMode: false
                    }
                }
            }
        case FETCH_MODAL_TEST_PLANS_PENDING:
            return {
                ...state,
                modals: {
                    ...state.modals,
                    addEditModal: {
                        ...state.modals.addEditModal,
                        testPlans: {
                            ...state.modals.addEditModal.testPlans,
                            pending: true,
                            error: null,
                            data: null
                        }
                    }
                }
            }
        case FETCH_MODAL_TEST_PLANS_ERROR:
            return {
                ...state,
                modals: {
                    ...state.modals,
                    addEditModal: {
                        ...state.modals.addEditModal,
                        testPlans: {
                            ...state.modals.addEditModal.testPlans,
                            pending: false,
                            error: action.error,
                        }
                    }
                }
            }
        case FETCH_MODAL_TEST_PLANS_SUCCESS:
                        return {
                ...state,
                modals: {
                    ...state.modals,
                    addEditModal: {
                        ...state.modals.addEditModal,
                        testPlans: {
                            ...state.modals.addEditModal.testPlans,
                            pending: false,
                            data: makeTestPlansForTreeView(action.payload),
                        }
                    }
                }
            }
        case FETCH_TEST_SUITES_PENDING:
            return {
                ...state,
                modals: {
                    ...state.modals,
                    addEditModal: {
                        ...state.modals.addEditModal,
                        testSuites: {
                            ...state.modals.addEditModal.testSuites,
                            pending: true,
                            error: null,
                            data: null
                        }
                    }
                }
            }
        case FETCH_TEST_SUITES_ERROR:
            return {
                ...state,
                modals: {
                    ...state.modals,
                    addEditModal: {
                        ...state.modals.addEditModal,
                        testSuites: {
                            ...state.modals.addEditModal.testSuites,
                            pending: false,
                            error: action.error,
                        }
                    }
                }
            }
        case FETCH_TEST_SUITES_SUCCESS:
            return {
                ...state,
                modals: {
                    ...state.modals,
                    addEditModal: {
                        ...state.modals.addEditModal,
                        testSuites: {
                            ...state.modals.addEditModal.testSuites,
                            pending: false,
                            data: makeTestSuitesForTreeView(action.payload)
                        }
                    }
                }
            }
        case FETCH_PARAMETERS_PENDING:
            return {
                ...state,
                modals: {
                    ...state.modals,
                    addEditModal: {
                        ...state.modals.addEditModal,
                        parameters: {
                            ...state.modals.addEditModal.parameters,
                            pending: true,
                            error: null,
                            data: null
                        }
                    }
                }
            }
        case FETCH_PARAMETERS_ERROR:
            return {
                ...state,
                modals: {
                    ...state.modals,
                    addEditModal: {
                        ...state.modals.addEditModal,
                        parameters: {
                            ...state.modals.addEditModal.parameters,
                            pending: false,
                            error: action.error,
                        }
                    }
                }
            }
        case FETCH_PARAMETERS_SUCCESS:
            return {
                ...state,
                modals: {
                    ...state.modals,
                    addEditModal: {
                        ...state.modals.addEditModal,
                        parameters: {
                            ...state.modals.addEditModal.parameters,
                            pending: false,
                            data: makeParametersForTreeView(action.payload)
                        }
                    }
                }
            }
        default:
            return state;
    }
}

export default testplans