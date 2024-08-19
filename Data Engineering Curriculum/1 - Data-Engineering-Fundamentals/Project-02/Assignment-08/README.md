# Project 2: Tracking User Activity

- In this project, you work at an ed tech firm. You've created a service that delivers assessments, and now lots of different customers (e.g., Pearson) want to publish their assessments on it. You need to get ready for data scientists who work for these customers to run queries on the data.

- Through 3 different activites, you will spin up existing containers and prepare the infrastructure to land the data in the form and structure it needs to be to be queried.
  1) Publish and consume messages with kafka.
  2) Use spark to transform the messages.
  3) Use spark to transform the messages so that you can land them in hdfs.

_______________________________________________________________________________________________________

## Summary

This is the final iteration, where we implemented a Streaming Pipeline from Events (JSON file), to distributed storage in HDFS, using Kafka, Spark, and Hadoop via Cloudera.

### Repository

- The data is a JSON File with 3280 assessments. These appear to be multiple choice questions. Important aspects of the data: Course Name, Timestamp, Score, etc.
- In the repo, the data is in a new folder called Data
- I've created a set of annotations based on the history logs, called penpen86-annotations.md. Markdown where I explain each step of using Kafka, and how to run a Spark notebook, and storing the important data in Hadoop
- The history logs is dumped in a file called penpen86-history.txt
- Also in the repo, is the docker-compose.yml used for spin up the cluster.
- Finally, there is also a Jupyter Notebook with the results from running Spark. By using implied Schema, we were able to extract the question pool. However, we needed to enforce some Schema too for extracting the necessary information for grades.
- Data stored in Hadoop:
    * raw_data: The raw form of the data, after extraction from Kafka
    * questions_pool_data: Data from each question answered in each Assessment
    * grades_ID: Grades of each Exam ID, as an individual data point
    * course_ID: Grades aggregated from each Course name, providing Average Score with its Standard Deviation
