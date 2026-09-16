from flask import Flask , jsonify, request      # import the require libraries
app = Flask(__name__)                           # start the Flask application calling any name

@app.route('/')                                 # when the webserver see this endpoint the flask get the request the def hello_world
def hello_world():
    return "Hello World!"

@app.route('/hithere')
def hi_there_everyone():
    return "I just hit /hithere"

@app.route('/bye')
def bye():
    # Prepare the resposnse for the request than came to /bye
    c = 2*534
    s = str(c)
#    c = 1/0                                   # it will give us a Internal Server Error. Run it with app.run(debug=True)
    return "bye"

@app.route('/jsexample')
def jsexample():
    age = 2*5
    retJson = {
        'Name': 'Ochenback',
        'Age': age,
        'phones':[
            {
                "phoneName": "Iphone8",
                "phoneNumber": 11111
            },
            {
                "phoneName": "Nokia",
                "phoneNumber": 11121
            }

        ]
    }
    return jsonify(retJson)

@app.route('/add_two_nums', methods=["POST"]) # this only allow the POST method
def add_two_nums():
    # Get x,y from the posted data
    dataDict = request.get_json()    # here we get the post information
    x = dataDict["x"]                # here we take the "x" value posted
    y = dataDict["y"]                # here we take the "x" value posted
    #Add z=x+y
    z = x + y                        # here we add_two_nums
    #Prepare a JSON, "z":z           # here we prepare the JSON structure to return the JSON
    retJson = {
        "z":z
    }
    #return jsonify(map_prepared)
    return jsonify(retJson), 200     # This code is to infor to the user the success of the request
                                     # The 404 code is for the FAIL Request

if __name__=="__main__":
    app.run()
#   app.run(debug=True)

## To run this file type in the terminal
## export FLASK_APP=app.py
## Press Enter
## Write: flask run (and Press Enter)
## Crtl + Shift + C to copy the http address and past it in your browse to see the end result

## To see the response of each end point type in your browser
## http://127.0.0.1:5000/
## http://127.0.0.1:5000/hi_there
## http://127.0.0.1:5000/bye

## For Web Servers API we usually return JSON files

## for Web Applications always return pages (return index.html or return render_template("index.html"))
