// https://docs.cypress.io/api/introduction/api.html

describe("Homepage test", () => {
  it("Visits the app root url", () => {
    cy.visit("/");
    cy.contains("h1", " Welcome to Vuetify 3 Beta ");
  });
});
