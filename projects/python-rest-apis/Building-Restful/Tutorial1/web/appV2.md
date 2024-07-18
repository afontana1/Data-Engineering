## Implementation APP

First we need to download image file for MongoDB. For that we go to DockerHub to get the image of MongoDB.

- search for mongodb in https://hub.docker.com

Second open the terminal and inside of _db_ folder run the command: 

    touch Dockerfile

Using atom to edit the Dockerfile we need to specifiy the mongodb image. For that type:
  
    FROM mongo:3.6.12

Now we need to define our _db_ service in _docker-compose.yml_ file as we did before for _web_ service

        db:
          build: ./db
          
But remember our _web_ service will depends of _db_ service because the _web_ wil use _db_ to store information. So, we need to add a link that coonect _web_ service to _db_ service. At the end your _docker-compose.yml_ file need to be equal to:

      version: '3'
      services:
        web:
          build: ./web
          ports:
            - "5000:5000"
          links:
            - db
        db:
          build: ./db

Since _web_ service depends of _db_ service the _db_ service is build in first and after that _web_ service is built.

Now we need to build a communication among _web_ and _db_ in our app.py. For that we need a library named as _pymongo_. So this library needs to be installed. And for that in file _requirements.txt_ add:

      pymongo
      
Now we need to build the project because you did several modifications. In terminal run:

      sudo docker-compose build

After build the project and check you don't have kind of errors duw to the last modifications you need to proceed with _app.py_ file in according to connect the application which is under development with the monogDB.

    from flask import Flask, jsonify, request
    from flask_restful import Api, Resource
    import os

    from pymongo import MongoClient

    app = Flask(__name__)
    api = Api(app)

    #->> initialize a new client: 
    # db is the name of the folder that have the Dockerfile of mongoDB
    # default port used by mongoDB: 27017
    client = MongoClient("mongodb://db:27017")
    db = client.aNewDB                          # create a new DB named as aNewDB
    UserNum = db["UserNum"]                     # create a collection

    UserNum.insert({                            # inside of the collection we insert documments
        'num_of_users':0
    })

    # Track the visits of our website
    class Visit(Resource):
        def get(self):                                               # here we are using GET and not POST
            prev_num = UserNum.find({})[0]['num_of_users']           # to get the previous number of users
            new_num = prev_num + 1
            UserNum.update({}, {"$set":{"num_of_users":new_num}})    # update the number of users
            return str("Hello user " + str(new_num))


Inside of our APIs section we write, to define the root of our application:

    api.add_resource(Visit, "/hello")
    
Now inside of your project folder where you have the folders _web_ and _db_ as well the _Dockerfile_ and _requirements.txt_ files, you need re _build_ and _up_ the project:

    sudo docker-compose build
    sudo docker-compose up

For you see the functionality of your app you need to poen your webrowser and after each refresh you will see the number of users increasing:

    localhost:5000/hello
