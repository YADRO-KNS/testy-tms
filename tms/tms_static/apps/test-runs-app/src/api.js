import axios from "axios";

export const baseUrl = `${process.env.API_ROOT}/api/v1/`

export const getTestPlansURL = () => {
    return baseUrl + `projects/${window.PROJECT_ID}/testplans/`
}

export const getTestPlanURL = (test_plan_id) => {
    return baseUrl + `testplans/${test_plan_id}/`
}

export const getTestResultOptionsURL = () => {
    return baseUrl + `test-results/`
}

export const postTestResultURL = (test_id) => {
    return baseUrl + `tests/${test_id}/results/`
}

export const postTestResult = async (data) => {
    return await axios.post(
        postTestResultURL(data.test),
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