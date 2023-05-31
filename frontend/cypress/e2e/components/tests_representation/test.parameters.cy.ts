export {}

describe('Testing functionality of parameters', () => {
    beforeEach(() => cy.loginAndCreateProject())
    afterEach(() => cy.deleteProject());

    it('select parameter', () => {
        cy.createParameter("Параметр для тестирования в cy", "Группа параметров")
        cy.visit('/testplans');
        cy.get('[data-cy="create-testplan"]').click()
        cy.get('button[title="Toggle"]').click()
        cy.get('span button[title="Toggle"]').eq(1).click()
        cy.get('span[role="checkbox"]').eq(3).click().should('have.attr', 'aria-checked')
            .and('equal', 'true')
    })

    it('create test plan with selected parameter', () => {
        cy.createParameter("Параметр для тестирования", "Группа параметров")
        cy.visit('/testplans');
        cy.get('[data-cy="create-testplan"]').click()
        cy.get('input[id="nameTestPlanTextField"]').type("Тест-план с параметром для тестирования в су")
            .should("have.value", "Тест-план с параметром для тестирования в су")
        cy.get('button[title="Toggle"]').click()
        cy.get('span button[title="Toggle"]').eq(1).click()
        cy.get('span[role="checkbox"]').eq(3).click()
        cy.get('[data-cy="agree-to-create-testplan"]').click()

        cy.contains('div', "Тест-план с параметром для тестирования в су [Параметр для тестирования]")
    });

    it('create test plan with several selected parameters', () => {
        cy.createParameter("Параметр для тестирования 1", "Группа параметров")
        cy.createParameter("Параметр для тестирования 2", "Группа параметров")
        cy.visit('/testplans');
        cy.get('[data-cy="create-testplan"]').click()
        cy.get('input[id="nameTestPlanTextField"]').type("Тест-план с параметрами для тестирования в су")
            .should("have.value", "Тест-план с параметрами для тестирования в су")
        cy.get('button[title="Toggle"]').click()
        cy.get('span button[title="Toggle"]').eq(1).click()
        cy.get('span[role="checkbox"]').eq(3).click()
        cy.get('span[role="checkbox"]').eq(4).click()
        cy.get('[data-cy="agree-to-create-testplan"]').click()

        cy.visit('/testplans');
        cy.contains('div', "Тест-план с параметрами для тестирования в су [Параметр для тестирования 1]")
        cy.contains('div', "Тест-план с параметрами для тестирования в су [Параметр для тестирования 2]")
    });

    it('edit parameters should be impossible', () => {
        cy.createParameter("Параметр для тестирования в cy", "Группа параметров").then(response => {
            console.log(response)
            cy.createTestplan("Тест-план для редактирования в cy", "2022-04-29 00:00:00", "2003-10-25 00:00:00", null, null, [response.body.id])
        })
        cy.visit('/testplans');
        cy.get('div').contains('Тест-план для редактирования в cy').click()
        cy.get('svg[data-testid="EditIcon"]').click()
        cy.contains('li', 'Без параметров').should('have.class', 'rct-disabled')
        cy.contains('li', 'Все параметры').should('have.class', 'rct-disabled')
        cy.get('span[role="checkbox"]').eq(1).should('have.attr', 'aria-checked').and('equal', 'true')
    })

//    TODO тесты на создание параметров
})