# Project 3: Instrument API for a mobile game
## Members: Vinicio De Sola, Jeremy Fraenkel, Daniel Alvarez

- You're a data scientist at a game development company.  
- Your latest mobile game has two events you're interested in tracking: 
- `buy a sword` & `join guild`...
- Each has metadata

## Project 3 Task
- Your task: instrument your API server to catch and analyze these two
event types.
- This task will be spread out over the last four assignments (9-12).

---

# Team The Legend of MIDS


## Repo

In this repo we are presenting the following:

- docker-compose.yml, to spun up the connection between the mids image, flask, and Kafka
- basic_game_api.py. Barebones source code with the methods used for testing the web connections on Flask
- game_api.py. More advance source code with connections with Kafka for ingesting events from the user of mobile app.
- penpen86-history.txt. History of all commands used for version control and for future debugging
- README.md. All the documentation of the project

## Summary

1. Our first step was to develop the source API. We decided to add one more method: Get Coins. Main goal will be to relate the coins gained in missions to the price of the swords or other items that we decide to add to our game. This will be a state driven approach. 
2.- For Kafka, I decide to name the topic userItems, because we envisioned the possibility of several topics: Inventory, User, Missions.
3.- Running Flask via curl, we are mocking the interaction of a user with the web application. We implemented a get method with a request, where we can customize the amount of coins receive or the color of the sword, using the query string. This process can be expanded for addind type of item (common, rare, epic, legendary).
    - Example of events stored in Kakca (docker-compose exec mids bash -c "kafkacat -C -b kafka:29092 -t userItems -o beginning -e"):
    ```
    092 -t userItems -o beginning -e"
    get_coins100
    default
    join_guild
    purchase_a_swordwhite
    purchase_a_swordgrey
    purchase_a_swordblack
    get_coins300
    % Reached end of topic userItems [0] at offset 7: exiting
    ```

## Future Work

1. Add POST and PUT methods in the Flask Application, build more of the business logic.
2. Add states to the topics using Redis: Inventory, wallet, maybe user level.
3. If time permits, mock connection with a form of cryptocurrency so we can model payment. Some of these coins allows for mock API connections for testing payment methods
    



