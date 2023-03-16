import localStorageTMS from "../../../../src/services/localStorageTMS";

export {}

describe('Testing functionality on the pages of testplans', () => {
    // @ts-ignore
    beforeEach(() => cy.loginAndCreateProject());

    it('disagree to create test plan', () => {
        cy.visit('/testplans');
        cy.get('[data-cy="create-testplan"]').click()
        cy.get('input[id="nameTestPlanTextField"]').type("Тест-план для тестирования в су")
            .should("have.value", "Тест-план для тестирования в су")
        cy.get('[data-cy="disagree-to-create-testplan"]').click()

        cy.contains('div', "Тест-план для тестирования в су").should('not.exist')
    });

    it('agree to create test plan', () => {
        cy.visit('/testplans');
        cy.get('[data-cy="create-testplan"]').click()
        cy.get('input[id="nameTestPlanTextField"]').type("Тест-план для тестирования в су")
            .should("have.value", "Тест-план для тестирования в су")
        cy.get('[data-cy="agree-to-create-testplan"]').click()

        cy.contains('div', "Тест-план для тестирования в су")
        cy.get('[data-cy="breadcrumbs"]').should("have.text", "Тест-планы/Тест-план для тестирования в су")
    });

    it('create test plan with selected parent', () => {
        cy.createTestplan("Родительский тест-план для тестирования в су", "2006-10-25 14:30:59", "2006-10-25 14:30:59")
        cy.visit('/testplans');
        cy.get('[data-cy="create-testplan"]').click()
        cy.get('input[id="nameTestPlanTextField"]').type("Дочерний тест-план для тестирования в су")
            .should("have.value", "Дочерний тест-план для тестирования в су")
        cy.get('[data-cy="select-parent-test-plan"]').click().get("li").contains("Родительский тест-план для тестирования в су").click()
        cy.get('[data-cy="agree-to-create-testplan"]').click()

        cy.get('[data-cy="breadcrumbs"]').should("have.text",
            "Тест-планы/Родительский тест-план для тестирования в су/Дочерний тест-план для тестирования в су")

        cy.visit('/testplans');
        cy.get('div').contains("Количество дочерних тест-планов: 1. Количество тестов: 0")
        cy.get('div').contains("Родительский тест-план для тестирования в су").click()
        cy.contains("Дочерний тест-план для тестирования в су")
    });

    it('create test plan with selected parameter', () => {
        cy.createParameter("Параметр для тестирования 1", "Группа параметров")
        cy.visit('/testplans');
        cy.get('[data-cy="create-testplan"]').click()
        cy.get('input[id="nameTestPlanTextField"]').type("Тест-план с параметром для тестирования в су")
            .should("have.value", "Тест-план с параметром для тестирования в су")
        cy.contains('span', `Все параметры`).parent().parent()
            .children().first().click() //раскрытие всех параметров
            .parent().parent().children().last().children().children().children().first().click() //раскрытие нужной группы параметров
            .parent().parent().children().last().children().children().children().last().children().eq(1).click() // выбор параметра
        cy.get('[data-cy="agree-to-create-testplan"]').click()

        cy.contains('div', "Тест-план с параметром для тестирования в су [Параметр для тестирования 1]")
    });

    it('create test plan with several selected parameters', () => {
        cy.createParameter("Параметр для тестирования 2", "Группа параметров")
        cy.visit('/testplans');
        cy.get('[data-cy="create-testplan"]').click()
        cy.get('input[id="nameTestPlanTextField"]').type("Тест-план с параметрами для тестирования в су")
            .should("have.value", "Тест-план с параметрами для тестирования в су")
        cy.contains('span', `Все параметры`).parent().parent()
            .children().first().click() //раскрытие всех параметров
            .parent().parent().children().last().children().children().children().first().click() //раскрытие нужной группы параметров
            .parent().parent().children().last().children().children().children().last().children().eq(1).click() // выбор 2 параметра
            .parent().parent().parent().parent().children().eq(0).children().children().eq(1).click() //выбор 1 параметра
        cy.get('[data-cy="agree-to-create-testplan"]').click()

        cy.visit('/testplans');
        cy.contains('div', "Тест-план с параметрами для тестирования в су [Параметр для тестирования 1]")
        cy.contains('div', "Тест-план с параметрами для тестирования в су [Параметр для тестирования 2]")
    });

    it('create test plan with selected test case', () => {
        cy.createSuite("Сьюта для тестирования").then((response) => {
            cy.createCase(response.body.id, "Кейс для тестирования", "Описание этого кейса")
        })
        cy.visit('/testplans');
        cy.get('[data-cy="create-testplan"]').click()
        cy.get('input[id="nameTestPlanTextField"]').type("Тест-план с кейсом для тестирования в су")
            .should("have.value", "Тест-план с кейсом для тестирования в су")
        cy.get('div').contains("Сьюта для тестирования").parent().parent().children().first().click()
        cy.get('[data-cy="agree-to-create-testplan"]').click()

        cy.contains('div', "Тест-план с кейсом для тестирования в су")
        cy.contains('div', "Кейс для тестирования")
    });

    it('create test plan with selected dates', () => {
        cy.visit('/testplans');
        cy.get('[data-cy="create-testplan"]').click()
        cy.get('input[id="nameTestPlanTextField"]').type("Тест-план с датами для тестирования в су")
            .should("have.value", "Тест-план с датами для тестирования в су")
        cy.get('[data-cy="testplan-started-at"]').clear().type("29/04/2022")
        cy.get('[data-cy="testplan-due-date"]').clear().type("29/04/2023")

        cy.get('[data-cy="agree-to-create-testplan"]').click()

        cy.contains('div', "Тест-план с датами для тестирования в су")
        cy.contains('p', "Дата начала: April 29, 2022 00:00")
        cy.contains('p', "Дата окончания: April 29, 2023 00:00")
    });

    it('edit test plan', () => {
        cy.createTestplan("Тест-план для редактирования", "2006-10-25 14:30:59", "2006-10-25 14:30:59")
        cy.visit('/testplans')
        cy.get('div').contains('Тест-план для редактирования').click()

        cy.get('svg[data-testid="EditIcon"]').click()
        cy.get('input[id="nameTestPlanTextField"]').should("have.value", "Тест-план для редактирования")
            .clear().type("Отредактированный тест-план для тестирования в cy")
        cy.get('[data-cy="agree-to-create-testplan"]').click()

        cy.contains('div', "Отредактированный тест-план для тестирования в cy")
        cy.get('[data-cy="breadcrumbs"]').should("have.text", "Тест-планы/Отредактированный тест-план для тестирования в cy")
    });

    it('edit test plan with parent, parameter and test', () => {
        cy.createTestplan("Родительский для редактирования", "2000-01-01 14:30:59", "2000-01-01 14:30:59").then((response) => {
            const parent = response.body[0].id
            cy.createParameter("Параметр", "Группа параметров").then((response) => {
                const parameter = response.body.id
                cy.createSuite("Сьюта").then((response) => {
                    cy.createCase(response.body.id, "Кейс", "Описание").then((response) => {
                        cy.createTestplan("Тест-план для редактирования", "2000-01-01 14:30:59", "2000-01-01 14:30:59", parent, [response.body.id], [parameter])
                    })
                })
            })
        })
        cy.visit('/testplans')
        cy.get('div').contains('Родительский для редактирования').click()
        cy.get('div').contains('Тест-план для редактирования [Параметр]').click()

        cy.get('svg[data-testid="EditIcon"]').click()
        cy.get('input[id="nameTestPlanTextField"]').should("have.value", "Тест-план для редактирования")
            .clear().type("Отредактированный тест-план c родителем, параметром и кейсом для тестирования в cy")
        cy.get('[data-cy="agree-to-create-testplan"]').click()

        cy.contains('div', "Отредактированный тест-план c родителем, параметром и кейсом для тестирования в cy")
        cy.get('[data-cy="breadcrumbs"]').should("have.text",
            "Тест-планы/Родительский для редактирования/Отредактированный тест-план c родителем, параметром и кейсом для тестирования в cy")
    });

    it('disagree to delete test plan', () => {
        cy.visit('/testplans')
        cy.contains("Удалить").should('be.disabled')
        cy.get('div').contains('Тест-план для тестирования в су').parent().parent().parent()
            .children().first().click()
        cy.contains("Удалить").click()
        cy.contains("Нет").click()
        cy.contains('div', "Тест-план для тестирования в су")
    });

    it('delete test plan', () => {
        cy.visit('/testplans')
        cy.contains("Удалить").should('be.disabled')
        cy.get('div').contains('Тест-план для тестирования в су').parent().parent().parent()
            .children().first().click()
        cy.contains("Удалить").click()
        cy.contains("Да").click()
        cy.contains('div', "Тест-план для тестирования в су").should('not.exist')
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
