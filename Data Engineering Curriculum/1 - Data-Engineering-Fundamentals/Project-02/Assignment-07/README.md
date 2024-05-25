# Project 2: Tracking User Activity

- In this project, you work at an ed tech firm. You've created a service that delivers assessments, and now lots of different customers (e.g., Pearson) want to publish their assessments on it. You need to get ready for data scientists who work for these customers to run queries on the data. 

- Through 3 different activites, you will spin up existing containers and prepare the infrastructure to land the data in the form and structure it needs to be to be queried. 
  1) Publish and consume messages with kafka.
  2) Use spark to transform the messages.
  3) Use spark to transform the messages so that you can land them in hdfs.

_______________________________________________________________________________________________________

## Summary

In this project, we're starting the streaming part of the pipeline, by using Kafka to Publish and Consume Messages from a JSON file of 3280 asssessments from students, and running a Spark container to understand the data and select which part of it is important for our analysis

### Repository

- The data is a JSON File with 3280 assessments. These appear to be multiple choice questions. Important aspects of the data: Course Name, Timestamp, Score, etc.
- In the repo, the data is in a new folder called Data
- I've created a set of annonations based on the history logs, called penpen86-annotations.md. Markdown where I explain each step of using Kafka, and how to run a Spark notenook
- The history logs is dumped in a file called penpen86-history.txt
- Also in the repo, is the docker-compose.yml used for spin up the cluster.
- Finally, there is also a Jupyter Notebook with the results from running Spark. From it also presents the frequency table of all the courses taken in our database. I replicate here my analysis of the data:
    At first glance, from the first JSON line, we get that each data point is an assessment of homework in our Application. In terms of what information we want to keep in our analysis, I could think on the following:

    + Name of the exam: This is important for statistics for the Professors on a given subject
    + Sequences: Specially the part where we have total correct, total incorrect, total incomplete, and total questions. These will be useful for grading in the UI and for statisitics on the thoughness of a test
    + Certification: This will help us divide the clients into Certifications vs. Free Users (Free Users usually don't receive a definitive grade or have a different pool of questions)
    + User_Exam_Id: To keep track of each person through their ID, so we can provide them with targeted marketing on next possible courses
    + The different timestamps can help for deploy some kind of reminders, but that could be a less important subject of analysis


### Future work

- Run more analysis on the entire dataset using SparkSQL
- Store the results in a Hadoop Database



