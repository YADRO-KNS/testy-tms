/// <reference types="cypress" />
import {attachment, project} from "../../src/components/models.interfaces";
import localStorageTMS from "../../src/services/localStorageTMS";

const login = () => {
    return cy.request({
        method: 'POST', url: 'http://localhost:8001/api/token/',
        body: {
            username: 'admin', password: 'password'
        }
    }).then((response) => {
        localStorageTMS.setAccessToken(response.body.access)
        localStorageTMS.setRefreshToken(response.body.refresh)
    })
}
const createProject = () => {
    return cy.request({
        method: 'GET',
        url: 'http://localhost:8001/api/v1/projects/', headers: {
            Authorization: 'Bearer ' + localStorageTMS.getAccessToken(), "Content-Type": "application/json"
        }
    }).then((response) => {
        const project = response.body.find((project: project) =>
            project.description === "Проект для тестирования в cy")
        if (project) {
            localStorageTMS.setCurrentProject(project)
        } else {
            cy.request({
                method: 'POST',
                url: 'http://localhost:8001/api/v1/projects/', body: {
                    name: "Проект для тестирования в cy", description: "Проект для тестирования в cy"
                }, headers: {
                    Authorization: 'Bearer ' + localStorageTMS.getAccessToken(), "Content-Type": "application/json",
                }
            }).then((response) => {
                localStorageTMS.setCurrentProject(response.body)
            })
        }
    })
}
Cypress.Commands.add('login', () => login())
Cypress.Commands.add('createProject', () => createProject())
Cypress.Commands.add('loginAndCreateProject', () => {
    login().then(() => {
        return createProject()
    })
})

Cypress.Commands.add('deleteProject', () => {
    return cy.request({
        method: 'GET',
        url: 'http://localhost:8001/api/v1/projects/',
        headers: {
            Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
            "Content-Type": "application/json"
        }
    }).then((response) => {
        const project = response.body.find((project: project) => (
            project.name === "Проект для тестирования в cy"
        ))
        if (project) {
            cy.request({
                method: 'DELETE',
                url: 'http://localhost:8001/api/v1/projects/' + project.id + '/',
                headers: {
                    Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
                    "Content-Type": "application/json"
                }
            })
        }
    })
})
Cypress.Commands.add('createTestplan', (name: string, started_at: string, due_date: string, parent?: number, test_cases?: number[], parameters?: number[]) => {
    return cy.request({
        method: 'POST', url: 'http://localhost:8001/api/v1/testplans/',
        body: {
            project: localStorageTMS.getCurrentProject().id,
            name: name, started_at: started_at,
            due_date: due_date, parent: parent,
            test_cases: test_cases ?? [], parameters: parameters ?? [],
        }, headers: {
            Authorization: 'Bearer ' + localStorageTMS.getAccessToken(), "Content-Type": "application/json",
        }
    })
})
Cypress.Commands.add('createParameter', (data: string, group_name: string) => {
    return cy.request({
        method: 'POST', url: 'http://localhost:8001/api/v1/parameters/',
        body: {
            project: localStorageTMS.getCurrentProject().id,
            data: data, group_name: group_name
        }, headers: {
            Authorization: 'Bearer ' + localStorageTMS.getAccessToken(), "Content-Type": "application/json",
        }
    })
})
Cypress.Commands.add('createSuite', (name: string) => {
    return cy.request({
        method: 'POST', url: 'http://localhost:8001/api/v1/suites/',
        body: {
            project: localStorageTMS.getCurrentProject().id,
            name: name
        },
        headers: {
            Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
            "Content-Type": "application/json",
        }
    })
})
Cypress.Commands.add('createCase', (suite: number, name: string, scenario: string, attachments: attachment[] = []) => {
    return cy.request({
        method: 'POST',
        url: 'http://localhost:8001/api/v1/cases/',
        body: {
            project: localStorageTMS.getCurrentProject().id, suite: suite,
            name: name,
            scenario: scenario,
            attachments: attachments
        }, headers: {
            Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
            "Content-Type": "application/json",
        }
    })
})

Cypress.Commands.add('createTestResult', (status: number, test: number ) => {
    return cy.request({
        method: 'POST',
        url: 'http://localhost:8001/api/v1/results/',
        body: {
            status: status,
            test: test
        },
        headers: {
            Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
            "Content-Type": "application/json",
        }
    })
})

Cypress.Commands.add('getTests', (plan: string) => {
    return cy.request({
        method: 'GET',
        url: 'http://localhost:8001/api/v1/tests/?plan=' + plan,
        headers: {
            Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
            "Content-Type": "application/json",
        }
    })
})