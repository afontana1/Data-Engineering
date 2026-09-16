## Information of the Files

- add.py: it is the basics of the api with the JSON file that is used to send information between server/servers

- add2.py: it contains a basic API that do the four elementary math operations: add, subtraction, multiply and divided. In this file the important we two important things:
    - how we can send error messages to guide the user
    - how we can pass a value to the API

## Structure of folders
        docker-compose.yml
        |-web
            app.py
            Dockerfile
            requirements.txt
        |-db
            Dockerfile
            


##  Notes

When we access to a normal page 

- The Browser sends the request to the google.com and the google.com sends a response back whcih is the index.html that is the google structure.

- Browsers only communicate using only text. all communication between server/servers or server/browser all communication on internt can only be done only with text (even when we send a image or video it is a text). Because the internet is based in the protocol TCP thats only support text

When we send a image the information that is send is text that are numbers that represent RGB for each pixel which is in the image.

- JSON is one format that is used to send organize texts between server/servers or server/browser

This is a simple strucute of JSON file (file-> value). The last line dont have commma

{

  "field1": "abc",
  
  "field2": "def",
  
  "field3": 4,
  
  "array": [1,2,3,4, "abc"],
  
  "array of objects"
  
}


**JSON Files**
When we send arrays of objects we can send a array with objects that contais other objects, that is another JSON:

- array [objects(objects)]

{

  "field1": "abc",
  
  "field2": "def",
  
  "field3": 4,
  
  "array": [1,2,3,4, "abc"],
  
  "array of objects":[
    
    {
      "field1_of object_1": 1
    },
    
    {
      "field2_of object_2": "this is a string"
    }
    
  ]
  
  "array of nested arrays": [
    
    {
    
       "nested array": [
       
          {
          
           "field1":1
           
           "name": "Olchenback"
      
          } #End first object of first nested array
          
       ] # End first nested array
    
    } # End the objects inside array of nested arrays
   
    
    
  ] #End array Nested array
     
  
} #end JSON FILE


**Array of nested arrays**

This is the output of the first exmaple of JSON files

![json_example](https://user-images.githubusercontent.com/37953610/57933258-b2c1c300-78b4-11e9-9275-0772e6e6c225.png)

**Install Postman**

- sudo wget https://dl.pstmn.io/download/latest/linux64 -O postman.tar.gz

- sudo tar -xzf postman.tar.gz -C /opt

- sudo rm postman.tar.gz

- sudo ln -s /opt/Postman/Postman /usr/bin/postman

- run postman type in terminal: postman

## Error chart for app2.py

![error_chart](https://user-images.githubusercontent.com/37953610/57983413-7d021300-7a49-11e9-918b-2748b2c2929b.png)


## Docker Container
- Scenario 1

Imagine that the Developer 1, uploaded your code which was developed in your local manchine. This code was using the Environnment 1. So, a Developer 2 download this code to your local machine and when use it your own envinronment to run the code that was downloaded he gets a bunch of errors. It happens because the two envinronments have different libraries and configurations. 

- Scenario 2
Imagine that after the two developers fixed all errors and posted it to the server that was buyed to run the code in production. The server have different environment and IDE from the two different developers and the code crashs in production.

**Solution**

- 1: Virtualization: It is a Virtual machine installed in your local computer that is a replica of the envinronment of the Server to guarantee thaht the code developed in your local machine is able to run in virtual machine installed and because for that guarantee that the same code will ruin in the server too. This solution have many abstaraction and the things are really slow when you put the code run in your virtual amchine because have only a few resources (memory, hd, etc).

![virtualization](https://user-images.githubusercontent.com/37953610/57986171-6ec3ef00-7a69-11e9-8d05-a3ac16819c49.png)


- 2: Docker (Linux container): The Docker Engine exists in your Operator System (OS).  The Docker Engine can hosts multiple applications (APP1... APPn). Each application have your own OS, code, environment and IDE. The Docker Engine translate the Application for your OS for theat application can run in your OS without any problem. Here, in this situation, Application is understood as a Container because a container can be anything . A container is made by a image. For example, a image can be a text file describes all proprieties of the environment that application should run (Ubuntu 16.0.4; Python 3; code developed; etc..). When your code is already to deploy to the Server, you need to install Docker Engine in the Server.After that you only need put the Image of the container in the Server and run it. And Docker guarantees that your code that runs in the image will run in the Server because the docker engine will translate the image to the server. It is the amin function of a docker contianer. 

![docker_explained](https://user-images.githubusercontent.com/37953610/57986410-789b2180-7a6c-11e9-888d-e576500c3d03.png)

## Docker Compose

Is a application to controle a docker that have a multiple containers. When have a need to comunicate between dockers the Docker compose can helps in that communication using a yaml file. 

Search in google for: download docker ubuntu and click in the site: Get Docker CE for Ubuntu

Once in the site goes to:Install using the repository and follows the instructions that are described there.


- sudo apt-get update

- sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
    
 - curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
 
 - sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
   
 - sudo apt-get update
   
 - sudo apt-get install docker-ce docker-ce-cli containerd.io
   
 - sudo docker run hello-world
   
 - Successfull Instalation
   
   ![docker_install](https://user-images.githubusercontent.com/37953610/57986717-7f2b9800-7a70-11e9-83cf-088e0264aa5a.png)

**Download and Install Docker Compose**

- Go to the website: https://docs.docker.com/compose/install

- Run the next commands:

    - sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

    - sudo chmod +x /usr/local/bin/docker-compose
    
    - docker-compose --version
    
![docker_compose](https://user-images.githubusercontent.com/37953610/57986824-a9318a00-7a71-11e9-9ed1-c948338f1e78.png)






