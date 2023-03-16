import axiosTMS from "./axiosTMS";
import {myCase} from "../components/models.interfaces";
import localStorageTMS from "./localStorageTMS";

export default class SuiteCaseService {

    static getSuites() {
        const projectId = localStorageTMS.getCurrentProject().id
        if (projectId) {
            return axiosTMS.get("api/v1/suites/?project=" + projectId)
        } else {
            return axiosTMS.get("api/v1/suites/")
        }
    }

    static getSuiteById(id: number) {
        return axiosTMS.get("api/v1/suites/" + id + "/")
    }

    static getCases() {
        const projectId = localStorageTMS.getCurrentProject().id
        if (projectId) {
            return axiosTMS.get("api/v1/cases/?project=" + projectId)
        } else {
            return axiosTMS.get("api/v1/cases/")
        }
    }

    static getCaseById(id: number) {
        return axiosTMS.get("api/v1/cases/" + id + "/")
    }

    static getTreeBySetSuite(id: number) {
        const projectId = localStorageTMS.getCurrentProject().id
        if (projectId) {
            return axiosTMS.get("api/v1/suites/" + id + "/?project=" + projectId + "&treeview=true")
        } else {
            return axiosTMS.get("api/v1/suites/" + id + "/?treeview=true")
        }
    }

    static getTreeSuites() {
        const projectId = localStorageTMS.getCurrentProject().id
        if (projectId) {
            return axiosTMS.get("api/v1/suites/?project=" + projectId + "&treeview=true")
        } else {
            return axiosTMS.get("api/v1/suites/?treeview=true")
        }
    }

    static async deleteCases(idCases: number[]) {
        for (let i = 0; i < idCases.length; i++) {
            await this.deleteCase(idCases[i]).catch((err) => console.log(err))
        }
    }

    static deleteCase(idCase: number) {
        return axiosTMS.delete("api/v1/cases/" + idCase + "/")
    }

    static deleteSuite(idSuite: number) {
        return axiosTMS.delete("api/v1/suites/" + idSuite + "/")
    }

    static createCase(myCase: { name: string; project: number; suite: number; scenario: string; }) {
        return axiosTMS.post("api/v1/cases/", myCase)
    }

    static editCase(myCase: myCase) {
        return axiosTMS.put("api/v1/cases/" + myCase.id + "/", myCase)
    }

    static editSuite(suite: { id: number; parent: number | null; name: string; project: number }) {
        return axiosTMS.put("api/v1/suites/" + suite.id + "/", suite)
    }

    static createSuite(suite: { parent: number | null; name: string; project: number }) {
        return axiosTMS.post("api/v1/suites/", suite)
    }

    static getEmptyDetailedCaseInfo() {
        return {
            show: false,
            myCase: {
                id: -1,
                name: "",
                suite: -1,
                scenario: "",
                description: "",
                project: -1,
                setup: "",
                teardown: "",
                estimate: -1,
                attachments: []
            }
        }
    }
}
