import axios from "axios";

export const baseUrl = `${process.env.API_ROOT}/api/v1/`

export const getProjectTestPlans = (projectId) => {
    return baseUrl + `projects/${projectId}/testplans/`
}

export const getProjectTestSuitesURL = (projectId) => {
    return baseUrl + `projects/${projectId}/suites/`
}

export const getProjectParametersURL = (projectId) => {
    return baseUrl + `projects/${projectId}/parameters/`
}

export const postTestPlanURL = () => {
    return baseUrl + `testplans/`
}

export const postTestPlan = async (data) => {
    return await axios.post(
        postTestPlanURL(),
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