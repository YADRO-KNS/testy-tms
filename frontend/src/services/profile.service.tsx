import axiosTMS from "./axiosTMS";

export default class ProfileService {
    static changeUser(id: number,
                      user: { username: string; password: string; first_name?: string, last_name?: string, email?: string }) {
        return axiosTMS.put("api/v1/users/" + id + "/", user)
    }

    static getUser(id: number) {
        return axiosTMS.get("api/v1/users/" + id)
    }
}
