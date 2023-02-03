import {project} from "../../../../src/components/projects/project.selection";
import {statuses} from "../../../../src/components/model.statuses";
import {myCase, test, testPlan} from "../../../../src/components/models.interfaces";
import {suite} from "../../../../src/components/testcases/suites.component";
import moment from "moment";

describe('Testing functionality on the project page', () => {
    let testPlanID = 0;

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
                let project: project = response.body
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
                        project = response.body
                        localStorage.setItem("currentProject", JSON.stringify(project))
                    })
                }
                cy.request({
                    method: 'GET',
                    url: 'http://localhost:8001/api/v1/testplans/',
                    headers: {
                        Authorization: 'Bearer ' + localStorage.getItem("accessToken"),
                        "Content-Type": "application/json"
                    }
                }).then((response) => {
                    let testPlan: testPlan = response.body
                        .find((plan: testPlan) =>
                            plan.title === "Тест-план для cy" && plan.tests.length >= statuses.length)
                    if (!testPlan) {
                        const casesId = Array<number>()

                        cy.request({
                            method: 'GET',
                            url: 'http://localhost:8001/api/v1/cases/',
                            headers: {
                                Authorization: 'Bearer ' + localStorage.getItem("accessToken"),
                                "Content-Type": "application/json"
                            }
                        }).then((response) => {
                            const cases: myCase[] = response.body.filter((value: myCase) => value.project === project.id)
                            if (cases.length < statuses.length) {
                                cy.request({
                                    method: 'POST',
                                    url: 'http://localhost:8001/api/v1/suites/',
                                    body: {
                                        name: "Сьюта для cy",
                                        project: project.id,
                                    },
                                    headers: {
                                        Authorization: 'Bearer ' + localStorage.getItem("accessToken"),
                                        "Content-Type": "application/json",
                                    }
                                }).then((response) => {
                                    const suite: suite = response.body
                                    statuses.map((status, index) => {
                                        cy.request({
                                            method: 'POST',
                                            url: 'http://localhost:8001/api/v1/cases/',
                                            body: {
                                                name: `Кейс ${index} для cy`,
                                                project: project.id,
                                                suite: suite.id,
                                                scenario: "Описание для cy"
                                            },
                                            headers: {
                                                Authorization: 'Bearer ' + localStorage.getItem("accessToken"),
                                                "Content-Type": "application/json",
                                            }
                                        }).then((response) => {
                                            const curCase: myCase = response.body
                                            casesId.push(curCase.id)
                                        })
                                    })
                                })
                            }

                            cy.request({
                                method: 'POST',
                                url: 'http://localhost:8001/api/v1/testplans/',
                                body: {
                                    name: "Тест-план для cy",
                                    started_at: "2023-01-31T12:02:31.903Z",
                                    test_cases: casesId,
                                    due_date: "2023-01-31T12:02:31.903Z",
                                    project: project.id,
                                },
                                headers: {
                                    Authorization: 'Bearer ' + localStorage.getItem("accessToken"),
                                    "Content-Type": "application/json",
                                }
                            }).then((response) => {
                                testPlan = response.body
                                testPlanID = testPlan.id ?? testPlan
                            })
                        })


                    }
                    cy.request({
                        method: 'GET',
                        url: 'http://localhost:8001/api/v1/tests/',
                        headers: {
                            Authorization: 'Bearer ' + localStorage.getItem("accessToken"),
                            "Content-Type": "application/json"
                        }
                    }).then((response) => {
                        const tests: test[] = response.body.filter((test: test) => test.plan === testPlan.id)
                        tests.forEach((value, index) => {
                            cy.request({
                                method: 'POST',
                                url: 'http://localhost:8001/api/v1/results/',
                                body: {
                                    test: value.id,
                                    status: index
                                },
                                headers: {
                                    Authorization: 'Bearer ' + localStorage.getItem("accessToken"),
                                    "Content-Type": "application/json",
                                }
                            })
                        })
                    })
                    if (testPlan)
                        testPlanID = testPlan.id
                })
            })
        });
    });

    it('display table header', () => {
        cy.visit('/project')
        cy.get('thead tr').contains('th', 'ID').should('be.visible')
        cy.get('thead tr').contains('th', 'НАЗВАНИЕ ТЕСТ-ПЛАНА').should('be.visible')
        cy.get('thead tr').contains('th', 'ВСЕГО ТЕСТОВ').should('be.visible')
        statuses.forEach((value) => {
            cy.get('thead tr').contains('th', value.name.toUpperCase()).scrollIntoView().should('be.visible')
        })
        cy.get('thead tr').contains('th', 'ДАТА ИЗМЕНЕНИЯ').scrollIntoView().should('be.visible')
        cy.get('thead tr').contains('th', 'КЕМ ИЗМЕНЕНО').scrollIntoView().should('be.visible')
    })

    it('display table data', () => {
        cy.visit('/project')
        cy.request({
            method: 'GET',
            url: `http://localhost:8001/api/v1/testplans/${testPlanID}`,
            headers: {
                Authorization: 'Bearer ' + localStorage.getItem("accessToken"),
                "Content-Type": "application/json"
            }
        }).then((response) => {
            const curPlan: testPlan = response.body
            cy.get('tbody tr')
                .should("have.text", `${testPlanID}Тест-план для cy${curPlan.tests.length}${"1".repeat(curPlan.tests.length)}${moment(curPlan.tests[0]?.updated_at ?? curPlan.started_at, "YYYY-MM-DDThh:mm").format("DD.MM.YYYY")}Не назначен`)
        })
    })

    it('filter statuses work', () => {
        cy.visit('/project')
        cy.contains('Фильтр').click()
        statuses.forEach((value) => {
            cy.get('.MuiFormGroup-root').contains(value.name.toUpperCase()).click()
            cy.get('thead tr').contains(value.name.toUpperCase()).should('not.exist')
        })
    })

    it('filter date work', () => {
        cy.visit('/project')
        cy.contains('Фильтр').click()
        cy.get('input[value="01/01/1970"]').clear().type(moment().add(1, 'days').format('DD/MM/YYYY'))
        cy.contains('Тест-план для cy').should('not.exist')

        cy.visit('/project')
        cy.contains('Фильтр').click()
        cy.get(`input[value="${moment().format('DD/MM/YYYY')}"]`).clear().type('01/01/1970')
        cy.contains('Тест-план для cy').should('not.exist')
    })

    it('redirect to testplan page', () => {
        cy.visit('/project')
        cy.get('thead tr th').then((response) => {
            const id = response.val()
            cy.contains('Тест-план для cy').click()
            cy.url().should('include', `/testplans/${id}`)
        })
    })

    it('open/close project settings', () => {
        cy.visit('/project')
        cy.contains('Настройки').click()
        cy.contains('Отменить').click()
    })

    it('switch to my activity', () => {
        cy.visit('/project')
        cy.get('input[type="checkbox"]').click()
        cy.contains('Тест-план для cy').should('not.exist')
    })
})