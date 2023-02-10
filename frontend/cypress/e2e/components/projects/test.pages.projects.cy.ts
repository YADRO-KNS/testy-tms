import {project} from "../../../../src/components/models.interfaces";

describe('Testing functionality on the pages of suites and cases', () => {
    beforeEach(() => {
        cy.request({
            method: 'POST',
            url: 'http://localhost:8001/api/token/',
            body: {
                username: 'admin', password: 'password'
            }
        }).then((response) => {
            localStorage.setItem("accessToken", response.body.access)
            localStorage.setItem("refreshToken", response.body.refresh)
        })
    })

    afterEach(() => {
        cy.request({
            method: 'GET',
            url: 'http://localhost:8001/api/v1/projects/',
            headers: {
                Authorization: 'Bearer ' + localStorage.getItem("accessToken"),
                "Content-Type": "application/json"
            }
        }).then((response) => {
            const project = response.body.find((project: project) => (
                project.name === "Тестовый проект для cypress" || project.name === "Отредактированный тестовый проект для cypress"
            ))
            if (project) {
                console.log(project)
                cy.request({
                    method: 'DELETE',
                    url: 'http://localhost:8001/api/v1/projects/' + project.id + '/',
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem("accessToken"),
                        "Content-Type": "application/json"
                    }
                })
            }
        })
    })

    const createProject = () => {
        cy.visit('/');
        cy.get('[data-cy="project-creation"]').click()
        cy.get('input[id="projectName"]').type("Тестовый проект для cypress")
            .should("have.value", "Тестовый проект для cypress")
        cy.get('textarea[id="projectDescription"]').type("Проект для тестирования в cypress")
            .should("have.value", "Проект для тестирования в cypress")
        cy.get('[data-cy="button-create-project"]').click()
    }

    it('open and close creation project form', () => {
        cy.visit('/');
        cy.get('[data-cy="project-creation-collapse"]').should((el) => {
            expect(el).to.have.css('height', '0px')
        })
        cy.get('[data-cy="project-creation"]').click()
        cy.get('[data-cy="project-creation-collapse"]').should((el) => {
            expect(el).not.to.have.css('height', '0px')
        })
        cy.get('[data-cy="project-creation"]').click()
        cy.get('[data-cy="project-creation-collapse"]').should((el) => {
            expect(el).to.have.css('height', '0px')
        })
    })

    it('create project', () => {
        createProject()
        cy.get('div').contains("Тестовый проект для cypress")
        cy.get('div').contains("Проект для тестирования в cypress")
    })

    it('agree to delete project', () => {
        createProject()
        cy.get('button svg[data-testid=DeleteIcon]:first').parent().click()
        cy.get('button').contains("Да").click()
        cy.get('div').contains("Тестовый проект для cypress", {matchCase: false})
        cy.get('div').contains("Проект для тестирования в cypress", {matchCase: false})
    })

    it('disagree to delete project', () => {
        createProject()
        cy.get('button svg[data-testid=DeleteIcon]:first').parent().click()
        cy.get('button').contains("Нет").click()
        cy.get('div').contains("Тестовый проект для cypress")
        cy.get('div').contains("Проект для тестирования в cypress")
    })

    it('change project name and description', () => {
        let oldName = "Тестовый проект для cypress"
        let oldDescription = "Проект для тестирования в cypress"
        let newName = "Отредактированный тестовый проект для cypress"
        let newDescription = "Отредактированный проект для тестирования в cypress"
        createProject()
        cy.contains(oldName).click()
        cy.get('[data-cy="openProjectSettingsPage"]').click()
        cy.get('input[id="projectNameEdit"]')
            .should("have.value", oldName)
            .clear()
            .type(newName)
            .should("have.value", newName)
        cy.get('textarea[id="projectDescriptionEdit"]')
            .should("have.value", oldDescription)
            .clear()
            .type(newDescription)
            .should("have.value", newDescription)
        cy.get('[data-cy="button-change-project"]').click()

        cy.visit('/');
        cy.get('div').contains(newName)
        cy.get('div').contains(newDescription)
    })
})
