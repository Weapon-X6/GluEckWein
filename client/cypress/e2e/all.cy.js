describe('Perusable.', () => {
  it('Displays a list of results.', () => {
    cy.intercept('GET', '**/api/v1/catalog/wines/**', { fixture: 'wines.json' }).as('getWines');

    cy.visit('/');
    cy.get('input#query').type('staglin');
    cy.get('button').contains('Search').click();
    cy.wait('@getWines');
    cy.get('div.card-title').should('contain', 'Cabernet Sauvignon');
  });
});