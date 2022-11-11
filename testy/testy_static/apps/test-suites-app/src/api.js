import axios from "axios";
import {API_ROOT} from "./constants/envrionment";

export const baseUrl = `${API_ROOT}/api/v1/`

export const getTestSuiteURL = (suite_id) => {
    return baseUrl + `suites/${suite_id}/`
}

export const getTestSuitesURL = () => {
    // TODO: передавать project_id через параметр
    return baseUrl + `projects/${window.PROJECT_ID}/suites/`
}

export const postTestSuiteURL = () => {
    return baseUrl + 'suites/'
}

export const postTestCaseURL = () => {
    return baseUrl + 'cases/'
}

export const getTestCaseURL = (test_case_id) => {
    return baseUrl + `cases/${test_case_id}/`
}


export const patchTestCase = async (testCaseId, data) => {
    return await axios.patch(
        getTestCaseURL(testCaseId),
        JSON.stringify(data),
        {
            headers: {
                'X-CSRFToken': CSRF_TOKEN,
                'Content-Type': 'application/json'
            }
        }
    ).then(response => {
        return response
    }).catch(error => {
        return error.response
    });
}

export const postTestCase = async (data) => {
    return await axios.post(
        postTestCaseURL(),
        JSON.stringify(data),
        {
            headers: {
                'X-CSRFToken': CSRF_TOKEN,
                'Content-Type': 'application/json'
            }
        }
    ).then(response => {
        return response
    }).catch(error => {
        return error.response
    });
}

export const patchTestSuite = async (test_suite_id, data) => {
    return await axios.patch(
        getTestSuiteURL(test_suite_id),
        JSON.stringify(data),
        {
            headers: {
                'X-CSRFToken': CSRF_TOKEN,
                'Content-Type': 'application/json'
            }
        }
    ).then(response => {
        return response
    }).catch(error => {
        return error.response
    });
}

export const postTestSuite = async (data) => {
    return await axios.post(
        postTestSuiteURL(),
        JSON.stringify(data),
        {
            headers: {
                'X-CSRFToken': CSRF_TOKEN,
                'Content-Type': 'application/json'
            }
        }
    ).then(response => {
        return response
    }).catch(error => {
        return error.response
    });
}

export const deleteTestSuite = async (test_suite_id) => {
    return await axios.delete(
        getTestSuiteURL(test_suite_id),
        {
            headers: {
                'X-CSRFToken': CSRF_TOKEN,
                'Content-Type': 'application/json'
            }
        }
    ).then(response => {
        return response
    }).catch(error => {
        return error.response
    });
}

export const deleteTestCase = async (test_case_id) => {
    return await axios.delete(
        getTestCaseURL(test_case_id),
        {
            headers: {
                'X-CSRFToken': CSRF_TOKEN,
                'Content-Type': 'application/json'
            }
        }
    ).then(response => {
        return response
    }).catch(error => {
        return error.response
    });
}