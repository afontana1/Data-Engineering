# Project 3: Instrument API for a mobile game
## Members: Vinicio De Sola, Jeremy Fraenkel, Daniel Alvarez

- You're a data scientist at a game development company.  
- Your latest mobile game has two events you're interested in tracking: 
- `buy a sword` & `join guild`...
- Each has metadata

## Project 3 Task
- Your task: instrument your API server to catch and analyze event types.
- This task will be spread out over the last four assignments (9-12).

## Project 3 Task Options 

- All: Game shopping cart data used for homework 
- Advanced option 1: Generate and filter more types of items.
- Advanced option 2: Enhance the API to accept parameters for purchases (sword/item type) and filter
- Advanced option 3: Shopping cart data & track state (e.g., user's inventory) and filter


---

# Team The Legend of MIDS


## Repo

In this repo we are presenting the following:

- docker-compose.yml, to spun up the connection between the mids image, flask, Kafka, and Spark
- game_api.py. Source code with connections with Kafka for ingesting events from the user of mobile app. The logic behind the source code is the following:
    * Join a Guild: We have a GET to avoid a 405 error if hit from Web. Most important aspect, the POST. We will expect JSON from the server: a dictionary with Level *"level"* and Color *"color"* of the Guild. We could also add names or ID later. We will connect the color of the Guild with the color of the Sword on Inventory.
    * Purchase a Sword: Same as before, but the attributes of Sword are: Price *"price"*, Color *"color"*, and Hit Points *"hit-points"*. Price will help us relate inventory with wallet, and Hit Points will be related with Guild and color (boosts in power) and internal logic of the game
    * Get Coins: Similar as before, only one attribute: Coins *"coins"*.
- PySpark_Job.ipynb. Jupyter Notebook with the exploratory part of Spark for streaming the events and visualization of the differences between POST and GET. 
- penpen86-history.txt. History of all commands used for version control and for future debugging
- README.md. All the documentation of the project

## Summary

1. For Kafka, I decide to name the topic userItems, because we envisioned the possibility of several topics: Inventory, User, Missions.
2. Running Flask via curl, we are mocking the interaction of a user with the web application. We implemented a GET method and a POST method using curl. Example of a POST Event
```
curl -H "Content-Type:application/json" -X POST http://localhost:5000/join_a_guild -d '{"level":"30", "color":"White"}'
```
3. In PySpark, we cache the data before printing the Schema to make sure we're free of errors. Good practice.

## Future Work

1. Build more of the business logic, and relationships between Guilds, Wallet, Inventory
2. Add states to the topics using Redis: Inventory, wallet, maybe user level.
3. If time permits, mock connection with a form of cryptocurrency so we can model payment. Some of these coins allows for mock API connections for testing payment methods

