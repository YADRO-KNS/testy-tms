export {}

describe('Testing functionality of tests', () => {
    beforeEach(() => cy.loginAndCreateProject());
    afterEach(() => cy.deleteProject());
    const started_at = "2002-04-29 14:30:59";
    const due_date = "2006-10-25 14:30:59";

    it('information about tests in the test plan', () => {
        let ids: number[] = []
        cy.createSuite("Сьюта").then((responseSuite) => {
            cy.createCase(responseSuite.body.id, "Кейс 1", "Описание кейса 1").then((response) => ids.push(response.body.id))
            cy.createCase(responseSuite.body.id, "Кейс 2", "Описание кейса 2").then((response) => ids.push(response.body.id))
            cy.createCase(responseSuite.body.id, "Кейс 3", "Описание кейса 3").then((response) => ids.push(response.body.id))
        })
        cy.createTestplan("Тест-план для тестирования в су", started_at, due_date, null, ids).then(response => {
            const plan = response.body[0].id.toString()
            cy.getTests(plan).then(response => {
                response.body.forEach((test: { id: any; }, index: number) => cy.createTestResult(index, test.id))
            })
        })
        cy.visit('/testplans/')
        cy.get('div').contains('Тест-план для тестирования в су').click()

        cy.get('input[type="checkbox"]').its('length').should('eq', 3)
        cy.contains('tr', 'Кейс 1').within(() => {
            cy.contains('Failed')
            cy.contains('не назначен')
            cy.get('[data-cy="icon-open-detailed-test-info"]')
        })
        cy.contains('tr', 'Кейс 2').within(() => {
            cy.contains('Passed')
            cy.contains('не назначен')
            cy.get('[data-cy="icon-open-detailed-test-info"]')
        })
        cy.contains('tr', 'Кейс 3').within(() => {
            cy.contains('Skipped')
            cy.contains('не назначен')
            cy.get('[data-cy="icon-open-detailed-test-info"]')
        })
        cy.get('input[type="checkbox"]').its('length').should('eq', 3)
    });

    it('detailed information about test', () => {
        let ids: number[] = []
        cy.createSuite("Сьюта").then((responseSuite) => {
            cy.createCase(responseSuite.body.id, "Кейс", "Описание кейса").then((response) => ids.push(response.body.id))
        })
        cy.createTestplan("Тест-план для тестирования в су", started_at, due_date, null, ids).then(response => {
            const plan = response.body[0].id.toString()
            cy.getTests(plan).then(response => {
                const test_id = response.body[0].id
                cy.visit('/testplans/')
                cy.get('div').contains('Тест-план для тестирования в су').click()
                cy.contains('tr', 'Кейс').within(() => {
                    cy.get('input[type="checkbox"]')
                    cy.contains(test_id.toString())
                    cy.contains('Untested')
                    cy.contains('не назначен')
                    cy.get('[data-cy="icon-open-detailed-test-info"]').click()
                })
                cy.contains('tr', 'Кейс').within(() => {
                    cy.get('input[type="checkbox"]')
                    cy.contains(test_id.toString())
                    cy.contains('Untested')
                    cy.contains('не назначен').should('not.exist')
                    cy.get('[data-cy="icon-open-detailed-test-info"]')
                })

                cy.contains('Дата создания:')
                cy.contains('Назначенный пользователь:').parent().contains('не назначен')
            })


        })

    })
})