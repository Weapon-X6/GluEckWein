describe('Persuable', () => {
  it('Displays the home page.', () => {
    cy.intercept('GET', '**/api/v1/catalog/wines/**', { fixture: 'wines.json' }).as('getWines');

    cy.visit('/');
    cy.get('input#query').type('cabernet');
    cy.get('button').contains('Search').click();
    cy.get('div.card-title').should('contain', 'Cabernet Sauvignon');
  });
});