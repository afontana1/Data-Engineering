# Author: Vinicio De Sola (username: penpen86)
# My annotations, Assignment 8.


## Let's start by doing the same as before, copying the data, and setting up the docker-compose.yml
  696  cd assignment-08-penpen86/
  697  ls
  698  git status
  699  vi docker-compose.yml
  700  docker ps
  701  docker-compose down
  702  docker-compose up -d
  
## Create the topic in Kafka, Publish the messages, and consume them
  703  docker-compose exec kafka kafka-topics --create --topic eduAssessments --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:32181
  704  docker-compose exec kafka kafka-topics --describe --topic eduAssessments --zookeeper zookeeper:32181
  705  docker-compose exec mids bash -c "kafkacat -C -b kafka:29092 -t eduAssessments -o beginning -e | wc -l"
  706  docker-compose exec mids bash -c "cat /w205/assessment-attempts-20180128-121051-nested.json | jq '.[]' -c | kafkacat -P -b kafka:29092 -t eduAssessments && echo 'Produced 3280 messages.'"
  707  docker-compose exec mids bash -c "kafkacat -C -b kafka:29092 -t eduAssessments -o beginning -e | wc -l"
  
## Open a Spark Notebook
  709  docker-compose exec spark env PYSPARK_DRIVER_PYTHON=jupyter PYSPARK_DRIVER_PYTHON_OPTS='notebook --no-browser --port 8888 --ip 0.0.0.0 --allow-root' pyspark
  
## Copy the Notebook from the container to the Host
  710  docker ps
  711  docker cp 06d37d0af7aa:/spark-2.2.0-bin-hadoop2.6/PySpark.ipynb ~/assignment-08-penpen86/PySpark.ipynb
  
## Check HDFS to see if all files are there, before turning down the cluster
  712  docker-compose exec cloudera hadoop fs -ls /tmp/
  713  docker-compose exec cloudera hadoop fs -ls /tmp/course_ID1
  714  docker-compose down
