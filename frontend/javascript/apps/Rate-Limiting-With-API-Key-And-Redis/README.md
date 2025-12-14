 # Rate Lmiting/ Metering Database Access By Creating And Using Your Own API Key

 This project shows you how to rate limit access to your critical resources by API key; create this API key, pass this API key as custom HTTP header for authentication and authorization. 
 This key is also used as Redis key to limit the number of time this resource can be accessed within certain time frame.
 You also learn how to communicate between two different domains and pass critical credentials betweeen them.
 ## Frontend Domain
 uses HTML, CSS, JS and FETCH API requests to another domain (backend damain) to first register with it, get API key, and pass that key for the request to actually access actor data from its database.
 The API key is stored and reterived from SessionStorage (builtin storage/API within all the browsers).
 ## Backend Domain
 PHP, Redis for caching, and a package to interact with Redis Cleint named Predis.

 ## Database
 MySQL 8.0 databse is used for this project. It comes pre-packaged with many databases; the specific database used in this project is named sakila and the specific table that is accessed from there is named actor.
 This project does not depend on this particular database and table; you can use your own database if you like.. all you need to take care of change the relevant database query in the project.
 You also need to create a another table for user registeration with only three fields (id, email and api_key).
 

