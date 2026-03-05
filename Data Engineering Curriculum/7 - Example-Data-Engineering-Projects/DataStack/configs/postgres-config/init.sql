
CREATE SCHEMA aggregations;

CREATE TABLE aggregations.tolls_avg_distance (
    id serial PRIMARY KEY,
    DOLocationID integer,
    avg_distance DECIMAL(15,4)
);