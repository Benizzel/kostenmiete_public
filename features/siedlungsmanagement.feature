Feature: Siedlung bewirtschaften
  CRUDL Siedlungen

  Scenario: Create a new Siedlung and verify it appears on the home page
    Given I am on the homepage
    When I click the "Create Siedlung" button
    And I am on the Siedlung creation page
    And I fill in the Siedlung details
    And I click the "Save" button
    Then I should be redirected to the Siedlung home page
    And I should see the newly created Siedlung listed

