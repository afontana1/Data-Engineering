from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)         # the Api takes our app from Flask

# Here we define the additional functions to help informe the user
def checkPostedData(postedData, functionName):
    if (functionName == "add" or functionName == "subtract" or functionName == "multiply"):
        if "x" not in postedData or "y" not in postedData:
            return 301              # an error occured: missing "x" or "y" value
        else:
            return 200              # all ok
    elif (functionName == "division"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif int(postedData["y"]) == 0:
            return 302
        else:
            return 200

#Here we build our resources in accordance with our Resources Chart already defined
class Add(Resource):
    def post(self):
        #If I am here, then the resource Add was requested using the method POST

        #Step 1: Get posted Data:
        postedData = request.get_json()

        # Step 1b: Verify the validity of the posted data
        status_code = checkPostedData(postedData, "add")
        if (status_code != 200):
            retJson = {
                "Message": "An error occured",
                "Status Code":status_code
            }
            return jsonify(retJson)


        x = postedData["x"]
        y = postedData["y"]

        x = int(x)
        y = int(y)

        # Step 2: Add the posted date
        ret = x + y

        # Step 3: Return the response to the user
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)
#    def get(self):
#        #If I am here, then the resource Add was requested using the method GET

#    def put(self):
#           #If I am here, then the resource Add was requested using the method PUT
#    def delete(self):
#           #If I am here, then the resource Add was requested using the method DELETE

class Subtract(Resource):
    def post(self):
        #If I am here, then the resource Subtract was requested using the method POST

        #Step 1: Get posted Data:
        postedData = request.get_json()

        # Step 1b: Verify the validity of the posted data
        status_code = checkPostedData(postedData, "subtract")
        if (status_code != 200):
            retJson = {
                "Message": "An error occured",
                "Status Code":status_code
            }
            return jsonify(retJson)


        x = postedData["x"]
        y = postedData["y"]

        x = int(x)
        y = int(y)

        # Step 2: Subtract the posted date
        ret = x - y

        # Step 3: Return the response to the user
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Multiply(Resource):
        def post(self):
            #If I am here, then the resource Multiply was requested using the method POST

            #Step 1: Get posted Data:
            postedData = request.get_json()

            # Step 1b: Verify the validity of the posted data
            status_code = checkPostedData(postedData, "multiply")
            if (status_code != 200):
                retJson = {
                    "Message": "An error occured",
                    "Status Code":status_code
                }
                return jsonify(retJson)


            x = postedData["x"]
            y = postedData["y"]

            x = int(x)
            y = int(y)

            # Step 2: Multiply the posted date
            ret = x * y

            # Step 3: Return the response to the user
            retMap = {
                'Message': ret,
                'Status Code': 200
            }
            return jsonify(retMap)

class Divide(Resource):
    def post(self):
        #If I am here, then the resource Divide was requested using the method POST

        #Step 1: Get posted Data:
        postedData = request.get_json()

        # Step 1b: Verify the validity of the posted data
        status_code = checkPostedData(postedData, "division")
        if (status_code != 200):
            retJson = {
                "Message": "An error occured",
                "Status Code":status_code
            }
            return jsonify(retJson)


        x = postedData["x"]
        y = postedData["y"]

        x = int(x)
        y = int(y)

        # Step 2: Divide the posted date
        ret = (x*1.0) / y

        # Step 3: Return the response to the user
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

# This section add the several resources to our API
api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/division")

@app.route('/')
def hello_world():
    return "Hello world!"

if __name__=="__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0') ##localhost
