describe('Perusable.', () => {
  it('Displays a list of results.', () => {
    cy.intercept('GET', '**/api/v1/catalog/wines/**', { fixture: 'wines.json' }).as('getWines');

    cy.visit('/');
    cy.get('input#country').type('US');
    cy.get('input#points').type('92');
    cy.get('input[placeholder="Enter a search term (e.g. cabernet)"]')
      .type('staglin');
    cy.get('button').contains('Search').click();
    cy.wait('@getWines');

    // Check paginator for first page of results
    cy.get('li:has([data-cy="previous-button"])').should('have.class', 'disabled');
    cy.get('li:has([data-cy="next-button"])').should('have.class', 'disabled');
    cy.get('[data-cy="page-count"]').contains(/^\d+ of \d+ pages$/);

    cy.get('div.card-title').should('contain', 'Cabernet Sauvignon');
  });
});