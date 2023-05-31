import localStorageTMS from "../../../../src/services/localStorageTMS";

describe('Testing functionality on the profile page', () => {
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
        })
    })

    it('change first_name, last_name, email', () => {
        cy.visit('/profile')
        cy.get(`#first_name`).clear().type('Admin_Cy')
        cy.get(`#last_name`).clear().type('Adminov_CY')
        cy.get(`#email`).clear().type('admin@cy.com')
        cy.get('#passwordProfile').clear().type(currentPassword)
        cy.get('button[type="submit"]').click()
        cy.contains('Изменения успешно сохранены')

        cy.visit('/profile')
        cy.get(`#first_name`).should('have.value', 'Admin_Cy')
        cy.get(`#last_name`).should('have.value', 'Adminov_CY')
        cy.get(`#email`).should('have.value', 'admin@cy.com')
    });

    it('not submit without username', () => {
        cy.visit('/profile')
        cy.get(`#username`).clear()
        cy.get('#passwordProfile').clear().type(currentPassword)
        cy.get('button[type="submit"]').click()
        cy.contains('Изменения успешно сохранены').should('not.exist')
    });

    it('not submit profile change without current password', () => {
        cy.visit('/profile')
        cy.get('button[type="submit"]').click()
        cy.contains('Изменения успешно сохранены').should('not.exist')
    });

    it('show alert when current password is wrong', () => {
        cy.visit('/profile')
        cy.get('#passwordProfile').clear().type(currentPassword + "idontremember")
        cy.get('button[type="submit"]').click()
        cy.contains('Текущий пароль не совпадает с указанным').should('exist')
    });

    it('not submit password change with all fields empty', () => {
        cy.visit('/profile')
        cy.contains('Смена пароля').click()
        cy.get('button[type="submit"]').click()
        cy.contains('Изменения успешно сохранены').should('not.exist')
    });

    it('not submit password change with some empty fields', () => {
        cy.visit('/profile')
        cy.contains('Смена пароля').click()
        cy.get('button[type="submit"]').click()
        cy.contains('Изменения успешно сохранены').should('not.exist')

        cy.visit('/profile')
        cy.contains('Смена пароля').click()
        cy.get('#new_password').clear().type('new-cy')
        cy.get('button[type="submit"]').click()
        cy.contains('Изменения успешно сохранены').should('not.exist')

        cy.visit('/profile')
        cy.contains('Смена пароля').click()
        cy.get('#new_password').clear().type('new-cy')
        cy.get('#repeat_password').clear().type('new-cy')
        cy.get('button[type="submit"]').click()
        cy.contains('Изменения успешно сохранены').should('not.exist')
    });

    it('show alert when repeated password not equal to new', () => {
        cy.visit('/profile')
        cy.contains('Смена пароля').click()
        cy.get('#new_password').clear().type('new-cy')
        cy.get('#repeat_password').clear().type('new-without-cy')
        cy.get('#password').clear().type(currentPassword)
        cy.get('button[type="submit"]').click()
        cy.contains('Новый пароль не совпадает с указанным').should('exist')
    });

    it('show alert when current password is wrong', () => {
        cy.visit('/profile')
        cy.contains('Смена пароля').click()
        cy.get('#new_password').clear().type('new-cy')
        cy.get('#repeat_password').clear().type('new-cy')
        cy.get('#password').clear().type(currentPassword + "idontremember")
        cy.get('button[type="submit"]').click()
        cy.contains('Текущий пароль не совпадает с указанным').should('exist')
    });

    it('change username', () => {
        cy.visit('/profile')
        cy.get(`#username`).clear().type('admin_cy')
        cy.get('#passwordProfile').clear().type(currentPassword)
        cy.get('button[type="submit"]').click()
        cy.contains('Изменения успешно сохранены')

        cy.visit('/profile')
        cy.get(`#username`).should("have.value", "admin_cy")

        cy.get(`#username`).clear().type(currentUsername)
        cy.get('#passwordProfile').clear().type(currentPassword)
        cy.get('button[type="submit"]').click()
        cy.contains('Изменения успешно сохранены')
    });
})

export {}