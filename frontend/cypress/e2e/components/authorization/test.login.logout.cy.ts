export {}
describe('Testing functionality of the login ang logout', () => {
    it('login', () => {
        cy.visit('/login')
        cy.get('input[id="login"]').type('admin')
        cy.get('input[id="password"]').type('password')
        cy.get('button[type="submit"]').click()
        cy.wait(20)
        cy.url().should('eq', Cypress.config().baseUrl)
    })

    it('login with wrong password', () => {
        cy.visit('/login')
        cy.get('input[id="login"]').type('admin')
        cy.get('input[id="password"]').type('wrong_password')
        cy.get('button[type="submit"]').click()
        cy.wait(20)
        cy.url().should('eq', Cypress.config().baseUrl + 'login')
    })

    it('refresh of access token', () => {
        cy.request({
            method: 'POST',
            url: 'http://localhost:8001/api/token/',
            body: {
                username: 'admin', password: 'password'
            }
        }).then((response) => {
            // simulation of token changes on the server over time
            localStorage.setItem("accessToken", response.body.refresh)
            localStorage.setItem("refreshToken", response.body.refresh)

            cy.visit('/')
            cy.wait(20)
            cy.url().should('eq', Cypress.config().baseUrl)
            cy.wait(20)
        })
    });

    it('logout', () => {
        cy.request({
            method: 'POST',
            url: 'http://localhost:8001/api/token/',
            body: {
                username: 'admin', password: 'password'
            }
        }).then((response) => {
            localStorage.setItem("accessToken", response.body.access)
            localStorage.setItem("refreshToken", response.body.refresh)

            cy.visit('/')
            cy.get('header button[type="button"]:last').click()
            cy.get('[data-cy="logout"]').click()
            cy.url().should('eq', Cypress.config().baseUrl + 'login')
        })
    })
})