Feature: User Authentication

  Scenario: User logs in with valid credentials
    Given the user exists with username "ameenalam" and password "ameenalamsecret"
    When the user logs in with username "ameenalam" and password "ameenalamsecret"
    Then the user should receive a token
