describe('Perusable.', () => {
  it('Displays the home page.', () => {
    cy.visit('/');
    cy.get('h1').should('contain', 'GlückWein');
  });

  it('Displays a list of results.', () => {
    cy.intercept('GET', '**/api/v1/catalog/pg-wines/**', { fixture: 'wines.json' }).as('getWines');

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

  it('Displays wine search words.', () => {
    // Stub server
    cy.intercept(
      'GET', '**/api/v1/catalog/wine-search-words/**',
      { fixture: 'wine_search_words.json' }
    ).as('getWineSearchWords');

    cy.visit('/');
    cy.get('input[placeholder="Enter a search term (e.g. cabernet)"]')
      .type('cabernet')
    cy.wait('@getWineSearchWords');
    cy.get('div#query').should('contain', 'cabernet')
  });
});