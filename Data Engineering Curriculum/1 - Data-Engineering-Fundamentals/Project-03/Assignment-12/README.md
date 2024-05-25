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

- docker-compose.yml, to spun up the connection between the mids image, flask, Kafka, Spark, Cloudera, and Presto
- game_api.py. Source code with connections with Kafka for ingesting events from the user of mobile app. The logic behind the source code is the following:
    * Join a Guild: We have a GET to avoid a 405 error if hit from Web. Most important aspect, the POST. We will expect JSON from the server: a dictionary with Level *"level"* and Color *"color"* of the Guild. We could also add names or ID later. We will connect the color of the Guild with the color of the Sword on Inventory.
    * Purchase a Sword: Same as before, but the attributes of Sword are: Price *"price"*, Color *"color"*, and Hit Points *"hit-points"*. Price will help us relate inventory with wallet, and Hit Points will be related with Guild and color (boosts in power) and internal logic of the game
    * Get Coins: Similar as before, only one attribute: Coins *"coins"*.
    
  We create also a new column from our JSON called attributes.
  
- write_stream.py. PySpark job to batch the contents of Kafka: We extract the events, we transformed by keeping the raw Json and add the timestamp, while separting the internal methods. For writing into HDFS, we keep the extracted events as a whole, but also create separate parquet files for *Default*, *Sword Purchases*, *Join Guild*, and *Coins*. Everything is done in stream.
- purchase_sword.json, join_guild.json, coins.json: Files needed for POST using Apache Bench
- penpen86-history.txt. History of all commands used for version control and for future debugging
- README.md. All the documentation of the project

## Summary

1. For Kafka, I decide to name the topic userItems, because we envisioned the possibility of several topics: Inventory, User, Missions.
2. Running Flask via curl, we are mocking the interaction of a user with the web application. We implemented a GET method and a POST method using curl. Example of a POST Event
```
curl -H "Content-Type:application/json" -X POST http://localhost:5000/join_a_guild -d '{"level":"30", "color":"White"}'
```
3. For Apache Bench, we used the followind comands to generate stream of data for all events:
```
while true; do docker-compose exec mids ab -p purchase_sword.json -n 10 -T application/json -H "Host: user1.comcast.com" http://localhost:5000/purchase_sword; sleep 10; done

while true; do docker-compose exec mids ab -p join_guild.json -n 10 -T application/json -H "Host: user1.comcast.com" http://localhost:5000/join_a_guild; sleep 10; done

while true; do docker-compose exec mids ab -p coins.json -n 10 -T application/json -H "Host: user1.comcast.com" http://localhost:5000/get_coins; sleep 10; done
```

4. In PySpark, we created the schema for all stream tables, each one is a different sink. 

5. Finally, we used hive to create each of the tables that we queried:
```
create external table if not exists default.sword (Accept string, Host string, User_Agent string, attributes array<struct<price:string,color:string,hit_points:string>>, event_type string, remote_addr string, timestamp string, raw_event string) stored as parquet location '/tmp/sword_purchases'  tblproperties ("parquet.compress"="SNAPPY");

create external table if not exists default.guild (Accept string, Host string, User_Agent string, attributes array<struct<level:string,color:string>>, event_type string, remote_addr string, timestamp string, raw_event string) stored as parquet location '/tmp/join_guild'  tblproperties ("parquet.compress"="SNAPPY");

create external table if not exists default.coins (Accept string, Host string, User_Agent string, attributes array<struct<coins:string>>, event_type string, remote_addr string, timestamp string, raw_event string) stored as parquet location '/tmp/get_coins'  tblproperties ("parquet.compress"="SNAPPY");
```
We ran simple queries in Presto to check that the stream of data was being saved:
```
docker-compose exec presto presto --server presto:8080 --catalog hive --schema default

select count(*) from sword;
select count(*) from guild;
select count(*) from coins;
```

## Future Work

1. Use redis for cache in the business logic of the API, so we can save states.
2. Mock connection with a form of cryptocurrency so we can model payment. Some of these coins allows for mock API connections for testing payment methods