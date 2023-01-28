import {project} from "../../../../src/components/projects/project.selection";

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
        });
    });

    it('disagree to create suite on upper level', () => {
        cy.visit('/testcases');
        cy.get('[data-cy="create-suite"]').click()
        cy.get('input[id="nameTextField"]').type("Сьюта для тестирования в cy")
            .should("have.value", "Сьюта для тестирования в cy")
        cy.get('[data-cy="disagree-to-save-suite"]').click()

        cy.contains('div', "Сьюта для тестирования в cy").should('not.exist')
        cy.contains('div', "Количество дочерних сьют: 0").should('not.exist')
    });

    it('agree to create suite on upper level', () => {
        cy.visit('/testcases');
        cy.get('[data-cy="create-suite"]').click()
        cy.get('input[id="nameTextField"]').type("Сьюта для тестирования в cy")
            .should("have.value", "Сьюта для тестирования в cy")
        cy.get('[data-cy="agree-to-save-suite"]').click()

        cy.contains('div', "Сьюта для тестирования в cy")
        cy.contains('div', "Количество дочерних сьют: 0")
    });

    it('create suite on upper level with selected parent', () => {
        cy.visit('/testcases');
        cy.get('[data-cy="create-suite"]').click()
        cy.get('[data-cy="select-parent-suite"]').click().get("li").contains("Сьюта для тестирования в cy").click()
        cy.get('input[id="nameTextField"]').type("Дочерняя сьюта для тестирования в cypress")
            .should("have.value", "Дочерняя сьюта для тестирования в cypress")
        cy.get('[data-cy="agree-to-save-suite"]').click()

        cy.get('div').contains("Сьюта для тестирования в cy")
        cy.get('div').contains("Количество дочерних сьют: 1")
    });

    it('find the created suite by name', () => {
        cy.visit('/testcases');
        cy.get('input[id="searchSuites"]').type("Сьюта для тестирования в cy")
        cy.get('[data-cy="list-of-suites"]').children().should('have.length.greaterThan', 0)
    });

    it('find not existed suite by name', () => {
        cy.visit('/testcases');
        cy.get('input[id="searchSuites"]').type("Такого имени не должно существовать")
        cy.get('[data-cy="list-of-suites"]').children().should('have.length', 0)
    });

    it('create suites in parent suite by button in tree', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.get('[data-cy="add-suite-in-parent"]')
            .each((element, index) => {
                cy.wrap(element).click()
                cy.get('input[id="nameTextField"]').type(`Дочерняя сьюта для тестирования в cy ${index}`)
                    .should("have.value", `Дочерняя сьюта для тестирования в cy ${index}`)
                cy.get('[data-cy="agree-to-save-suite"]').click()
                cy.get('div').contains(`Дочерняя сьюта для тестирования в cy ${index}`)
            })
    });

    it('close-open suite', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains("Дочерняя сьюта для тестирования в cypress").parent().children().eq(0).click()
        cy.contains("Дочерняя сьюта для тестирования в cy 1").should('not.be.visible')

        cy.contains("Дочерняя сьюта для тестирования в cypress").parent().children().eq(0).click()
        cy.contains("Дочерняя сьюта для тестирования в cy 1").should('be.visible')
    });

    it('close all - open all suites', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.get('[data-cy="close-all-suites"]').click()
        cy.contains("Сьюта для тестирования в cy").should('be.visible')
        cy.contains("Дочерняя сьюта для тестирования в cypress").should('not.be.visible')
        cy.contains("Дочерняя сьюта для тестирования в cy 0").should('not.be.visible')
        cy.contains("Дочерняя сьюта для тестирования в cy 1").should('not.be.visible')

        cy.get('[data-cy="open-all-suites"]').click()
        cy.contains("Сьюта для тестирования в cy").should('be.visible')
        cy.contains("Дочерняя сьюта для тестирования в cypress").should('be.visible')
        cy.contains("Дочерняя сьюта для тестирования в cy 0").should('be.visible')
        cy.contains("Дочерняя сьюта для тестирования в cy 1").should('be.visible')
    });

    it('create cases in suite by button in tree', () => {
        let countOfCases = 0;
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.get('[data-cy="add-case-in-suite"]')
            .each((element, index) => {
                cy.wrap(element).click()
                cy.get('input[id="nameCaseTextField"]').type(`Кейс для тестирования в cy ${index}`)
                    .should("have.value", `Кейс для тестирования в cy ${index}`)
                cy.get('textarea[id="scenarioCaseTextField"]').type(`Описание для кейса для тестирования в cy ${index}`)
                    .should("have.value", `Описание для кейса для тестирования в cy ${index}`)
                cy.get('textarea[id="case-setup"]').type(`Подготовка теста для кейса для тестирования в cy ${index}`)
                    .should("have.value", `Подготовка теста для кейса для тестирования в cy ${index}`)
                cy.get('textarea[id="case-teardown"]').type(`Очистка после теста для кейса для тестирования в cy ${index}`)
                    .should("have.value", `Очистка после теста для кейса для тестирования в cy ${index}`)
                cy.get('input[id="case-time-run"]').type(`123`)
                    .should("have.value", `123`)
                cy.get('[data-cy="agree-to-save-case"]').click()
                countOfCases++
                cy.get('div').contains(`Кейс для тестирования в cy ${index}`)
            })

        cy.get('[data-cy="add-case-in-suite"]')
            .each((element, index) => {
                cy.wrap(element).click()
                cy.get('input[id="nameCaseTextField"]').type(`Кейс для тестирования в cy ${index + countOfCases}`)
                    .should("have.value", `Кейс для тестирования в cy ${index + countOfCases}`)
                cy.get('textarea[id="scenarioCaseTextField"]').type(`Описание для кейса для тестирования в cy ${index + countOfCases}`)
                    .should("have.value", `Описание для кейса для тестирования в cy ${index + countOfCases}`)
                cy.get('[data-cy="agree-to-save-case"]').click()
                cy.get('div').contains(`Кейс для тестирования в cy ${index + countOfCases}`)
            })
    });

    it('open-close detailed info about case by arrow', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains('td', `Кейс для тестирования в cy 0`).parent()
            .children()
            .last()
            .children()
            .last()
            .click()
        cy.get('[data-cy="detailed-info-case-name"]')
            .should('have.text', `Кейс для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-scenario"]')
            .should('have.text', `Описание для кейса для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-setup"]')
            .should('have.text', `Подготовка теста для кейса для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-teardown"]')
            .should('have.text', `Очистка после теста для кейса для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-estimate"]')
            .should('have.text', `123`)
        cy.contains('td', `Кейс для тестирования в cy 0`).parent()
            .children()
            .last()
            .children()
            .last()
            .click()
        cy.get('[data-cy="detailed-info-case-scenario"]')
            .should('not.exist')
    })

    it('open-close detailed info about case by close button', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains('td', `Кейс для тестирования в cy 0`).parent()
            .children()
            .last()
            .children()
            .last()
            .click()
        cy.get('[data-cy="detailed-info-case-name"]').should('have.text', `Кейс для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-scenario"]').should('have.text', `Описание для кейса для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-setup"]').should('have.text', `Подготовка теста для кейса для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-teardown"]').should('have.text', `Очистка после теста для кейса для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-estimate"]').should('have.text', `123`)
        cy.get('[data-cy="close-info-case"]').click()
        cy.get('[data-cy="detailed-info-case-scenario"]')
            .should('not.exist')
    })

    it('switching detailed info about cases', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains('td', `Кейс для тестирования в cy 0`).parent()
            .children()
            .last()
            .children()
            .last()
            .click()
        cy.contains('div', `Описание для кейса для тестирования в cy 0`)

        cy.contains('td', `Кейс для тестирования в cy 1`).parent()
            .children()
            .last()
            .children()
            .last()
            .click()
        cy.contains('div', `Описание для кейса для тестирования в cy 1`)
        cy.contains('div', `Описание для кейса для тестирования в cy 0`).should('not.exist')

        cy.contains('td', `Кейс для тестирования в cy 2`).parent()
            .children()
            .last()
            .children()
            .last()
            .click()
        cy.contains('div', `Описание для кейса для тестирования в cy 2`)
        cy.contains('div', `Описание для кейса для тестирования в cy 1`).should('not.exist')

        cy.get('[data-cy="close-info-case"]').click()
        cy.contains('div', `Описание для кейса для тестирования в cy 2`).should('not.exist')
    })

    it('editing case with open detailed information', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains('td', `Кейс для тестирования в cy 0`).parent()
            .children()
            .last()
            .children()
            .last()
            .click()

        cy.get('[data-cy="detailed-info-case-name"]')
            .should('have.text', `Кейс для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-scenario"]')
            .should('have.text', `Описание для кейса для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-setup"]')
            .should('have.text', `Подготовка теста для кейса для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-teardown"]')
            .should('have.text', `Очистка после теста для кейса для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-estimate"]')
            .should('have.text', `123`)

        cy.contains('td', `Кейс для тестирования в cy 0`).parent()
            .children()
            .last()
            .children()
            .first()
            .children()
            .last()
            .click({force: true})
        cy.get('input[id="nameCaseTextField"]')
            .should("have.value", `Кейс для тестирования в cy 0`)
            .clear()
            .type(`Отредактированный кейс для тестирования в cy 0`)
            .should("have.value", `Отредактированный кейс для тестирования в cy 0`)
        cy.get('textarea[id="scenarioCaseTextField"]')
            .should("have.value", `Описание для кейса для тестирования в cy 0`)
            .clear()
            .type(`Отредактированное описание для кейса для тестирования в cy 0`)
            .should("have.value", `Отредактированное описание для кейса для тестирования в cy 0`)
        cy.get('textarea[id="case-setup"]')
            .should("have.value", `Подготовка теста для кейса для тестирования в cy 0`)
            .clear()
            .type(`Отредактированная подготовка теста для кейса для тестирования в cy 0`)
            .should("have.value", `Отредактированная подготовка теста для кейса для тестирования в cy 0`)
        cy.get('textarea[id="case-teardown"]')
            .should("have.value", `Очистка после теста для кейса для тестирования в cy 0`)
            .clear()
            .type(`Отредактированная очистка после теста для кейса для тестирования в cy 0`)
            .should("have.value", `Отредактированная очистка после теста для кейса для тестирования в cy 0`)
        cy.get('input[id="case-time-run"]')
            .should("have.value", `123`)
            .clear()
            .type(`321`)
            .should("have.value", `321`)
        cy.get('[data-cy="agree-to-save-case"]').click()
        cy.get('[data-cy="detailed-info-case-name"]')
            .should('have.text', `Отредактированный кейс для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-scenario"]')
            .should('have.text', `Отредактированное описание для кейса для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-setup"]')
            .should('have.text', `Отредактированная подготовка теста для кейса для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-teardown"]')
            .should('have.text', `Отредактированная очистка после теста для кейса для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-estimate"]')
            .should('have.text', `321`)
        cy.contains('td', `Отредактированный кейс для тестирования в cy 0`)
    })

    it('deleting case with open detailed information', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains('td', `Отредактированный кейс для тестирования в cy 0`).parent()
            .children()
            .last()
            .children()
            .last()
            .click()

        cy.get('[data-cy="detailed-info-case-name"]')
            .should('have.text', `Отредактированный кейс для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-scenario"]')
            .should('have.text', `Отредактированное описание для кейса для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-setup"]')
            .should('have.text', `Отредактированная подготовка теста для кейса для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-teardown"]')
            .should('have.text', `Отредактированная очистка после теста для кейса для тестирования в cy 0`)
        cy.get('[data-cy="detailed-info-case-estimate"]')
            .should('have.text', `321`)

        cy.contains('td', `Отредактированный кейс для тестирования в cy 0`).parent()
            .children()
            .last()
            .children()
            .first()
            .children()
            .first()
            .click({force: true})
        cy.get('[data-cy="agree-to-delete"]').click()
        cy.contains('td', "Отредактированный кейс для тестирования в cy 1").should('not.exist')
        cy.get('[data-cy="detailed-info-case-scenario"]').should('not.exist')
    })

    it('disagree to edit case', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains('td', `Кейс для тестирования в cy 1`).parent()
            .children()
            .last()
            .children()
            .first()
            .children()
            .last()
            .click({force: true})
        cy.get('input[id="nameCaseTextField"]')
            .should("have.value", `Кейс для тестирования в cy 1`)
            .clear()
            .type(`Отредактированный кейс для тестирования в cy 1`)
            .should("have.value", `Отредактированный кейс для тестирования в cy 1`)
        cy.get('textarea[id="scenarioCaseTextField"]')
            .should("have.value", `Описание для кейса для тестирования в cy 1`)
            .clear()
            .type(`Отредактированное описание для кейса для тестирования в cy 1`)
            .should("have.value", `Отредактированное описание для кейса для тестирования в cy 1`)
        cy.get('[data-cy="disagree-to-save-case"]').click()
        cy.contains('td', "Кейс для тестирования в cy 1")
        cy.contains('td', "Отредактированный кейс для тестирования в cy 0").should('not.exist')
    })

    it('agree to edit case', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains('td', `Кейс для тестирования в cy 1`).parent()
            .children()
            .last()
            .children()
            .first()
            .children()
            .last()
            .click({force: true})
        cy.get('input[id="nameCaseTextField"]')
            .should("have.value", `Кейс для тестирования в cy 1`)
            .clear()
            .type(`Отредактированный кейс для тестирования в cy 1`)
            .should("have.value", `Отредактированный кейс для тестирования в cy 1`)
        cy.get('textarea[id="scenarioCaseTextField"]')
            .should("have.value", `Описание для кейса для тестирования в cy 1`)
            .clear()
            .type(`Отредактированное описание для кейса для тестирования в cy 1`)
            .should("have.value", `Отредактированное описание для кейса для тестирования в cy 1`)
        cy.get('[data-cy="agree-to-save-case"]').click()
        cy.contains('td', "Отредактированный кейс для тестирования в cy 1")
        cy.contains('td', "Кейс для тестирования в cy 1").should('not.exist')
    })

    it('disagree to delete case', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains('td', `Отредактированный кейс для тестирования в cy 1`).parent()
            .children()
            .last()
            .children()
            .first()
            .children()
            .first()
            .click({force: true})
        cy.get('[data-cy="disagree-to-delete"]').click()
        cy.contains('td', "Отредактированный кейс для тестирования в cy 1")
    })

    it('agree to delete case', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains('td', `Отредактированный кейс для тестирования в cy 1`).parent()
            .children()
            .last()
            .children()
            .first()
            .children()
            .first()
            .click({force: true})
        cy.get('[data-cy="agree-to-delete"]').click()
        cy.contains('td', "Отредактированный кейс для тестирования в cy 1").should('not.exist')
    })

    it('delete cases using checkbox', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains('td', `Кейс для тестирования в cy 2`)
            .parent()
            .parent()
            .parent()
            .children()
            .first()
            .children()
            .children()
            .first()
            .click()

        cy.contains('td', `Кейс для тестирования в cy 3`)
            .parent()
            .children()
            .first()
            .click()
        cy.get('[data-cy="delete-cases-using-checkbox"]').click()
        cy.get('[data-cy="agree-to-delete-using-checkbox"]').click()
        cy.contains('td', `Кейс для тестирования в cy 2`).should('not.exist')
        cy.contains('td', `Кейс для тестирования в cy 6`).should('not.exist')
        cy.contains('td', `Кейс для тестирования в cy 3`).should('not.exist')
    })

    it('disagree to edit suite', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains("Дочерняя сьюта для тестирования в cypress").parent().children().eq(1).click()
        cy.get('input[id="nameTextField"]')
            .should("have.value", "Дочерняя сьюта для тестирования в cypress")
            .clear()
            .type("Отредактированная дочерняя сьюта для тестирования в cypress")
            .should("have.value", "Отредактированная дочерняя сьюта для тестирования в cypress")
        cy.get('[data-cy="disagree-to-save-suite"]').click()
        cy.contains("Дочерняя сьюта для тестирования в cypress")
        cy.contains("Отредактированная дочерняя сьюта для тестирования в cypress").should('not.exist')
    });

    it('agree to edit suite', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains("Дочерняя сьюта для тестирования в cypress").parent().children().eq(1).click()
        cy.get('input[id="nameTextField"]')
            .should("have.value", "Дочерняя сьюта для тестирования в cypress")
            .clear()
            .type("Отредактированная дочерняя сьюта для тестирования в cypress")
            .should("have.value", "Отредактированная дочерняя сьюта для тестирования в cypress")
        cy.get('[data-cy="agree-to-save-suite"]').click()
        cy.contains("Отредактированная дочерняя сьюта для тестирования в cypress")
        cy.contains("Дочерняя сьюта для тестирования в cypress").should('not.exist')
    });

    it('disagree to delete suite', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains("Отредактированная дочерняя сьюта для тестирования в cypress").parent().children().eq(2).click()
        cy.get('[data-cy="disagree-to-delete"]').click()
        cy.contains("Отредактированная дочерняя сьюта для тестирования в cypress")
    });

    it('agree to delete suite', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains("Отредактированная дочерняя сьюта для тестирования в cypress").parent().children().eq(2).click()
        cy.get('[data-cy="agree-to-delete"]').click()
        cy.contains("Отредактированная дочерняя сьюта для тестирования в cypress").should('not.exist')
    });

    it('delete project for tests', () => {
        JSON.parse(localStorage.getItem("currentProject") ?? '{"id" : null}').id
        cy.request({
            method: 'DELETE',
            url: 'http://localhost:8001/api/v1/projects/' +
                JSON.parse(localStorage.getItem("currentProject") ?? '{"id" : null}').id + "/",
            headers: {
                Authorization: 'Bearer ' + localStorage.getItem("accessToken"),
                "Content-Type": "application/json"
            }
        })
    });

})
