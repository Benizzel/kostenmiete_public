Feature: Siedlung bewirtschaften
  CRUDL Siedlungen

  Scenario: Create a new Siedlung and verify it appears on the home page
    Given I am on the homepage
    When I click the "Create Siedlung" button
    And I fill in the Siedlung details on the Siedlung creation page
    And I click the "Save" button
    Then I am redirected to the homepage
    And I see the newly created Siedlung in the list of all Siedlungen

  # Systemtest
  # to be enhanced with various object types, Siedlungs Stammdaten etc.
  # Variants might be tested on lower test level
  Scenario: Create new Objekt within Siedlung
    Given existing, empty Siedlung
    When creates new Objekt B2 within selected Siedlung
    And saves new Objekt 
    Then user gets redirected to the Siedlung details page
    And the newly created Objekt is visible in the list of all Objekte within the Siedlung
    And the newly created Objekt is visible in the list of all Objekte on the homepage

  # Systemtest
  # could potentially be tested without UI when relocating the last two steps into a separate UI verification
  Scenario: Delete Siedlung
    Given existing Siedlung with 1-n Objekte
    When users deletes Siedlung
    Then Siedlung is deleted
    And all Objekte within Siedlung are deleted
    And Siedlung is not visible anymore on homepage
    And Objekte are not visible anymore on homepage

  Scenario: Update Siedlung Stammdaten
    Given existing Siedlung
    When users changes Stammdaten of Siedlung
    And saves changes
    Then user gets redirected to the Siedlung details page
    And updated Stammdaten are visible

    
