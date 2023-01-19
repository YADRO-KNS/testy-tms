import axios from "axios";
import authHeader from "./Authorization/auth.header";
import AuthService from "./Authorization/auth.service";

const API_URL = process.env.REACT_APP_API_URL;

const axiosTMS = axios.create({
    baseURL: API_URL,
    headers: undefined,
    data: undefined
})

axiosTMS.interceptors.request
    .use(function (config) {
        if (config.url?.includes("api/v1/")) {
            config.headers = authHeader()
        }

        return config;
    });

axiosTMS.interceptors.response
    .use(function (response) {
            return response;
        },async function (error) {
            const loginUrl = "/login"
            try {
                if (error.response.status === 401) {
                    if (error.config.url === "api/token/refresh/") {
                        localStorage.removeItem("accessToken");
                        localStorage.removeItem("refreshToken");
                        window.location.assign(loginUrl);
                        return Promise.reject(error);
                    }

                    await AuthService.refreshToken()
                    return axiosTMS(error.config);
                }
                return Promise.reject(error);
            } catch {
                window.location.assign(loginUrl);
                return;
            }

        });

export default axiosTMS
