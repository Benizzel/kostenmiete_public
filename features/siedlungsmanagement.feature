Feature: Siedlung bewirtschaften
  CRUDL Siedlungen

#Siedlungs spezifische Tests
  Scenario: Create a new Siedlung and verify it appears on the home page
    Given I am on the homepage
    When I create a Siedlung
    And I fill in the Siedlung details
    And I save the Siedlung
    Then I am redirected to the homepage
    And the Siedlung is in the list of all Siedlungen

  Scenario: Update Siedlung - create new Objekt within Siedlung
    Given an existing Siedlung without Objekt
    And I am on the Siedlung details
    When I create a new Objekt
    And I define the Bereich B2
    And I fill in the other Objekt details
    And I save the Objekt
    Then I am redirected to the Siedlung details
    And the Objekt is in the list of all Objekte on the Siedlung-Detail-page
    When I navigate to the homepage
    Then the Objekt is in the list of all Objekte on the home-page

  Scenario: Update Siedlung - Change Stammdaten
      Given existing Siedlung
      When users changes Stammdaten of Siedlung
      And user saves changes
      Then user gets redirected to the Siedlung details page
      And updated Stammdaten are visible

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
      
    
