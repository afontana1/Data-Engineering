2;2Rmplate-activity-03


# Query Project

- In the Query Project, you will get practice with SQL while learning about
  Google Cloud Platform (GCP) and BiqQuery. You'll answer business-driven
  questions using public datasets housed in GCP. To give you experience with
  different ways to use those datasets, you will use the web UI (BiqQuery) and
  the command-line tools, and work with them in jupyter notebooks.

- We will be using the Bay Area Bike Share Trips Data
  (https://cloud.google.com/bigquery/public-data/bay-bike-share). 

#### Problem Statement
- You're a data scientist at Ford GoBike (https://www.fordgobike.com/), the
  company running Bay Area Bikeshare. You are trying to increase ridership, and
  you want to offer deals through the mobile app to do so. What deals do you
  offer though? Currently, your company has three options: a flat price for a
  single one-way trip, a day pass that allows unlimited 30-minute rides for 24
  hours and an annual membership. 

- Through this project, you will answer these questions: 
  * What are the 5 most popular trips that you would call "commuter trips"?
  * What are your recommendations for offers (justify based on your findings)?


## Assignment 03 - Querying data from the BigQuery CLI - set up 

### What is Google Cloud SDK?
- Read: https://cloud.google.com/sdk/docs/overview

- If you want to go further, https://cloud.google.com/sdk/docs/concepts has
  lots of good stuff.

### Get Going

- Install Google Cloud SDK: https://cloud.google.com/sdk/docs/

- Try BQ from the command line:

  * General query structure

    ```
    bq query --use_legacy_sql=false '
        SELECT count(*)
        FROM
           `bigquery-public-data.san_francisco.bikeshare_trips`'
    ```

### Queries

1. Rerun last week's queries using bq command line tool (Paste your bq
   queries):

- What's the size of this dataset? (i.e., how many trips)

```
bq query --use_legacy_sql=false 'SELECT count(*) FROM `bigquery-public-data.san_francisco.bikeshare_status`'
```

 * Answer: For the status database

 Row | Answer
 ---|------------
 1 | 107,501,619


- What is the earliest start time and latest end time for a trip?:
```
 bq query --use_legacy_sql=false 'SELECT x.Earliest_Date, y.Latest_Date FROM (SELECT min(start_date) Earliest_Date  FROM `bigquery-public-data.san_francisco.bikeshare_trips`) as x, (SELECT max(end_date) Latest_Date FROM `bigquery-public-data.san_francisco.bikeshare_trips`) as y'
```

 * Answer: We're now using the Trips database

 Row  | Earliest_Date | Latest_Date
 --- | -------------------------- | --------------------------
 1  | 2013-08-29 09:08:00 UTC | 2016-08-31 23:48:00 UTC


- How many bikes are there?
```
bq query --use_legacy_sql=false 'SELECT count(distinct bike_number) Number_Bikes FROM `bigquery-public-data.san_francisco.bikeshare_trips`'
```

 * Answer: Again, using the Trips database

 Row  | Number_Bikes
 --- | -------------
 1  | 700


2. New Query (Paste your SQL query and answer the question in a sentence):

- How many trips are in the morning vs in the afternoon?
```
bq query --use_legacy_sql=false 'SELECT x.Morning, y.Afternoon FROM
(SELECT COUNT(*) Morning FROM `bigquery-public-data.san_francisco.bikeshare_trips` WHERE EXTRACT(HOUR FROM end_date) BETWEEN '06' and '12') as x,
(SELECT COUNT(*) Afternoon FROM `bigquery-public-data.san_francisco.bikeshare_trips` WHERE EXTRACT(HOUR FROM end_date) BETWEEN '16' and '22') as y'
```


 * Answer:

 Row  | Morning | Afternoon
 --- | ---------- | ----------
 1  | 432,595 | 407,211

### Project Questions
Identify the main questions you'll need to answer to make recommendations (list
below, add as many questions as you need).

- Question 1: What is the composition of clients?

- Question 2: What's the average trip time by customer type?

- Question 3: What are the 5 most popular areas by customer type?

- Question 4: What's the top 5 of stations in average percentage of idle (no use) bikes?

- Question 5: What's the top 5 of stations in average percentage of usage?

- Question 6: What's the average duration in minutes of a trip by membership type?

- Question 7: What's a commuter trip?

- Question 8: What's the average time of a commuter trip? by costumer type

- Question 9: How many commuter trips per costumer type are there?

### Answers

Answer at least 4 of the questions you identified above You can use either
BigQuery or the bq command line tool.  Paste your questions, queries and
answers below.

- Question 1: What is the composition of clients?
  * Answer:

 Row  | Percentage_Subscriber | subscriber_type
 --- | -------------------------- | --------------------------
 1  | 13.91 | Customer
 2 | 86.09 | Subscriber

As we can see, the vast majority of users are using a long term commitment (either by a yearly or monthly subscription) as their main form of using our App. For the next project, I'll plot the evolution of these percentage over time.

  * SQL query:
```
bq query --use_legacy_sql=false 'SELECT round(count(subscriber_type)/983648*100,2) Percentage_Subscriber, subscriber_type FROM `bigquery-public-data.san_francisco.bikeshare_trips` GROUP BY subscriber_type'
```

- Question 2: What's the average trip time by customer type?
  * Answer:

 Row  | Average_Duration | subscriber_type
 --- | -------------------------- | --------------------------
 1  | 61.98 | Customer
 2 | 9.71 | Subscribe

This is an interesting result. Customers (people with short term commitment) use the bikes in avearge longer that Subscriber by a ratio of 6:1. In terms of our business, this is great news if our prices are adecuate: long term commitment translates into low usage.

  * SQL query:
```
bq query --use_legacy_sql=false 'SELECT round(avg(timestamp_diff(end_date,start_date,minute)),2) Average_Duration, subscriber_type FROM `bigquery-public-data.san_francisco.bikeshare_trips` GROUP BY subscriber_type'
```
 
- Question 3: What are the 5 most popular areas by customer type?
  * Answer:

For Customers (people with short term commitment)

 Row | start_station_name | Number_trips
 --- | ---------------------------- | --------
 1 | Embarcadero at Sansome |  13,934
 2 | Harry Bridges Plaza (Ferry Building) | 12,441
 3 | Market at 4th | 5,952
 4 | Powell Street BART | 5,214
 5 | Embarcadero at Vallejo | 4,945

For Subscriber (people with long term commitment)

 Row | start_station_name | Number_trips
 --- | ---------------------------- | --------
 1 | San Francisco Caltrain (Townsend at 4th) |  68,384
 2 | San Francisco Caltrain 2 (330 Townsend) | 53,694
 3 | Temporary Transbay Terminal (Howard at Beale) | 37,888
 4 | Harry Bridges Plaza (Ferry Building) | 36,621
 5 | 2nd at Townsend | 35,500

The distribution is quite different. Customers use the service in Tourist regions, like Embarcadero; while Subscriber use it for commute - near Public Transportation.

  * SQL query: 
```
bq query --use_legacy_sql=false 'SELECT start_station_name, count(trip_id) as Number_trips FROM `bigquery-public-data.san_francisco.bikeshare_trips` where subscriber_type = 'Subscriber' group by start_station_name order by Number_trips desc limit 5'
```

- Question 4: What's the top 5 of stations in average percentage of idle (no use) bikes?
  * Answer:

  Row  | Usage | name
  --- | ------------- | -------------
  1  | 58.2 | Harry Bridges Plaza (Ferry Building)
  2 | 58.07 | San Francisco Caltrain (Townsend at 4th)
  3 | 56.75 | California Ave Caltrain Station
  4 | 55.67 | Embarcadero at Bryant
  5 | 54.77 | San Jose Civic Center

We can see that for the San Francisco Caltrain, it makes sense to have a lot of bikes available, because is the most used Location. However, there are many stations with high idle time that we can rearrange for better churn.

  * SQL query:
```
bq query --use_legacy_sql=false 'SELECT round(avg((Status.bikes_available)*100/(Status.bikes_available+Status.docks_available)),2) Usage, Stations.name FROM `bigquery-public-data.san_francisco.bikeshare_status` as Status join `bigquery-public-data.san_francisco.bikeshare_stations` as Stations on Status.station_id=Stations.station_id WHERE Status.bikes_available+Status.docks_available <> 0 GROUP BY Stations.name ORDER BY Usage desc LIMIT 5 
```
