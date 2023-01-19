import axios from "axios";
import authHeader from "./auth.header";
import axiosTMS from "../axiosTMS";

const API_URL = process.env.REACT_APP_API_URL;


export default class AuthService {
    static login(username: string, password: string) {
        return axiosTMS
            .post("api/token/", {username: username, password: password})
            .then((response) => {
                if (response.data.access) {
                    localStorage.setItem("currentUsername", username)
                    localStorage.setItem("currentPassword", password)
                    localStorage.setItem("accessToken", response.data.access)
                    localStorage.setItem("refreshToken", response.data.refresh)
                }
            })
    }

    static refreshToken() {
        const token = localStorage.getItem("refreshToken")
        return axiosTMS
            .post("api/token/refresh/", {refresh: token})
            .then((response) => {
                if (response.data.access) {
                    localStorage.setItem("accessToken", response.data.access)
                }
            })
    }

    static logout() {
        axios.get(API_URL + "logout/", {headers: authHeader(), params: {"token": localStorage.getItem('token')}})
            .then(() => {
            })
        localStorage.removeItem("currentUsername")
        localStorage.removeItem("accessToken")
        localStorage.removeItem("refreshToken")
    }

    static getCurrentAccessToken() {
        return localStorage.getItem("accessToken")
    }
}
