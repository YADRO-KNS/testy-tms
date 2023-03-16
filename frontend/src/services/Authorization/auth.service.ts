import axiosTMS from "../axiosTMS";
import localStorageTMS from "../localStorageTMS";

export default class AuthService {
    static login(username: string, password: string) {
        return axiosTMS
            .post("api/token/", {username: username, password: password})
            .then((response) => {
                if (response.data.access) {
                    localStorageTMS.setAccessToken(response.data.access)
                    localStorageTMS.setRefreshToken(response.data.refresh)
                }
            })
    }

    static refreshToken() {
        const token = localStorageTMS.getRefreshToken()
        return axiosTMS
            .post("api/token/refresh/", {refresh: token})
            .then((response) => {
                if (response.data.access) {
                    localStorageTMS.setAccessToken(response.data.access)
                }
            })
    }

    static logout() {
        localStorageTMS.removeAccessToken()
        localStorageTMS.removeRefreshToken()
    }

    static getCurrentAccessToken() {
        return localStorageTMS.getAccessToken()
    }
}
