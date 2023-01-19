import axiosTMS from "./axiosTMS";

export default class ProjectService {

    static getProjects() {
        return axiosTMS.get("api/v1/projects/")
    }

    static getTestPlans() {
        return axiosTMS.get("api/v1/testplans/")
    }

    static getTests() {
        return axiosTMS.get("api/v1/tests/")
    }

    static getUsers() {
        return axiosTMS.get("api/v1/users/")
    }

    static createProject(project: { name: string, description: string }) {
        return axiosTMS.post("api/v1/projects/", project)
    }

    static patchProject(project: { name: string, description: string }, id: number) {
        return axiosTMS.patch("api/v1/projects/" + id.toString() + "/", project)
    }
}
