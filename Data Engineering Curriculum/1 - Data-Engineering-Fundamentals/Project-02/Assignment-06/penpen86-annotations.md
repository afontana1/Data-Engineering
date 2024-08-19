# Author: Vinicio De Sola (username: penpen86)
# My annotations, Assignment 6.


## First, let's get the data using curl, and the docker-compose.yml
  397  curl -L -o assessment-attempts-20180128-121051-nested.json https://goo.gl/ME6hjp
  404  cp course-content/06-Transforming-Data/docker-compose.yml assignment-06-penpen86/docker-compose.yml

## Next, I make a new folder for the data, called Data
  408  mkdir data
  409  ls
  410  cp assessment-attempts-20180128-121051-nested.json data/assessment-attempts-20180128-121051-nested.json
  411  ls
  412  cd data/

## Next, I spin up my kafka, zookeeper, mids cluster.
  423  docker-compose up -d

## Then, I create a topic for the data, called eduAssessment, and check it out
  426  docker-compose exec kafka kafka-topics --create --topic eduAssessments --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:32181
  427  docker-compose exec kafka kafka-topics --describe --topic eduAssessments --zookeeper zookeeper:32181
  
## Visualize the data, using JQ, first as a pretty print, then as JQ lines
  481  docker-compose exec mids bash -c "cat /w205/assessment-attempts-20180128-121051-nested.json | jq '.'"
  482  docker-compose exec mids bash -c "cat /w205/assessment-attempts-20180128-121051-nested.json | jq '.[]' -c"
  
## Count the number of lines in the file
  483  docker-compose exec mids bash -c "cat /w205/assessment-attempts-20180128-121051-nested.json | jq '.[]' -c | wc -l"
  
## Produce the messages in Kafka, and produce an echo of 3280 messages
  495  docker-compose exec mids bash -c "cat /w205/assessment-attempts-20180128-121051-nested.json | jq '.[]' -c | kafkacat -P -b kafka:29092 -t eduAssessments && echo 'Produced 3280 messages.'"
  
## Make sure that the total of messages are indeed 3280
  496  docker-compose exec mids bash -c "kafkacat -C -b kafka:29092 -t eduAssessments -o beginning -e"
  497  docker-compose exec mids bash -c "kafkacat -C -b kafka:29092 -t eduAssessments -o beginning -e | wc -l"
  
## Turn down the cluster, and save the history logs
  500  docker-compose down
  501  history > penpen86-history.txt

