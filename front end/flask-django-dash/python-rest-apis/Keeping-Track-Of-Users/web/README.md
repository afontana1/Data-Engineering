## Objective

The main objective is improve the app.py builded to do the four elementary operations: add, subtraction, division, multiplication.

Here we are build a MongoDB database to store how many times the user requires an operation. If the same user have more than five requirements the app blocks the access. In other words, an user have a limite of five requirements. For that the user can provide the UserName(User) and the PassWord(PW) to the app controls how many times the app was required by user. This information will be stored in a MongoDB databse.

## MongoDB

The next table mkes the correlations among a Relational DB with a MongoDB. For instance we can see that in a **RBMS** a **Table** is compound by **Rows** and **Colunms**. But in a **MondoDB** a table is a Collection. In MondoDB, **Collections** is compounded by **Documents** and **Fields**. 


![RDMS_MongoDB](https://user-images.githubusercontent.com/37953610/58112126-be7df400-7bea-11e9-9da1-8efb24a95417.png)

![doc_MB](https://user-images.githubusercontent.com/37953610/58112767-0d785900-7bec-11e9-8137-651067eed5fb.png)



The **id** field in the MongoDB means the primary key of the Collection. This primary key is a 12 bytes hexadecimal number which assures the uniqueness of every document and it is build as:

- 4 bytes for the current timestamp
- next 3 bytes for machine id
- next 2 bytes for process if od MongoDB server
- last 3 bytes are simple incremental VALUE

In general, in a Relational DB we have a schema that shows a number of tables and the relashionship between these tables. While in MongoDB, there is no concept of relationship.

**Advantages of  MongoDB over RDBMS**

  1 - Schema Less - MongoDB is a document database in which one collection holds different documents. Number of fields, content and size of the document can differ from one document to another.
  
  2 - Structure of a single object is clear
  
  3 - No complex joins
  
  4 - Seep query-ability: MongoDB supports dynamic queries on documents using a document based query language that's nearly powerful as SQL (Relational DB).
  
  5 - Tuning
  
  6 - Ease of scale out: MongoDb is easy to scale
  
  7 - Conversion/mapping of application objects to databse objects not neeeded. 
  
  8 - Uses internal memory for storing the (windowed) working set, enabling faster access of data.
  
  **Where to use MongoDB?**
  
   1 - Big Data : sclable and fast
   
   2 - Content Management and Delivery
   
   3 - Mobile and Social Infrastructure
   
   4 - User Data management
   
   5 - Data Hub
   
**Install MongoDb on Ubuntu 18.04 LTS**
   
Go to site and follow the instructions:

   https://websiteforstudents.com/install-mongodb-on-ubuntu-18-04-lts-beta-server/
   
Or simple copy and past in your terminal the next set of commands:

  1 - sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
  
  2 - echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
  
  3 - sudo apt update
  
  4 - sudo apt install -y mongodb-org 
  
  5- Run one of the next commands in according with your objective
  
    - sudo systemctl stop mongod.service
    - sudo systemctl start mongod.service   (for start MongoBD)
    - sudo systemctl enable mongod.service
   
 6 - sudo systemctl status mongod    (to see the status)
 
 ![mongoinst-1](https://user-images.githubusercontent.com/37953610/58115754-ac07b880-7bf2-11e9-963a-6aeed7847b02.png)
 
 7- To run MongoDB type in terminal only: mongo
 
 8 - To see the options: db.help()
 
 9 - To see the status:  db.status()
 
 10- To see the version of MongoDB: db.version()
 
 ![version_mongoDB](https://user-images.githubusercontent.com/37953610/58115875-e8d3af80-7bf2-11e9-93d3-d192c01f2ee7.png)
 
 ## Representation of the same problem in Relational DB and in a MongoDB
 
 **Problem Definition**
 
 Suppose a client needs a database design for his blof/website and see the differences between RDBMS and MongoDB schema design. Website has the following requirements:
 
 - Every post has the unique title, description and url
 
 - Every post can have one or more tags
 
 - Every post has the name of its publisher and total number of likes
 
 - Every post has comments given by users along with their name, message, data-time and likes
 
 - On each post, there can be zero or more comments.
 
 **Relation Database**
 
 ![RDB-Prob1](https://user-images.githubusercontent.com/37953610/58119602-45d36380-7bfb-11e9-81c5-432cc81c9174.png)
 
 **Mongo DB**
 
 ![Mongo-Prob1](https://user-images.githubusercontent.com/37953610/58119629-4ff56200-7bfb-11e9-90f4-af7c3ecc9232.png)
 
 ## First Commands in MongoDB
 
 **1. Create and Delete Databases**
 
 - _use nameDB_ : Create an non-existence DB or use a existent DB
 
 - _db_ : To check your currently selected database
 
 - _show dbs_ : To check your databases list
 
 **Note:** Your db created only appears on the list after you insert at lesat one document into your created db:
 
      db.movie.insert({"name":"tutorial"})

After you insert a document use _show dbs_ command to see your db in the list. 

**Attention:** As default the MongoDB creates a db named as test. If you didn't create any databse, then collections will be stored in the test database. 

  - _db.dropDatabase()_ : To drop a exisiting database. If you have not selected any database, then it will delete default 'test' database.
  
        use mydb                # use the Databse mydb
        db.dropDatabase()       # drop the Database mydb
        show dbs                # check if the Database was dropped 
        
**2. Create and Drop a Collection**

- _db.createCollection(name,options)

- _name_ : it is the name of collection to be created

- _options_ (this paramenter is optional): it is a document and is used to specify configuration of collection

  - Capped (boolean) : when insert the new element it removes the oldest element, because capped collection is a fixed size collection that automatically overwrites its oldets entris when it reaches its amximum size.
  
  - autoIndexId (boolean) : If irue, automatically create index on id fields. default value is False
  
  - Size (number) : when the capped is true you need to scificies a maximum size in bytes for a capped collection
  
  - Max (number) : if the capped is true specifies the maximum number of documents allowed in the capped collection
  
        use test
        db.createCollection("mycollection")
        show collections
        
        db.createCollection("mycol", {
          capped: true,
          autoIndexId: true,
          size: 6142800,
          max : 10000
          })
    
 **Note:** In MongoDB, you don't need to create collection. MongoDB creates collection automatically, when you insert some document.
 
        # The next line creates a collection with a name magicalCollection
        db.magicalCollection.insert({"name" : "magicalCollection"})     
        show collections
        
- _db.CollectionName.drop()_ : it drops a the CollectionName from the database
  
        use mydb
        show collections
        db.mycollection.drop()
        show collections
        
**3. Inserting Documents to Collections**

- _db.CollectionName.insert(document)_ : you can use the _insert()_ or the _save()_ method to create a document
    
        db.mycol.insert({
          _id: ObjectId(7df78ad8902c),
          title: "MongoDB Overview",
          description: "MongoDB is no sql database",
          tags: ["mongodb", "database","NoSQL"],
          likes: 100
        })
        
 **Note:** To insert multiple documents ina a single query, you can passa an array of documents in _insert()_ command, like this:
 
        db.mycol.insert([{},{},{},{}])     # you insert four empty documents
    
## Data Types MongoDB

Some of datatypes supported by MongoDB:

  - string : must be UTF-8 valid
  
  - integer : integer can be 32 bit or 64 bit depending upon your server
  
  - boolean : true / false
  
  - double : for store floating point values
  
  - min / max keys : used to compare a value against the lowest and highest BSON elements
  
  - arrays
  
  - timestamp - ctimestamp. This can be handy for recording when a document has been modified or added
  
  - object : thsi datatype is used for embedded documents
  
  - null : this type is used to store a null value
  
  - symbol : it's generally reserved for languages tha tuse a specific symbol type
  
  - date : to store the current date or time in UNIX time format. You can specify your own date time by creating object of Date and passing day, month, year into it.
  
  - object id : it is used to store the document's ID.
  
  - binary data : it is used to store binary data
  
  - code : it is to store JavaScript code into the document
  
  - regular expression : it is used to store regular expression
 
 ## Query Documents
 
 - _find()_ 
 
        # it will display all documents in a non-structured way
        db.CollectionName.find({})         # display all documents
        
        # it will display in a formatted way
        db.CollectionName.pretty({})       # display all documents  
        
  - _findOne()_ : that returns only one document
  
  **1. Filters**
  
 - Equality: 
  
        db.mycol.find({
          "title":"MongoDB Overview"
        }).pretty()
  
 - Less Than:
  
        db.mycol.find({
          "likes":{$lt:50}
        }).pretty()
  
 - Less Than Equals:
  
        db.mycol.find({
          "likes":{$lte:50}
        }).pretty()
        
 - Greater Than: 
  
        db.mycol.find({
          "likes":{$gt:50}
        }).pretty()
               
- Greater Than Equals: 
  
        db.mycol.find({
          "likes":{$gte:50}
        }).pretty()
        
                
- Not Equals:  
  
        db.mycol.find({
          "likes":{$ne:50}
        }).pretty()
        
**2. AND in MongoDB**

In _find()_ method, if you pass multiple keys by separating them by ',' then MongoDB treats it as AND condition.

        db.mycol.find({
          $and:[
            {
              "likes":{$gte:50}
            },
            {
              "title":"MongoDB Overview"
            }
          ]
        }).pretty()
 
 **3. OR in MongoDB**
 
 You need to use _$or_ keyword.
 
         db.mycol.find({
           $or:[
            {
              "likes":{$gte:50}
            },
            {
              "title":"MongoDB Overview"
            }
           ]
          }).pretty()

## 4. Updating Documents in MongoDB

- _update()_ : it updates values in the existing document 

      db.CollectionName.update(SelectionCriteria,UpdatedData)
      
      db.mycol.update( 
        {
        "title":"MongoDb Overview"
        },
        {
        $set: {"title":"New Mongo DB Tutorial"}
        }
      )
   
 **Note:** To update multiple documents, you need toset a parameter 'multi' to true.
 
      db.mycol.update( 
        {
        "title":"MongoDb Overview"
        },
        {
        $set: {"title":"New Mongo DB Tutorial"}
        },
        {multi:true}
      )

- _save()_ : it replaces the existing document with the document passed in saved() method

- _remove() : to delete a document

      db.CollectionName.remove(DelletionCritteria)

      db.mycol.remove({
        "title":"MongoDb Overview"
      })

## Projection

In MongoDB, projection means selecting only the encessary data rather than selecting sholeof the data of a document. If a document has 5 fields and you need to show only 3, then select only 3 fields from them.

MongoDB's _find()_ method, explained before accpets second optional parameter that is kist of fields that you want to retrieve. In MongoDB, when tou execue _find()_ method, then it displays all fields of a document. To limit this, you need to set a list of fields with value 1 or 0, 1 is used to show the field while 0 is used to hide the fields.

    # This only return the titles(show=1) and not the _id (hidden=0)
    db.mycol.find({},{"title":1,_id:0})
    
## Limiting Records

This is used to limit the records displayed by the _find()_ command.

    db.CollectionName.find().limit(Number)
    
    db.mycol.find({},{"title":1,_id:0}).limit(1)   # shows only one document
    
## Sorting Documents

The _sort()_ method accpets a document containig a list of fields along with their soring order. To specify sorting order 1(ascending order) and -1(descending order) are used. 

    db.CollectionName.find().sort({KEY:1})
    
    db.mycol.find().sort({"likes":1})
    
