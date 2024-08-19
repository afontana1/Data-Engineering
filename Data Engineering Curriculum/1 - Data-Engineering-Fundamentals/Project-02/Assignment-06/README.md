# Project 2: Tracking User Activity

- In this project, you work at an ed tech firm. You've created a service that delivers assessments, and now lots of different customers (e.g., Pearson) want to publish their assessments on it. You need to get ready for data scientists who work for these customers to run queries on the data. 

- Through 3 different activites, you will spin up existing containers and prepare the infrastructure to land the data in the form and structure it needs to be to be queried. 
  1) Publish and consume messages with kafka.
  2) Use spark to transform the messages.
  3) Use spark to transform the messages so that you can land them in hdfs.

_______________________________________________________________________________________________________

## Summary

In this project, we're starting the streaming part of the pipeline, by using Kafka to Publish and Consume Messages from a JSON file of 3280 asssessments from students.

### Summary

- The data is a JSON File with 3280 assessments. These appear to be multiple choice questions. Important aspects of the data: Course Name, Timestamp, Score, etc.
- In the repo, the data is in a new folder called Data
- I've created a set of annonations based on the history logs, called penpen86-annotations.md. Markdown where I explain each step of using Kafka
- The history logs is dumped in a file called penpen86-history.txt
- Also in the repo, is the docker-compose.yml used for spin up the cluster.
- The topic in Kafka was named eduAssessment. 

### Future work

- Use PySpark for processing the data.
- Use Python for visualization of scores, most taken course, etc.

