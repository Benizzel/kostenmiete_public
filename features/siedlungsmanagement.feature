Feature: Siedlung bewirtschaften
  CRUDL Siedlungen

  Scenario: Create a new Siedlung and verify it appears on the home page
    Given I am on the homepage
    When I click the "Create Siedlung" button
    And I fill in the Siedlung details on the Siedlung creation page
    And I click the "Save" button
    Then I am redirected to the homepage
    And I see the newly created Siedlung in the list of all Siedlungen

