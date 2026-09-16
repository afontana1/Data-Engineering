# Author: Vinicio De Sola (username: penpen86)
# My annotations, Assignment 7.


## Let's start by doing the same as before, copying the data, and setting up the docker-compose.yml
  531  cp ~/course-content/07-Sourcing-Data/docker-compose.yml docker-compose.yml
  532  git add -A
  533  ls
  534  git status
  535  docker-compose down
  536  docker-compose up -d
  
## Create the topic in Kafka, Publish the messages, and consume them
  537  docker-compose exec kafka kafka-topics --create --topic eduAssessments --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:32181
  538  docker-compose exec kafka kafka-topics --describe --topic eduAssessments --zookeeper zookeeper:32181
  539  docker-compose exec mids bash -c "cat /w205/assessment-attempts-20180128-121051-nested.json | jq '.[]' -c | kafkacat -P -b kafka:29092 -t eduAssessments && echo 'Produced 3280 messages.'"
  540  docker-compose exec mids bash -c "kafkacat -C -b kafka:29092 -t eduAssessments -o beginning -e | wc -l"
  
## Open a Spark Notebook
  541  docker-compose exec spark ls 
  542  docker-compose exec spark env PYSPARK_DRIVER_PYTHON=jupyter PYSPARK_DRIVER_PYTHON_OPTS='notebook --no-browser --port 8888 --ip 0.0.0.0 --allow-root' pyspark
  
## Copy the Notebook from the container to the Host
  547  docker ps
  550  docker cp 137aec3d0601:/spark2.2.0-bin-hadoop2.6/'PySpark - Unrolling Assessments'.ipynb ~/assignment-07-penpen86/PySpark.ipynb
  
## Turn down the cluster, and create the annotations.md
  561  echo "" >> penpen86-annotations.md
  562  git add penpen86-annotations.md 
  563  git status
  564  vi README.md 
  565  vi penpen86-annotations.md 
  566  docker-compose down

