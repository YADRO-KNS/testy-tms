import {project} from "../../../../src/components/models.interfaces";
import localStorageTMS from "../../../../src/services/localStorageTMS";

describe('Testing functionality on the pages of suites and cases', () => {
    beforeEach(() => {
        cy.login()
    })

    afterEach(() => {
        cy.request({
            method: 'GET',
            url: 'http://localhost:8001/api/v1/projects/',
            headers: {
                Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
                "Content-Type": "application/json"
            }
        }).then((response) => {
            const project = response.body.find((project: project) => (
                project.name === "Проект для тестирования в cy" || project.name === "Отредактированный Проект для тестирования в cy"
            ))
            if (project) {
                console.log(project)
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
        cy.visit('/');
        cy.get('[data-cy="project-creation"]').click()
        cy.get('input[id="projectName"]').type("Проект для тестирования в cy")
            .should("have.value", "Проект для тестирования в cy")
        cy.get('textarea[id="projectDescription"]').type("Проект для тестирования в cy")
            .should("have.value", "Проект для тестирования в cy")
        cy.get('[data-cy="button-create-project"]').click()
        cy.get('div').contains("Проект для тестирования в cy")
        cy.get('div').contains("Проект для тестирования в cy")
    })

    it('agree to delete project', () => {
        cy.createProject()
        cy.visit('/');
        cy.get('button svg[data-testid=DeleteIcon]:first').parent().click()
        cy.get('button').contains("Да").click()
        cy.get('div').contains("Проект для тестирования в cy", {matchCase: false})
        cy.get('div').contains("Проект для тестирования в cy", {matchCase: false})
    })

    it('disagree to delete project', () => {
        cy.createProject()
        cy.visit('/');
        cy.get('button svg[data-testid=DeleteIcon]:first').parent().click()
        cy.get('button').contains("Нет").click()
        cy.get('div').contains("Проект для тестирования в cy")
        cy.get('div').contains("Проект для тестирования в cy")
    })

    it('change project name and description', () => {
        let oldName = "Проект для тестирования в cy"
        let oldDescription = "Проект для тестирования в cy"
        let newName = "Отредактированный Проект для тестирования в cy"
        let newDescription = "Отредактированный Проект для тестирования в cy"
        cy.createProject()
        cy.visit('/');
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
