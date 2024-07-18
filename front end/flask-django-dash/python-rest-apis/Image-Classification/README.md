### Build an API for Image Recognition - DS API

This API uses Machine Learning for Image Recognition using TensorFlow using a trained model named as Inceptionv3.
The user sends the image to the API and the Machine Learning classifies the image as:

- Person
- Vegetable
- Famouse Person
- Animal
- Transport: cars, airplane, trains, etc.

**Resources**

- Register a new user

    - URL: /register
    - Method: POST
    - Parameters : username , password
    - status codes: 
      - 200 ok
      - 301 invalid username

- Classify: root for classify the image

    - URL: /detect
    - Method: POST
    - Parameters : username , password, image url (image from the internet)
    - status codes: 
      - 200 ok : return the similarity between two documents
      - 301 invalid username
      - 302 invalid password
      - 303 out of tokens

- Refill : allows the admin of the site to add tokens to the users

    - URL: /refill
    - Method: POST
    - Parameters : username , adm_pw, refill_amount
    - status codes: 
      - 200 ok
      - 301 invalid username
      - 304 invalid admin password
    
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *    

## Building a Docker Compose from scratch
    
Inside of the main folder (i.e Tutorial4) run the below commands
    
    touch docker-compose.yml
    mkdir web                            # where we develop our API
    mkdir db                             # to store in mongDB informations about the users among of them username and passwords
        
Inside of folder \Tutorial4\db create a new file:
   
    touch Dockerfile
   
Inside of folder \Tutorial4\web create a new file:

    touch requirements.txt   
    touch Dockerfile
        
**Tensorflow**
For to classify the image using inceptionv3 we to create a new file with the name _classify_image.py_ with the contect that you will find in the Tensorflow repo:
    
    https://github.com/tensorflow/models/blob/master/tutorials/image/imagenet/classify_image.py
   
Inside of this file we need to find the localization of the model. And download the model from there (84.8 MB):

    DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'



* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
## Test the API

**To Run**: In the mail foler (TextSimilarity/) run:

    sudo docker-compose build
    sudo docker compose up

**Postman**: To test the API go to Postman

Here we can do a little diferent as usual a we write all entries for all roots (register, classify and register) and we will select one of them to see what happens. For each root only the fields that the root is expected are automatically read.

Now, select Body with option raw and JSON(application/json) and write:

    {
      "username": "user1",
      "password": "secure",
      "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Zebra_standing_alone_crop.jpg/250px-Zebra_standing_alone_crop.jpg",
      "amount": 2
    }
    
For url adrress is only to search for a image in your web browser (for instance: zebra) and with right click select _Copy Image Address_.

Now we can select each root. 

- First test Register and for that select POST, and write:

       localhost:5000/register

After click on Send blue bottom you will receive the _"msg": "Successfully registration"_

- Now teste the Classify. Select POST and write:

        localhost:5000/classify
    
Click on Send blue bottom and wait a moment until the result appears:

![class_result](https://user-images.githubusercontent.com/37953610/58471452-d2ba7780-813b-11e9-8365-5840d4d0ee20.jpg)

We can see from the result the category with higher probability is zebra. So, it is what we expected the model do.
   

- For last test Refill. 

For that we need run classify more six times until receive the message _"Not enough tokens"_. After that select POST, and write:

       localhost:5000/refill
       
Now we add more 2 credits for the user and you after three using _/classify_ you will get the same message: _"Not enough tokens"_  .
