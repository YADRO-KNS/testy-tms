import {statuses} from "../../../../src/components/model.statuses";
import {myCase, planStatistic, test, testPlan, project, testResult} from "../../../../src/components/models.interfaces";
import {suite} from "../../../../src/components/testcases/suites.component";
import moment from "moment";
import localStorageTMS from "../../../../src/services/localStorageTMS";

describe('Testing functionality on the project page', () => {
    let testPlanID = 0;
    let updateDate: string | null = null
    let currentStatistics: planStatistic[] | null = null
    const currentUsername = 'admin'
    const currentPassword = 'password'

    beforeEach(() => {
        cy.request({
            method: 'POST',
            url: 'http://localhost:8001/api/token/',
            body: {
                username: currentUsername, password: currentPassword
            }
        }).then((response) => {
            localStorageTMS.setAccessToken(response.body.access)
            localStorageTMS.setRefreshToken(response.body.refresh)

            cy.request({
                method: 'GET',
                url: 'http://localhost:8001/api/v1/projects/',
                headers: {
                    Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
                    "Content-Type": "application/json"
                }
            }).then((response) => {
                let project: project = response.body
                    .find((project: project) =>
                        project.description === "Проект для тестирования в cy")
                if (project) {
                    localStorageTMS.setCurrentProject(project)
                } else {
                    cy.request({
                        method: 'POST',
                        url: 'http://localhost:8001/api/v1/projects/',
                        body: {
                            name: "Проект для тестирования в cy",
                            description: "Проект для тестирования в cy"
                        },
                        headers: {
                            Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
                            "Content-Type": "application/json",
                        }
                    }).then((response) => {
                        project = response.body
                        localStorageTMS.setCurrentProject(project)
                    })
                }
                cy.request({
                    method: 'GET',
                    url: 'http://localhost:8001/api/v1/tests/',
                    headers: {
                        Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
                        "Content-Type": "application/json"
                    }
                }).then((response) => {
                    const tests: test[] = response.body.filter((test: test) => test.project == project.id)

                    cy.request({
                        method: 'GET',
                        url: 'http://localhost:8001/api/v1/testplans/',
                        headers: {
                            Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
                            "Content-Type": "application/json"
                        }
                    }).then((response) => {
                        let testPlan = response.body
                            .find((plan: testPlan) => plan.title === "Тест-план для cy" &&
                                tests.filter((test) => test.plan == plan.id).length === statuses.length
                            )
                        if (!testPlan) {
                            const casesId = Array<number>()

                            cy.request({
                                method: 'GET',
                                url: 'http://localhost:8001/api/v1/cases/',
                                headers: {
                                    Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
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
                                            Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
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
                                                    Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
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
                                        Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
                                        "Content-Type": "application/json",
                                    }
                                }).then((response) => {
                                    testPlan = response.body
                                    testPlanID = testPlan.id ?? testPlanID
                                })
                            })
                        }
                        if (testPlan) {
                            testPlanID = testPlan.id
                            const currentTests: test[] = tests.filter((test: test) => test.plan === testPlan.id)
                            cy.request({
                                method: 'GET',
                                url: `http://localhost:8001/api/v1/testplans/${testPlanID}/statistics/`,
                                headers: {
                                    Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
                                    "Content-Type": "application/json"
                                }
                            }).then((response) => {
                                const statistics: planStatistic[] = response.body
                                currentStatistics = statistics
                                for (const statistic of statistics) {
                                    if (statistic.value > 1) {
                                        currentTests.forEach((value, index) => {
                                            cy.request({
                                                method: 'POST',
                                                url: 'http://localhost:8001/api/v1/results/',
                                                body: {
                                                    test: value.id,
                                                    status: Array.from(statuses.values())[index].id
                                                },
                                                headers: {
                                                    Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
                                                    "Content-Type": "application/json",
                                                }
                                            })
                                        })
                                        currentStatistics = null
                                        break
                                    }
                                }
                            })
                            cy.request({
                                method: 'GET',
                                url: 'http://localhost:8001/api/v1/results/',
                            }).then(() => {
                                const results: testResult[] = response.body.filter((result: testResult) => result.project == project.id)
                                const tests_ids = currentTests.map((test) => test.id)
                                results.sort((a, b) =>
                                    moment(b.updated_at, "YYYY-MM-DDThh:mm").valueOf() - moment(a.updated_at, "YYYY-MM-DDThh:mm").valueOf())
                                for (let test_result of results) {
                                    if (tests_ids.includes(test_result.test)) {
                                        updateDate = test_result?.updated_at ?
                                            moment(test_result?.updated_at, "DD-MM-YYYYThh:mm")
                                                .format("DD.MM.YYYY") : updateDate
                                        break
                                    }
                                }
                            })
                        }
                    })
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
            url: `http://localhost:8001/api/v1/tests/`,
            headers: {
                Authorization: 'Bearer ' + localStorageTMS.getAccessToken(),
                "Content-Type": "application/json"
            }
        }).then((response) => {
            const curTests: test[] = response.body.filter((test: test) => test.plan == testPlanID)
            if (currentStatistics == null)
                cy.get('tbody tr')
                    .should("contain", `${testPlanID}Тест-план для cy${curTests.length}${"1".repeat(curTests.length)}${updateDate ?? moment().format("DD.MM.YYYY")}${currentUsername}`)
            else {
                let planStatusesValues = ""
                statuses.forEach((status) => {
                    planStatusesValues +=
                        currentStatistics?.find((stat) => stat.label == status.name.toUpperCase())?.value.toString() ?? ""
                })

                cy.get('tbody tr')
                    .should("contain", `${testPlanID}Тест-план для cy${curTests.length}${planStatusesValues}${updateDate ?? moment().format("DD.MM.YYYY")}${currentUsername}`)
            }

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
        cy.contains('Тест-план для cy').should("exist")
    })
})