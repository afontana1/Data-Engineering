## Here are the steps that you need to do to use MongoDB using Docker.

Get the MongoDB image

Create a file to initiate authenticated database and user

Create a docker-compose file

Start MongoDB container

Login to MongoDB with created credentials



### Get the MongoDB Image
You will first need to get the latest image of MongoDB on your local machine. You can execute the following command:
```shell
docker pull mongo:latest
```


### Create a file to initiate authenticated database and user

Create a file named init-mongo.js (you can name it whatever you want) with the below content. You can alternatively get the file from the zip attached with this lecture.

```python
db.createUser(
    {
        user:"admin",
        pwd:"password",
        roles: [
            {
                role: "readWrite",
                db:"firstdb"
            }
        ]
    }
)
```

Create a docker-compose file
```yml
version: '3'
 
services:
    mongodb:
        image: 'mongo'
        container_name: 'my-mongo-container'
        # restart: always
        environment:
            MONGO_INITDB_ROOT_USERNAME: admin
            MONGO_INITDB_ROOT_PASSWORD: password
            MONGO_INITDB_DATABASE: firstdb
        volumes:
            - ./init-mongo.js:/docker-entrypoint-initdb.d/init-mongo.js:ro
            - ./mongo-volume:/data/db
        ports:
            - '27017-27019:27017-27019'
```
     

Here's a bit of theory and explanation on what each line in the file means (for those who are curious):
version: is a version of docker-compose file format, you can change to the latest version

database: on line 3 is just a service name, you can change the name whatever you want

image: We are specifying mongo here because you want to create a container from the mongo image

container_name: is the name of your container, this is optional

environment: is a variable that will be used on the mongo container

MONGO_INITDB_ROOT_USERNAME: you fill with the username of the root that you want

MONGO_INITDB_ROOT_PASSWORD: you fill with the password of the root that you want

MONGO_INITDB_DATABASE: you fill with a database name that you want to create, make it the same like init-mongo.js

volumes: to define a file/folder that you want to use for the container

./init-mongo.js:/docker-entrypoint-initdb.d/init-mongo-js:ro means you want to copy init-mongo.js to /docker-entrypoint-initdb.d/ as a read-only file. /docker-entrypoint-initdb.d is a folder that has already been created inside the mongo container used for initiating the database, so we copy our script to that folder

./mongo-volume:/data/db means you want to set data on the container to persist on your local folder named mongo-volume . /data/db/ is a folder that has already been created inside the mongo container.

ports: are to define which ports you want to expose and define, in this case, I use default MongoDB port 27017 until 27019

###  Start MongoDB container
Open terminal --> Navigate to the project directory and run the following command to run the docker-compose file

```shell
docker-compose up

Now open a new terminal and verify if this mongo container is up and running

docker ps
```

### Login to MongoDB with created credentials

Now we have a MongoDB image in the container and to access it we will have to log in to the container. To login to the container, execute the following command:

```shell
docker exec -it <container-name> bash
```

The container name here is the container-name you specified in the docker-compose file (my-mongo-container in my case)


### Now, finally, you can log in to MongoDB using the following commands:

```shell
mongo -u <your username> -p <your password> --authenticationDatabase <your database name>

OR

mongo -u <your username> --authenticationDatabase <your database name>
```

Here is your database connection URL : mongodb://YourUsername:YourPasswordHere@127.0.0.1:27017/your-database-name