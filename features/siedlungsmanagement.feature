Feature: Siedlung bewirtschaften
  CRUDL Siedlungen

#Siedlungs spezifische Tests
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
  Scenario: Update Siedlung - create new Objekt within Siedlung
    Given existing, empty Siedlung
    When creates new Objekt B2 within selected Siedlung
    And saves new Objekt 
    Then user gets redirected to the Siedlung details page
    And the newly created Objekt is visible in the list of all Objekte within the Siedlung
    And the newly created Objekt is visible in the list of all Objekte on the homepage

  # Test variaton on DB (Model) Level with Unit Test because there is the validation
  # Django serves the DB Validation with a proper UI Message
  # Specific UI Unit Test for own Validators
  Scenario: Update Siedlung - Change Stammdaten
      Given existing Siedlung
      When users changes Stammdaten of Siedlung
      And user saves changes
      Then user gets redirected to the Siedlung details page
      And updated Stammdaten are visible

  # Systemtest
  # Check after deletion if Siedlung-Detail can be loaded with siedlung_pk -> Expected: 404
  # Check the same way if Objekt with siedlung_fk is available -> Expected: 404
  # "Browser Caching" - Check with Cypress if list-count of all Siedlungen == Siedlung Cards on UI
  # could potentially be tested without UI when relocating the last two steps into a separate UI verification
  Scenario: Delete Siedlung
    Given existing Siedlung with 1-n Objekte
    When users deletes Siedlung
    And warning message on UI is confirmed by user
    Then Siedlung is deleted
    And all Objekte within Siedlung are deleted
  # Implement this with Cypress
    And Siedlung is not visible anymore on homepage
    And Objekte are not visible anymore on homepage

# Objekt spezifische Tests
  # Implementation "-1": http request "DEL" with random Objekt_pk (der nicht in der DB sein kann...) -> Expected: "Objekt not available" 
  Scenario Outline: Delete Objekt within Siedlung
    Given exisiting Siedlung with <number_of_objekte> Objekte
    When <number_of_objekte_to_be_deleted> Objekt get deleted
    Then deletion is <valid>
    And Siedlung continues to exist

    Examples: 
      | number_of_objekte | number_of_objekte_to_be_deleted | valid        |
      | 5                 | 1                               | accepted     |
      | 5                 | 5                               | accepted     |
      | 5                 | -1                              | not accepted |

  # negative case
  Scenario: Create Objekt without Siedlung
    Given Objekte database exists 
    When new Objekt gets created in database
    And no Siedlung is linked to newly created Objekt
    Then Objekt is not saved in database

  #examples to be reviewed and enhanced
  Scenario Outline: Update Objekt
    Given existing Objekt with Stammdaten <current_bereich>, <current_punkte>, <current_miete>
    And Objekt is linked to <current_siedlung>
    When Objekt Stammdaten get changed with <new_bereich> OR <new_punkte> OR <new_miete> OR <new_siedlung>
    Then changes are <changes saved>
    And saved changes are visible 

    Examples:
      | current_bereich | current_punkte | current_miete | current_siedlung | new_bereich | new_punkte | new_miete | new_siedlung | changes saved | explanation                                                                     |
      | B2              |  8.0           | 2000          |  siedlung 1      | B3          |            |           |              | saved         |                                                                                 |
      | B3              |  10.0          | 3500          |  siedlung 1      |             |            | 4000      |              | saved         |                                                                                 |
      | GZ              |  6.0           | 0             |  siedlung 1      |             |            | 500       |              | not saved     | GZ Objekte dürfen keinen aktuellen Mietzins haben. Nur berechnete Kostenmiete!  |
      | B2              |  8.0           | 2000          |  siedlung 1      |             |            |           | siedlung 2   | saved         |                                                                                 |
      
    
