export {}

describe('Testing functionality on the pages of testplans', () => {
    beforeEach(() => cy.loginAndCreateProject());
    afterEach(() => cy.deleteProject());
    const started_at = "2002-04-29 14:30:59";
    const due_date = "2006-10-25 14:30:59";

    const createFullTestPlan = () => {
        cy.createTestplan("Родительский для редактирования", started_at, due_date).then((response) => {
            const parent = response.body[0].id
            cy.createParameter("Параметр", "Группа параметров").then((response) => {
                const parameter = response.body.id
                cy.createSuite("Сьюта").then((response) => {
                    cy.createCase(response.body.id, "Кейс", "Описание").then((response) => {
                        cy.createTestplan("Тест-план для редактирования", started_at, due_date, parent, [response.body.id], [parameter])
                    })
                })
            })
        })
    }

    it('disagree to create test plan', () => {
        cy.visit('/testplans');
        cy.get('[data-cy="create-testplan"]').click()
        cy.get('input[id="nameTestPlanTextField"]').type("Тест-план для тестирования в су")
            .should("have.value", "Тест-план для тестирования в су")
        cy.get('[data-cy="disagree-to-create-testplan"]').click()

        cy.contains('div', "Тест-план для тестирования в су").should('not.exist')
    });

    it('agree to create test plan', () => {
        cy.visit('/testplans')
        cy.get('[data-cy="create-testplan"]').click()
        cy.get('input[id="nameTestPlanTextField"]').type("Тест-план для тестирования в су")
            .should("have.value", "Тест-план для тестирования в су")
        cy.get('[data-cy="agree-to-create-testplan"]').click()

        cy.contains('div', "Тест-план для тестирования в су")
        cy.get('[data-cy="breadcrumbs"]').should("have.text", "Тест-планы/Тест-план для тестирования в су")
    });

    it('bar chart before add results', () => {
        let ids: number[] = []
        cy.createSuite("Сьюта для тестирования").then((responseSuite) => {
            cy.createCase(responseSuite.body.id, "Кейс для тестирования 1", "Описание этого кейса").then((response) => ids.push(response.body.id))
            cy.createCase(responseSuite.body.id, "Кейс для тестирования 2", "Описание этого кейса").then((response) => ids.push(response.body.id))
            cy.createCase(responseSuite.body.id, "Кейс для тестирования 3", "Описание этого кейса").then((response) => ids.push(response.body.id))
        })
        cy.createTestplan("Тест-план для тестирования в су", started_at, due_date, null, ids)
        cy.visit('/testplans')
        cy.contains('div', "Тест-план для тестирования в су")
        cy.contains('div', 'Количество дочерних тест-планов: 0. Количество тестов: 3')
        cy.get('[text-anchor="untested"]')
        cy.get('[text-anchor="passed"]').should('not.exist')
        cy.get('[text-anchor="failed"]').should('not.exist')
        cy.get('[text-anchor="skipped"]').should('not.exist')
        cy.get('[text-anchor="broken"]').should('not.exist')
        cy.get('[text-anchor="blocked"]').should('not.exist')
        cy.get('[text-anchor="retest"]').should('not.exist')

        cy.get('div [class="recharts-default-tooltip"]').parent().should('not.be.visible')
        cy.get('div [class="recharts-default-tooltip"]').parent().invoke('show').click({force: true})
            .should('be.visible')
        cy.contains('li', 'passed').contains('0')
        cy.contains('li', 'failed').contains('0')
        cy.contains('li', 'skipped').contains('0')
        cy.contains('li', 'broken').contains('0')
        cy.contains('li', 'blocked').contains('0')
        cy.contains('li', 'retest').contains('0')
        cy.contains('li', 'untested').contains('3')
    });

    it('bar chart after add results', () => {
        let ids: number[] = []
        cy.createSuite("Сьюта для тестирования").then((responseSuite) => {
            cy.createCase(responseSuite.body.id, "Кейс для тестирования 1", "Описание этого кейса").then((response) => ids.push(response.body.id))
            cy.createCase(responseSuite.body.id, "Кейс для тестирования 2", "Описание этого кейса").then((response) => ids.push(response.body.id))
            cy.createCase(responseSuite.body.id, "Кейс для тестирования 3", "Описание этого кейса").then((response) => ids.push(response.body.id))
        })
        cy.createTestplan("Тест-план для тестирования в су", started_at, due_date, null, ids).then(response => {
            const plan = response.body[0].id.toString()
            cy.getTests(plan).then(response => {
                response.body.forEach((test: { id: any; }, index: number) => cy.createTestResult(index, test.id))
            })
        })
        cy.visit('/testplans')
        cy.contains('div', "Тест-план для тестирования в су")
        cy.contains('div', 'Количество дочерних тест-планов: 0. Количество тестов: 3')
        cy.get('[text-anchor="untested"]').should('not.exist')
        cy.get('[text-anchor="passed"]')
        cy.get('[text-anchor="failed"]')
        cy.get('[text-anchor="skipped"]')
        cy.get('[text-anchor="broken"]').should('not.exist')
        cy.get('[text-anchor="blocked"]').should('not.exist')
        cy.get('[text-anchor="retest"]').should('not.exist')

        cy.get('div [class="recharts-default-tooltip"]').parent().should('not.be.visible')
        cy.get('div [class="recharts-default-tooltip"]').parent().invoke('show').click({force: true})
            .should('be.visible')
        cy.contains('li', 'passed').contains('1')
        cy.contains('li', 'failed').contains('1')
        cy.contains('li', 'skipped').contains('1')
        cy.contains('li', 'broken').contains('0')
        cy.contains('li', 'blocked').contains('0')
        cy.contains('li', 'retest').contains('0')
        cy.contains('li', 'untested').contains('0')
    });

    it('create test plan with selected parent', () => {
        cy.createTestplan("Родительский тест-план для тестирования в су", started_at, due_date)
        cy.visit('/testplans')
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
        cy.contains('p', "Дата начала: April 29, 2022 03:00")
        cy.contains('p', "Дата окончания: April 29, 2023 03:00")
    });

    it('edit name of test plan', () => {
        cy.createTestplan("Тест-план для редактирования", started_at, due_date)
        cy.visit('/testplans')
        cy.get('div').contains('Тест-план для редактирования').click()

        cy.get('svg[data-testid="EditIcon"]').click()
        cy.get('input[id="nameTestPlanTextField"]').should("have.value", "Тест-план для редактирования")
            .clear().type("Отредактированный тест-план для тестирования в cy")
        cy.get('[data-cy="agree-to-create-testplan"]').click()

        cy.contains('div', "Отредактированный тест-план для тестирования в cy")
        cy.get('[data-cy="breadcrumbs"]').should("have.text", "Тест-планы/Отредактированный тест-план для тестирования в cy")
    });

    it('edit name of test plan with parent, parameter and test', () => {
        createFullTestPlan()
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

    it('edit test of test plan', () => {
        createFullTestPlan()
        cy.visit('/testplans')
        cy.get('div').contains('Родительский для редактирования').click()
        cy.get('div').contains('Тест-план для редактирования [Параметр]').click()
        cy.get('td').contains('Кейс')
        cy.get('span').contains('Untested')

        cy.createSuite("Новая сьюта").then((response) => {
            cy.createCase(response.body.id, "Новый кейс", "Описание")
        })
        cy.reload()
        cy.get('svg[data-testid="EditIcon"]').click()
        cy.get('span[role="checkbox"]').eq(2).click().should('have.attr', 'aria-checked').and('equal', 'true')
        cy.get('span[role="checkbox"]').eq(3).click().should('have.attr', 'aria-checked').and('equal', 'false')
        cy.get('[data-cy="agree-to-create-testplan"]').click()

        cy.get('td').contains('Кейс').should('not.exist')
        cy.get('td').contains('Новый кейс')
    });

    it('edit dates of test plan', () => {
        createFullTestPlan()
        cy.visit('/testplans')
        cy.get('div').contains('Родительский для редактирования').click()
        cy.get('div').contains('Тест-план для редактирования [Параметр]').click()
        cy.contains('p', "Дата начала: April 29, 2002 18:30")
        cy.contains('p', "Дата окончания: October 25, 2006 18:30")

        cy.get('svg[data-testid="EditIcon"]').click()
        cy.get('[data-cy="testplan-started-at"]').clear().type("29/04/2022")
        cy.get('[data-cy="testplan-due-date"]').clear().type("29/04/2023")
        cy.get('[data-cy="agree-to-create-testplan"]').click()

        cy.contains('p', "Дата начала: April 29, 2022 03:00")
        cy.contains('p', "Дата окончания: April 29, 2023 03:00")
    });

    it('edit parent of test plan', () => {
        createFullTestPlan()
        cy.createTestplan("Новый родительский", started_at, due_date)

        cy.visit('/testplans')
        cy.get('div').contains('Родительский для редактирования').click()
        cy.get('div').contains('Тест-план для редактирования [Параметр]').click()

        cy.get('svg[data-testid="EditIcon"]').click()
        cy.get('div').contains('Родительский для редактирования')
        cy.get('[data-cy="select-parent-test-plan"]').click().get("li").contains("Новый родительский").click()
        cy.get('[data-cy="agree-to-create-testplan"]').click()

        cy.get('[data-cy="breadcrumbs"]').should("have.text",
            "Тест-планы/Новый родительский/Тест-план для редактирования")

        cy.visit('/testplans');
        cy.get('div').contains("Новый родительский").click()
        cy.contains("Тест-план для редактирования [Параметр]")
    });

    it('disagree to delete test plan', () => {
        cy.createTestplan("Тест-план для тестирования в су", started_at, due_date)
        cy.visit('/testplans')
        cy.contains("Удалить").should('not.exist')
        cy.contains('div', "Тест-план для тестирования в су")
        cy.get('input[type="checkbox"]').click()
        cy.contains("Удалить").click()
        cy.contains("Нет").click()
        cy.contains('div', "Тест-план для тестирования в су")
    });

    it('delete test plan', () => {
        cy.createTestplan("Тест-план для тестирования в су", started_at, due_date)
        cy.visit('/testplans')
        cy.contains("Удалить").should('not.exist')
        cy.contains('div', "Тест-план для тестирования в су")
        cy.get('input[type="checkbox"]').click()
        cy.contains("Удалить").click()
        cy.contains("Да").click()
        cy.contains('div', "Тест-план для тестирования в су").should('not.exist')
    });

    it('delete several test plans', () => {
        cy.createTestplan("Тест-план для тестирования в су 1", started_at, due_date)
        cy.createTestplan("Тест-план для тестирования в су 2", started_at, due_date)
        cy.visit('/testplans')
        cy.contains("Удалить").should('not.exist')
        cy.contains('div', "Тест-план для тестирования в су 1")
        cy.contains('div', "Тест-план для тестирования в су 2")
        cy.get('input[type="checkbox"]').each((el) => cy.wrap(el).click())
        cy.contains("Удалить").click()
        cy.contains("Да").click()
        cy.contains('div', "Тест-план для тестирования в су 1").should('not.exist')
        cy.contains('div', "Тест-план для тестирования в су 2").should('not.exist')
    });
})
