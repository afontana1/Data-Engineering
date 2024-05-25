# Query Project
- In the Query Project, you will get practice with SQL while learning about Google Cloud Platform (GCP) and BiqQuery. You'll answer business-driven questions using public datasets housed in GCP. To give you experience with different ways to use those datasets, you will use the web UI (BiqQuery) and the command-line tools, and work with them in jupyter notebooks.
- We will be using the Bay Area Bike Share Trips Data (https://cloud.google.com/bigquery/public-data/bay-bike-share). 

#### Problem Statement
- You're a data scientist at Ford GoBike (https://www.fordgobike.com/), the company running Bay Area Bikeshare. You are trying to increase ridership, and you want to offer deals through the mobile app to do so. What deals do you offer though? Currently, your company has three options: a flat price for a single one-way trip, a day pass that allows unlimited 30-minute rides for 24 hours and an annual membership. 

- Through this project, you will answer these questions: 
  * What are the 5 most popular trips that you would call "commuter trips"?
  * What are your recommendations for offers (justify based on your findings)?


## Assignment 02: Querying Data with BigQuery

### What is Google Cloud?
- Read: https://cloud.google.com/docs/overview/

### Get Going

- Go to https://cloud.google.com/bigquery/
- Click on "Try it Free"
- It asks for credit card, but you get $300 free and it does not autorenew after the $300 credit is used, so go ahead (OR CHANGE THIS IF SOME SORT OF OTHER ACCESS INFO)
- Now you will see the console screen. This is where you can manage everything for GCP
- Go to the menus on the left and scroll down to BigQuery
- Now go to https://cloud.google.com/bigquery/public-data/bay-bike-share 
- Scroll down to "Go to Bay Area Bike Share Trips Dataset" (This will open a BQ working page.)


### Some initial queries
Paste your SQL query and answer the question in a sentence.

- What's the size of this dataset? (i.e., how many trips)
   * SQL Query:
   
   ```{SQL}
   #standardSQL
   SELECT count(*) Number_Events /*Name the Result*/
   FROM `bigquery-public-data.san_francisco.bikeshare_trips`
   ```
   * Answer:
   
  Row  | Number_Events
  --- | -------------
  1  | 983,648


- What is the earliest start time and latest end time for a trip?
   * SQL Query:
   
   ```{SQL}
   #standardSQL
   SELECT x.Earliest_Date, y.Latest_Date
   FROM (SELECT min(start_date) Earliest_Date  FROM `bigquery-public-data.san_francisco.bikeshare_trips`) as x, 
   (SELECT max(end_date) Latest_Date FROM `bigquery-public-data.san_francisco.bikeshare_trips`) as y
   ```
   
   * Answer:
   
  Row  | Earliest_Date | Latest_Date
  --- | -------------------------- | --------------------------
  1  | 2013-08-29 09:08:00 UTC | 2016-08-31 23:48:00 UTC

- How many bikes are there?
   * SQL Query:
   
   ```{SQL}
   #standardSQL
   SELECT count(distinct bike_number) Number_Bikes
   FROM `bigquery-public-data.san_francisco.bikeshare_trips`
   ```
   * Answer:
   
  Row  | Number_Bikes
  --- | -------------
  1  | 700



### Questions of your own
- Make up 3 questions and answer them using the Bay Area Bike Share Trips Data.
- Use the SQL tutorial (https://www.w3schools.com/sql/default.asp) to help you with mechanics.

- Question 1: What's the amount of clients per membership type, percentage wise?
  * Answer:
  
  Row  | Percentage_Subscriber | subscriber_type
  --- | -------------------------- | --------------------------
  1  | 13.91 | Customer
  2 | 86.09 | Subscriber
  
  As we can see, the vast majority of users are using a long term commitment (either by a yearly or monthly subscription) as their main form of using our App. 
  
  * SQL query:
  
   ```{SQL}
   #standardSQL
   SELECT round(count(subscriber_type)/983648*100,2) Percentage_Subscriber, subscriber_type
   FROM `bigquery-public-data.san_francisco.bikeshare_trips`
   GROUP BY subscriber_type
   ```  

- Question 2: What's the average duration in minutes of a trip by membership type?
  * Answer:
  
  Row  | Average_Duration | subscriber_type
  --- | -------------------------- | --------------------------
  1  | 61.98 | Customer
  2 | 9.71 | Subscriber
  
  This is an interesting result. Customers (people with short term commitment) use the bikes in avearge longer that Subscriber by a ratio of 6:1. In terms of our business, this is great news if our prices are adecuate: long term commitment translates into low usage.
  
  
  * SQL query:
  
   ```{SQL}
   #standardSQL
   SELECT round(avg(timestamp_diff(end_date,start_date,minute)),2) Average_Duration, subscriber_type 
   FROM `bigquery-public-data.san_francisco.bikeshare_trips`
   GROUP BY subscriber_type 
   ```  
  

- Question 3: What's the top 5 of stations in average percentage of idle (no use) bikes? 
  * Answer:
  
  Row  | Usage | station_id
  --- | ------------- | -------------
  1  | 58.2 | 50
  2 | 58.07 | 70
  3 | 56.75 | 36
  4 | 55.67 | 54
  5 | 54.77 | 3
  
  With average disuse of around 55%, we need to rethink how many idle bikes do we want in a given location. Maybe we need to redistribute bikes across stations. 
  
  
  * SQL query:
  
   ```{SQL}
   #standardSQL
   SELECT round(avg((bikes_available)*100/(bikes_available+docks_available)),2) Usage, station_id 
   FROM `bigquery-public-data.san_francisco.bikeshare_status`
   WHERE bikes_available+docks_available <> 0 /* To avoid dividing by 0*/
   GROUP BY station_id 
   ORDER BY Usage LIMIT 5
   ```



