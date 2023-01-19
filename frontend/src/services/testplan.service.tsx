import axiosTMS from "./axiosTMS";
import {testPlan} from "../components/models.interfaces";

export default class TestPlanService {
    static getAllTestPlans() {
        return axiosTMS.get("api/v1/testplans/")
    }

    static async getTestPlan(id: number) {
        const testPlanData = await axiosTMS.get("api/v1/testplans/" + id + "/")
        const testPlan: testPlan = testPlanData.data
        for (const i of testPlan.tests) {
            const testResults = await this.getAllTestResults(i.id)
            i.test_results = testResults.data
        }
        return testPlanData
    }

    static editTestPlan(testplan: { parent: null | number; child_test_plans: number[]; name: string; test_cases: number[]; due_date: string; is_archive: boolean; project: number; started_at: string; id: number; parameters: number[]; url: string }) {
        return axiosTMS.put("api/v1/testplans/" + testplan.id, testplan)
    }

    static async deleteTestPlans(id: number[]) {
        for (let i = 0; i < id.length; i++) {
            await this.deleteTestPlan(id[i]).catch((err) => console.log(err))
        }
    }

    static deleteTestPlan(id: number) {
        return axiosTMS.delete("api/v1/testplans/" + id + "/")
    }

    static getTreeTestPlans() {
        const projectId = JSON.parse(localStorage.getItem("currentProject") ?? '{"id" : null}').id
        if (projectId) {
            return axiosTMS.get("api/v1/projects/" + projectId + "/testplans/")
        } else {
            return axiosTMS.get("api/v1/projects/1/testplans/")
        }
    }

    static getParameters() {
        const projectId = JSON.parse(localStorage.getItem("currentProject") ?? '{"id" : null}').id
        if (projectId) {
            return axiosTMS.get("api/v1/parameters/?project=" + projectId)
        } else {
            return axiosTMS.get("api/v1/parameters/")
        }

    }

    static getAllTestResults(id: number) {
        return axiosTMS.get("api/v1/results/?test=" + id)
    }

    static createTestPlan(testPlan: { name: string, project: number, parent: number | null, test_cases: number[], parameters: number[], started_at: string, due_date: string }) {
        return axiosTMS.post("api/v1/testplans/", testPlan)
    }

    static createTestResult(testResult: { status: number, comment: string, execution_time: number | null, test: number }) {
        return axiosTMS.post("api/v1/results/", testResult)
    }

    static getTest(id: number) {
        return axiosTMS.get("api/v1/tests/" + id)
    }
}