## File Information 

- appV1: build an application to do the four elementary opperations: add, subtraction, division, multiply 

    -how we can send error messages to guide the user

    - how we can pass a value to the API

- appV2: it shows how connect the app to mongoDb server 

    - Readme to [Mongo Basics](https://github.com/njsdias/APIForDS/blob/master/Tutorial1/web/mongobasics.md)

    - readme to [Modification to connect mongoDb with the application](https://github.com/njsdias/APIForDS/blob/master/Tutorial1/web/appV2.md)

- appV3

**Note:** 
Modify the below line in Dockerfile with the name of app that you are using

       CMD ["python", "appV1.py"]

## Dockers

Once that you copy your aapp.py the Docker expects to see a Dockerfile

- To create a DockerFile. In terminal write : 

        touch Dockerfile

After that we nee to tell to Docker which applications that is necessary to run the Application app.py. For that we need create a file that contains the default libraries necessary by app.py.

        touch requirements.txt


## Dockerfile
The Dockerfile have the instructions to build a machine from scratch.

Open the Dockerfile and fill with the next lines (without the comments after ->)

- FROM python:3 -> This pull pyhton 3 from https://hub.docker.com/_/pyhton/ that is like a a repository for dockers
                   The truth is that pulls the Ubuntu too to run the python3 in the container.

- WORKDIR /usr/src/app -> Defining the work directory (this path is just a convention)

- COPY requirements.txt . -> To copy to the current work directory the file that contains the specifications to install in the machine. Attention to the dot(.) at the end of the command line.

- RUN pip install --no-cache-dir -r requirements.txt -> Once tyou have the requirements.txt on the container you need install the specification that are inside of this file.

- COPY . . -> Copy all files of the current directory (local) first dot(.) to the machine, the second dot(.) means into the machine (container)

- CMD ["python", "app.py"] -> to run in the machine the app.py using python
                   
## requirements.txt
This file ontains the programs or libraries taht you need to run your application. For our case fill the file as

- flask
- flask_restful

That tells to pip to install this two libraries.

## Docker- Compose
Now we need to do something to automatically start this application. First we to jump to the main directory (Tutorial1) and create the docker-compose that contains all containers (imagine you have many containers: web,db,npl, etc.). The docker-compose controls this containers

- to create the yml file -> touch docker-compose.yml

The version:'3' specify the version of the docker-compose. The next lines says that: the web is a service and for build it use the folder ./web where is located the DockerFile

        version: '3'
        
        services:
          web:
            build: ./web
            ports:
              - "5000:5000"
         
## Run the Docker
In the main folder (Tutorial1):

- sudo docker-compose build -> It builds the entire system. 

- sudo docker-compose up -> To put the envinronment in the production in web

In the postman we can run the application selecting the POST and, for instance, localhost:5000/division to test if is all right.

Imagine we modify your file app.py. To test the changes you only need run:

- sudo docker-compose up

The command build is necessary run if you change anything on the docker files.


