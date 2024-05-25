from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

def get_graph(period = 'JJA'):
    # Import libraries
    import pandas as pd
    import plotly.express as px

    df = pd.read_csv('GlobalTemps1880-2022.csv')
    fig = px.bar(df, x='Year', y = period, color=period, title = period, 
        color_continuous_scale='reds', template='none', width=1000, height=500)

    graphJSON = fig.to_json()

    return json.dumps(graphJSON)

def template(params):
    return render_template(params['template'], params=params)

@app.route('/')
def index():
    return render_template('index.html')

#### Simple template ####

@app.route('/simple')
def simpleindex():
    # The root endpoint builds the page
    header = "Global Temperature"
    subheader = "Global Temperature changes over the last few centuries"
    description = """The graph shows the increase in temperature year on year.
    The data spans the years 1881 to 2022 and includes temperature anomalies for groups of months such as the June through August.
    """
    params = {
        'template':'simpleindex.html',
        'title': header,
        'subtitle': subheader,
        'content' : description,
        'graph'   : get_graph()
    }
    return template(params)


#### Simple template with dropdown ####

@app.route('/ddsimple')
def ddsimpleindex():
    # The root endpoint builds the page
    header = "Global Temperature"
    subheader = "Global Temperature changes over the last few centuries"
    description = """The graph shows the increase in temperature year on year.
    The data spans the years 1881 to 2022 and includes temperature anomalies for periods of each year as indicated.
    """
    menu_label = "Select a period"
    params = {    
        'template': 'ddsimpleindex.html',
        'title': header,
        'subtitle': subheader,
        'content' : description,
        'menu_label': menu_label,
        'options' : [{'code':'J-D', 'desc':'Whole year'},
                     {'code':'DJF','desc':'Winter (North)'},
                     {'code':'MAM','desc':'Spring (North)'},
                     {'code':'JJA','desc':'Summer (North)'},
                     {'code':'SON','desc':'Autumn/Fall (North)'}],
        'graph'   : get_graph()
    }
    return template(params)


#### Callback for drop down menu ####

@app.route('/callback', methods=['POST'])
def callback():
    # The callback updates the page
    if request.is_json:
        data = request.get_json()
        #print(f"{list(data.keys())}")

        # do something with the incoming data and return the appropiate data 
        print(data['dropdown'])
        return get_graph(period=data['dropdown'])
    else:
        return jsonify({"error": "Invalid JSON data"}), 400

#### Main ####

if __name__ == '__main__':
    app.run(debug=True)


