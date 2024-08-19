# GMail Puller

This is a small application which will pull the email ids from the GMail account and store in a database. Here is the technology stack used for the same.

* GMail API - To pull the email metadata from GMail accounts.
* Mongo DB - To persist the data that is pulled from GMail accounts.
* Python - To automate the process.
* Docker - To dockerize the application.

## Implementation Plan

Here are the details about the implementation plan for application like this.

* Be comfortable with Python.
* Understand concepts behind GMail.
  * Contacts
  * Labels
  * Messages
  * Message Threads
* As we will be using Mongo DB as database, we need to understand the concepts of Mongo DB Database.
  * Collection
  * Documents - JSON and BSON
  * CRUD Operations
* We also need to build docker container to deploy it as a microservice once per day per mail box.

## Setup Project

Let us go ahead and setup the project. We need to have Python3.9 installed locally on our PC or Mac.

* Use Pycharm and create new project called as `gmail-puller`.
* Make sure virtual environment is created with name `gp-venv`. You can use `python3.9 -m venv gp-venv`.
* Install required libraries by running `pip install -r requirements.txt`
* The repository also contain jupyter notebooks to learn key concepts required for this project. Install **jupyter lab** using `pip install jupyterlab`.
* Once jupyter lab is installed, you can run `jupyter lab` command to start jupter lab based notebook server.
* Make sure to create `.credentials` folder under project directory **gmail-puller**.
* 
## GMail API

GMail provides an API to interact with GMail Boxes programmatically.

* We can get started by going to the [official page of GMail API](https://developers.google.com/gmail/api).
* You can see how to get started using Python to pull the data using this [quickstart page](https://developers.google.com/gmail/api/quickstart/python).
* We need to first turn on the Gmail API and download `credentials.json`.
* As we will be using Python as programming language we need to ensure that relevant libraries are downloaded.
* Make sure you are in the right Python Virtual Environment and run the following command to install Google Developer Library.
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# You can also update requirements.txt
```
* We can use the examples from official documentation for following:
  * List Messages
  * Get Message Details
* All the APIs return `dict` and we have to program around to process by understanding how data is represented.
  * Get the messages for a given day.
  * Use message id to get message details.
  * Each message contain the metadata as part of a list called as headers. Each element in the headers is a dict with 2 elements `name` and `value` - **e. g: {'name': 'From', 'value': 'dummy@email.com'}**
  * We have to filter for required header elements.

```
users = service.users()
messages = users.messages().list(userId='me', q=f'after:2020/01/01 before:2020/01/02').execute()
message_list = []

for m in messages['messages']:
    msg = users.messages().get(userId='me', id=m['id']).execute()
    msg_details = {'id': m['id']}
    for headers in msg['payload']['headers']:
        if headers['name'] == 'From' and 'YouTube' in headers['value']:
            for header in msg['payload']['headers']:
                if header['name'] == 'From':
                    msg_details['From'] = header['value']
                elif header['name'] == 'Date':
                    msg_details['Date'] = header['value']
            message_list.append(msg_details)
```

## Mongo DB
Let us understand the concepts of Mongo DB and then the relevant APIs from Mongo DB Library.

* Mongo DB Server can host multiple databases.
* As part of the databases we create collections.
* Collection contain documents which are typically read in the form of JSON Objects.
* We can perform CRUD Operations against Mongo DB Collections.
* We can build MongoDB database quickly using Docker Container.
```
# Creating network so that our application container 
# can use the Mongo DB database running as part of Docker Container
docker network create -d bridge gmail_puller_nw
docker pull mongo
docker run \
  --name gmail_puller_db \
  -p 27017:27017 \
  -d \
  --network gmail_puller_nw \
  mongo
# Make sure to get the container id by running
docker ps
```

## Application Development

Now let us go ahead and connect all the dots.

* Develop the driver program `app.py` which will import the programs that are developed to get the data and store into the database.
* Develop required program `get_mail_ids.py` to fetch the message details such as id, email id and date.
* Develop required program `load_mail_ids.py` to store these messages into MongoDB database.

## Dockerize

Here are the steps to dockerize the container.
* Create Dockerfile for our application
```
FROM python:3.7

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```
* Build the container
* Run the container attaching to the Mongo DB Database.

```
docker build -t gmail_puller .

docker run \
  --name gmail_puller \
  -v `pwd`:/app \
  -e MONGO_HOST=9df71c86f0f6 \
  -e START_DATE=2020/01/01 \
  -e END_DATE=2020/01/02 \
  --network gmail_puller_nw \
  -it gmail_puller \
  bash

docker run \
  --name gmail_puller \
  -v `pwd`:/app \
  -e MONGO_HOST=9df71c86f0f6 \
  -e START_DATE=2020/01/02 \
  -e END_DATE=2020/01/03 \
  --network gmail_puller_nw \
  gmail_puller
```
