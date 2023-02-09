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
            localStorage.setItem("accessToken", response.body.access)
            localStorage.setItem("refreshToken", response.body.refresh)
            localStorage.setItem("currentPassword", currentPassword)
        })
    })

    it('first_name, last_name, email edit and save', () => {
        cy.visit('/profile')
        cy.get(`#first_name`).clear().type('Admin-Cy')
        cy.get(`#last_name`).clear().type('Adminov-Cy')
        cy.get(`#email`).clear().type('admin@cy.com')
        cy.get('button[type="submit"]').click()

        cy.visit('/profile')
        cy.get(`#first_name`).should("have.value", 'Admin-Cy')
        cy.get(`#last_name`).should("have.value", 'Adminov-Cy')
        cy.get(`#email`).should("have.value", 'admin@cy.com')
    });

    it('not submit without username', () => {
        cy.visit('/profile')
        cy.get(`#username`).clear()
        cy.get('button[type="submit"]').click()
        cy.contains('Изменения успешно сохранены').should('not.exist')
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

    it('username edit and save', () => {
        cy.visit('/profile')
        cy.get(`#username`).clear().type('admin_cy')
        cy.get('button[type="submit"]').click()

        cy.visit('/profile')
        cy.get(`#username`).should("have.value", 'admin_cy')

        cy.get(`#username`).clear().type('admin')
        cy.get('button[type="submit"]').click()
    });
})

export {}