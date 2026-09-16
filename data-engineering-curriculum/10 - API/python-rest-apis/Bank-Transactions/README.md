### Building a Bank API 

Suppose a Bank which have a safe-deposit box with a lot of money and you open different accounts in this Bank. Now we make a deposit in one bank account and you do money transfer between accounts. You can take a loan from the Bank. In this sense it will increase your cash as well your debit. Our API want to ensure the transactions between the accounts are corrected and is no problem.


**Resources**

- Register a new user

    - URL: /register
    - Method: POST
    - Parameters : username , password
    - status codes: 
      - 200 ok
      - 301 invalid username
      - 302 invalid password

- Add: allows you to add money to bank account

    - URL: /add
    - Method: POST
    - Parameters : username , password, amount
    - status codes: 
      - 200 ok : return the similarity between two documents
      - 301 invalid username
      - 302 invalid password
      - 304 negative amount

- Transfer : transfer money between accounts

    - URL: /transfer
    - Method: POST
    - Parameters : username , password, to, amount
    - status codes: 
      - 200 ok
      - 301 invalid username
      - 302 invalid password
      - 303 not enough money
      - 304 negative amount

- CheckBalance : 

    - URL: /balance
    - Method: POST
    - Parameters : username , password
    - status codes: 
      - 200 ok
      - 301 invalid username
      - 302 invalid password
      
- Takeloan : 

    - URL: /takeloan
    - Method: POST
    - Parameters : username , password, amount
    - status codes: 
      - 200 ok
      - 301 invalid username
      - 302 invalid password
      - 304 negative amount
 
- Payloan : 

    - URL: /payloan
    - Method: POST
    - Parameters : username , password, amount
    - status codes: 
      - 200 ok
      - 301 invalid username
      - 302 invalid password
      - 303 not enough money
      - 304 negative amount
    
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *    

## Building a Docker Compose from scratch
    
Inside of the main folder (i.e BankAPI) run the below commands
    
    touch docker-compose.yml
    mkdir web                            # where we develop our API
    mkdir db                             # to store in mongDB informations about the users among of them username and passwords
    touch web/Dockerfile
    touch web/app.py
    touch web/requirements.txt
    touch db/DockerFile
   


* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
## Test the BANK API

**To Run**: In the mail foler (BankAPI/) run:

    sudo docker-compose build
    sudo docker compose up

**Postman**: To test the API go to Postman

Here we can do a little diferent as usual. We write all entries for all roots (register, classify and register) and we will select one of them to see what happens. For each root only the fields that the root is expected are automatically read.

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
       
Now, select Body with option raw and JSON(application/json) and register BANK:

    {
      "username": "BANK",
      "password": "secure"
    }

After click on Send blue bottom you will receive the status 200.

Register user1 and user2:

    {
      "username": "user1",
      "password": "secure"
    }
    
    {
      "username": "user2",
      "password": "secure"
    }

If you try register the same user twice you will receive a status error 301.

- Balance of the Bank. Select POST and write:

        localhost:5000/balance
    
Click on Send blue bottom and you will see the bank don't have already Debt and Own:

    {
      "Debt": 0,
      "Own": 0,
      "Username": "BANK"
    }

- Add. Select POST and write:

        localhost:5000/add
        
Add money to user1:

    {
      "username": "user1",
      "password": "secure",
      "amount": 100
    }     
    
After click on Send blue bottom you will receive the status 200.       

- Balance of the user1. Select POST and write:

        localhost:5000/balance
        
Click on Send blue bottom and you will see the bank don't have already Debt and Own:

    {
      "Debt": 0,
      "Own": 99,
      "Username": "user1"
    }
    
 Because the Bank take 1 from the user. You can now check the balance of the Bank and you will see
 
     {
      "Debt": 0,
      "Own": 1,
      "Username": "BANK"
    }

- Transfer. The user1 transfer money to user2. Select POST and write:

        localhost:5000/transfer
        
Now, select Body with option raw and JSON(application/json) and register BANK:

    {
      "username": "user1",
      "password": "secure",
      "to": "user2",
      "amount": 20
    }
Click on Send blue bottom and you will see the status 200.     
    
- Balance. Check the balance of the user2. Select POST and write:

        localhost:5000/balance
  
Now, select Body with option raw and JSON(application/json) and register BANK:

    {
      "username": "user2",
      "password": "secure",
    }
Click on Send blue bottom and you will see:

    {
      "Debt": 0,
      "Own": 19
      "Username":"user2"
    }

Since the bank takes 1 from the transfer the user2 only has 19.

Check the TakeLoan and PayLoan and after that check the balance to see differences.
