import localStorageTMS from "../../../../src/services/localStorageTMS";

describe('Testing functionality on the pages of suites and cases', () => {
    beforeEach(() => cy.loginAndCreateProject());

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

    it('go to the suites tree by the id specified in the url', () => {
        let suiteId: number
        const projectId = localStorageTMS.getCurrentProject().id
        cy.request({
            method: 'GET',
            url: `http://localhost:8001/api/v1/suites/?project=${projectId}&treeview=true`,
            headers: {
                Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
                "Content-Type": "application/json"
            }
        }).then((response) => {
            suiteId = response.body[0].id
            cy.visit(`/testcases/${suiteId}`);
        })
        cy.get('div').contains("Сьюта для тестирования в cy")
        cy.get('div').contains("Дочерняя сьюта для тестирования в cypress")
    })

    it('go to the suites tree by the not existed id specified in the url', () => {
        const projectId = localStorageTMS.getCurrentProject().id
        cy.request({
            method: 'GET',
            url: `http://localhost:8001/api/v1/suites/?project=${projectId}&treeview=true`,
            headers: {
                Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
                "Content-Type": "application/json"
            }
        }).then(() => {
            cy.visit(`/testcases/-1`)
        })
        cy.get('div').contains("Сьюта для тестирования в cy")
        cy.get('div').contains("Количество дочерних сьют: 3")
    })

    it('try to create suite without name', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.get('[data-cy="create-suite"]').click()
        cy.get('[data-cy="agree-to-save-suite"]').click()
        cy.get('[data-cy="fill-field-note"]').should('have.length', 1)
    })

    it('try to create case without name/scenario', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.get('[data-cy="create-case"]').click()
        cy.get('[data-cy="agree-to-save-case"]').click()
        cy.get('[data-cy="fill-field-note"]').should('have.length', 2)

        cy.get('input[id="nameCaseTextField"]').type(`Название`)
            .should("have.value", `Название`)
        cy.get('[data-cy="agree-to-save-case"]').click()
        cy.get('[data-cy="fill-field-note"]').should('have.length', 1)
        cy.get('input[id="nameCaseTextField"]').clear()

        cy.get('textarea[id="scenarioCaseTextField"]').type(`Описание`)
            .should("have.value", `Описание`)
        cy.get('[data-cy="agree-to-save-case"]').click()
        cy.get('[data-cy="fill-field-note"]').should('have.length', 1)
    })

    it('create case by main button "Create test-case"', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.get('[data-cy="create-case"]').click()
        cy.get('input[id="nameCaseTextField"]').type(`Кейс для тестирования в cy по главной кнопке`)
            .should("have.value", `Кейс для тестирования в cy по главной кнопке`)
        cy.get('textarea[id="scenarioCaseTextField"]').type(`Описание для кейса для тестирования в cy по главной кнопке`)
            .should("have.value", `Описание для кейса для тестирования в cy по главной кнопке`)
        cy.get('[data-cy="agree-to-save-case"]').click()
        cy.contains('div', `Кейс для тестирования в cy по главной кнопке`)
    })

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

    it('find suites in folder structure panel', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.get('input[id="find-suite-folder-structure"]')
            .should("have.value", "").type("Дочерняя сьюта для тестирования в cy")
            .should('have.value', "Дочерняя сьюта для тестирования в cy")

        cy.get('div').filter(".Mui-selected").should("have.length", 3)
    })

    it('switching suites in folder structure panel', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.get('input[id="find-suite-folder-structure"]')
            .should("have.value", "").type("Дочерняя сьюта для тестирования в cy")
            .should('have.value', "Дочерняя сьюта для тестирования в cy")

        cy.get('div').filter(".Mui-selected").should("have.length", 3)
            .eq(0).should('have.css', 'background-color', 'rgb(166, 196, 229)')

        cy.get('[data-cy="go-next"]').click()
        cy.get('div').filter(".Mui-selected").should("have.length", 3)
            .eq(0).should('not.have.css', 'background-color', 'rgb(166, 196, 229)')
        cy.get('div').filter(".Mui-selected").should("have.length", 3)
            .eq(1).should('have.css', 'background-color', 'rgb(166, 196, 229)')

        cy.get('[data-cy="go-next"]').click()
        cy.get('div').filter(".Mui-selected").should("have.length", 3)
            .eq(1).should('not.have.css', 'background-color', 'rgb(166, 196, 229)')
        cy.get('div').filter(".Mui-selected").should("have.length", 3)
            .eq(2).should('have.css', 'background-color', 'rgb(166, 196, 229)')

        cy.get('[data-cy="go-next"]').click()
        cy.get('div').filter(".Mui-selected").should("have.length", 3)
            .eq(2).should('not.have.css', 'background-color', 'rgb(166, 196, 229)')
        cy.get('div').filter(".Mui-selected").should("have.length", 3)
            .eq(0).should('have.css', 'background-color', 'rgb(166, 196, 229)')

        cy.get('[data-cy="go-back"]').click()
        cy.get('div').filter(".Mui-selected").should("have.length", 3)
            .eq(0).should('not.have.css', 'background-color', 'rgb(166, 196, 229)')
        cy.get('div').filter(".Mui-selected").should("have.length", 3)
            .eq(2).should('have.css', 'background-color', 'rgb(166, 196, 229)')

        cy.get('[data-cy="go-back"]').click()
        cy.get('div').filter(".Mui-selected").should("have.length", 3)
            .eq(2).should('not.have.css', 'background-color', 'rgb(166, 196, 229)')
        cy.get('div').filter(".Mui-selected").should("have.length", 3)
            .eq(1).should('have.css', 'background-color', 'rgb(166, 196, 229)')

        cy.get('[data-cy="go-back"]').click()
        cy.get('div').filter(".Mui-selected").should("have.length", 3)
            .eq(1).should('not.have.css', 'background-color', 'rgb(166, 196, 229)')
        cy.get('div').filter(".Mui-selected").should("have.length", 3)
            .eq(0).should('have.css', 'background-color', 'rgb(166, 196, 229)')
    })

    it('navigate by suite in folder structure panel', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.get('div').contains("Дочерняя сьюта для тестирования в cy 1").should("not.be.visible")

        cy.get('input[id="find-suite-folder-structure"]')
            .should("have.value", "").type("Дочерняя сьюта для тестирования в cy 1")
            .should('have.value', "Дочерняя сьюта для тестирования в cy 1")

        cy.get('div').filter(".Mui-selected").should("have.text", "Дочерняя сьюта для тестирования в cy 1").click()

        cy.get('div').contains("Дочерняя сьюта для тестирования в cy 1").should("be.visible")

    })

    it('search for a non-existent suite and clearing the search field in folder structure panel', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.get('input[id="find-suite-folder-structure"]')
            .should("have.value", "").type("Не существующая дочерняя сьюта")
            .should('have.value', "Не существующая дочерняя сьюта")

        cy.get('div').filter(".Mui-selected").should("have.length", 0)

        cy.get('input[id="find-suite-folder-structure"]')
            .should("have.value", "Не существующая дочерняя сьюта").clear()
            .type("Дочерняя сьюта для тестирования в cy 1").clear()

        cy.get('div').filter(".Mui-selected").should("have.length", 0)
    })

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

    it('select/unselect all using checkbox', () => {
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

        cy.get('span').filter(".Mui-checked").should('have.length', 3)

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

        cy.get('span').filter(".Mui-checked").should('have.length', 0)
    })

    it('select/unselect by one using checkbox', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains('td', `Кейс для тестирования в cy по главной кнопке`)
            .parent()
            .children()
            .first()
            .click()

        cy.contains('td', `Кейс для тестирования в cy 4`)
            .parent()
            .children()
            .first()
            .click()

        cy.contains('td', `Кейс для тестирования в cy 2`)
            .parent()
            .children()
            .first()
            .click()

        cy.contains('td', `Кейс для тестирования в cy 6`)
            .parent()
            .children()
            .first()
            .click()

        cy.contains('td', `Кейс для тестирования в cy 3`)
            .parent()
            .children()
            .first()
            .click()

        cy.contains('td', `Кейс для тестирования в cy 7`)
            .parent()
            .children()
            .first()
            .click()

        cy.get('span').filter(".Mui-checked").should('have.length', 9)

        cy.contains('td', `Кейс для тестирования в cy по главной кнопке`)
            .parent()
            .children()
            .first()
            .click()

        cy.contains('td', `Кейс для тестирования в cy 6`)
            .parent()
            .children()
            .first()
            .click()

        cy.contains('td', `Кейс для тестирования в cy 7`)
            .parent()
            .children()
            .first()
            .click()

        cy.get('span').filter(".Mui-checked").should('have.length', 3)
    })

    it('disagree to delete cases using checkbox', () => {
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
        cy.get('[data-cy="disagree-to-delete-using-checkbox"]').click()
        cy.contains('td', `Кейс для тестирования в cy 2`).should('exist')
        cy.contains('td', `Кейс для тестирования в cy 6`).should('exist')
        cy.contains('td', `Кейс для тестирования в cy 3`).should('exist')
    })

    it('agree to delete cases using checkbox with open detailed info about case', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains('td', `Кейс для тестирования в cy 2`).parent()
            .children()
            .last()
            .children()
            .last()
            .click()

        cy.get('[data-cy="detailed-info-case-name"]').should('have.text', `Кейс для тестирования в cy 2`)
        cy.get('[data-cy="detailed-info-case-scenario"]').should('have.text', `Описание для кейса для тестирования в cy 2`)
        cy.get('[data-cy="detailed-info-case-setup"]').should('have.text', `Подготовка теста для кейса для тестирования в cy 2`)
        cy.get('[data-cy="detailed-info-case-teardown"]').should('have.text', `Очистка после теста для кейса для тестирования в cy 2`)
        cy.get('[data-cy="detailed-info-case-estimate"]').should('have.text', `123`)

        cy.contains('td', `Кейс для тестирования в cy 2`)
            .parent()
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
        cy.get('[data-cy="detailed-info-case-name"]').should('not.exist')
        cy.get('[data-cy="detailed-info-case-scenario"]').should('not.exist')
        cy.get('[data-cy="detailed-info-case-setup"]').should('not.exist')
        cy.get('[data-cy="detailed-info-case-teardown"]').should('not.exist')
        cy.get('[data-cy="detailed-info-case-estimate"]').should('not.exist')
        cy.contains('td', `Кейс для тестирования в cy 2`).should('not.exist')
        cy.contains('td', `Кейс для тестирования в cy 3`).should('not.exist')
    })

    it('agree to delete cases using checkbox without open detailed info about case', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains('td', `Кейс для тестирования в cy 6`)
            .parent()
            .parent()
            .parent()
            .children()
            .first()
            .children()
            .children()
            .first()
            .click()

        cy.get('[data-cy="delete-cases-using-checkbox"]').click()
        cy.get('[data-cy="agree-to-delete-using-checkbox"]').click()
        cy.contains('td', `Кейс для тестирования в cy 6`).should('not.exist')
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

    it('delete the suite with the marked case in the checkbox', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains('td', `Кейс для тестирования в cy 5`)
            .parent()
            .children()
            .first()
            .click()

        cy.contains("Дочерняя сьюта для тестирования в cy 0").parent().children().eq(2).click()
        cy.get('[data-cy="agree-to-delete"]').click()
        cy.contains("Дочерняя сьюта для тестирования в cy 0").should('not.exist')
        cy.contains("Кейс для тестирования в cy 5").should('not.exist')
    });

    it('delete the case marked in the checkbox', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        // Create 7 cases for this test
        for (let index = 0; index <= 6; index++) {
            cy.get('[data-cy="create-case"]').click()
            cy.get('input[id="nameCaseTextField"]').type(`Кейс для тестирования в cy (чекбокс) ${index}`)
                .should("have.value", `Кейс для тестирования в cy (чекбокс) ${index}`)
            cy.get('textarea[id="scenarioCaseTextField"]').type(`Описание для кейса для тестирования в cy (чекбокс) ${index}`)
                .should("have.value", `Описание для кейса для тестирования в cy (чекбокс) ${index}`)
            cy.get('[data-cy="agree-to-save-case"]').click()
            cy.get('div').contains(`Кейс для тестирования в cy (чекбокс) ${index}`)
        }

        for (let index = 0; index <= 6; index++) {
            cy.contains('td', `Кейс для тестирования в cy (чекбокс) ${index}`)
                .parent()
                .children()
                .first()
                .click()
        }

        for (let index = 0; index <= 6; index += 3) {
            cy.contains('td', `Кейс для тестирования в cy (чекбокс) ${index}`).parent()
                .children()
                .last()
                .children()
                .first()
                .children()
                .first()
                .click({force: true})

            cy.get('[data-cy="agree-to-delete"]').click()
            cy.contains(`Кейс для тестирования в cy (чекбокс) ${index}`).should('not.exist')
        }
    });

    it('edit the parent suite at the topmost level', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Сьюта для тестирования в cy").click()

        cy.contains("Сьюта для тестирования в cy").parent().children().eq(1).click()
        cy.get('input[id="nameTextField"]')
            .should("have.value", "Сьюта для тестирования в cy")
            .clear()
            .type("Отредактированная сьюта для тестирования в cy")
            .should("have.value", "Отредактированная сьюта для тестирования в cy")
        cy.get('[data-cy="agree-to-save-suite"]').click()
        cy.contains("Отредактированная сьюта для тестирования в cy")
        cy.contains("Сьюта для тестирования в cy").should('not.exist')
    });

    it('delete the parent suite at the topmost level', () => {
        cy.visit('/testcases');
        cy.get('div').contains("Отредактированная сьюта для тестирования в cy").click()

        cy.contains("Отредактированная сьюта для тестирования в cy").parent().children().eq(2).click()
        cy.get('[data-cy="agree-to-delete"]').click()
        cy.url().should('eq', 'http://localhost:3000/testcases')
    });

    it('delete project for tests', () => {
        cy.request({
            method: 'DELETE',
            url: 'http://localhost:8001/api/v1/projects/' +
                localStorageTMS.getCurrentProject().id + "/",
            headers: {
                Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
                "Content-Type": "application/json"
            }
        })
    });

})
