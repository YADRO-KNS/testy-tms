/// <reference types="cypress" />
import {project} from "../../src/components/projects/project.selection";

Cypress.Commands.add('loginAndCreateProject', () => {
    return cy.request({
        method: 'POST',
        url: 'http://localhost:8001/api/token/',
        body: {
            username: 'admin', password: 'password'
        }
    }).then((response) => {
        localStorage.setItem("accessToken", response.body.access)
        localStorage.setItem("refreshToken", response.body.refresh)
        cy.request({
            method: 'GET',
            url: 'http://localhost:8001/api/v1/projects/',
            headers: {
                Authorization: 'Bearer ' + localStorage.getItem("accessToken"),
                "Content-Type": "application/json"
            }
        }).then((response) => {
            const project = response.body
                .find((project: project) =>
                    project.description === "Проект для тестирования в cy")
            if (project) {
                localStorage.setItem("currentProject", JSON.stringify(project))
            } else {
                cy.request({
                    method: 'POST',
                    url: 'http://localhost:8001/api/v1/projects/',
                    body: {
                        name: "Проект для тестирования в cy",
                        description: "Проект для тестирования в cy"
                    },
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem("accessToken"),
                        "Content-Type": "application/json",
                    }
                }).then((response) => {
                    localStorage.setItem("currentProject", JSON.stringify(response.body))
                })
            }
        })
    })
})

Cypress.Commands.add('createTestplan', (name: string, started_at: string, due_date: string, parent?: number, test_cases?: number[], parameters?: number[]) => {
    return cy.request({
        method: 'POST',
        url: 'http://localhost:8001/api/v1/testplans/',
        body: {
            project: JSON.parse(localStorage.getItem("currentProject") ?? '{"id" : null}').id,
            name: name,
            started_at: started_at,
            due_date: due_date,
            parent: parent,
            test_cases: test_cases ?? [],
            parameters: parameters ?? [],
        },
        headers: {
            Authorization: 'Bearer ' + localStorage.getItem("accessToken"),
            "Content-Type": "application/json",
        }
    })
})

Cypress.Commands.add('createParameter', (data: string, group_name: string) => {
    return cy.request({
        method: 'POST',
        url: 'http://localhost:8001/api/v1/parameters/',
        body: {
            project: JSON.parse(localStorage.getItem("currentProject") ?? '{"id" : null}').id,
            data: data,
            group_name: group_name
        },
        headers: {
            Authorization: 'Bearer ' + localStorage.getItem("accessToken"),
            "Content-Type": "application/json",
        }
    })
})

Cypress.Commands.add('createSuite', (name: string) => {
    return cy.request({
        method: 'POST',
        url: 'http://localhost:8001/api/v1/suites/',
        body: {
            project: JSON.parse(localStorage.getItem("currentProject") ?? '{"id" : null}').id,
            name: name
        },
        headers: {
            Authorization: 'Bearer ' + localStorage.getItem("accessToken"),
            "Content-Type": "application/json",
        }
    })
})

Cypress.Commands.add('createCase', (suite: number, name: string, scenario: string) => {
    return cy.request({
        method: 'POST',
        url: 'http://localhost:8001/api/v1/cases/',
        body: {
            project: JSON.parse(localStorage.getItem("currentProject") ?? '{"id" : null}').id,
            suite: suite,
            name: name,
            scenario: scenario
        },
        headers: {
            Authorization: 'Bearer ' + localStorage.getItem("accessToken"),
            "Content-Type": "application/json",
        }
    })
})
