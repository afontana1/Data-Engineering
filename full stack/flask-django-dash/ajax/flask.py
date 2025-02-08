from flask import Flask, render_template, request, jsonify
import feedparser as fp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', weatherData = getWeather("2643123"))

@app.route('/fetchweather/')
def fetchweather():
    return jsonify(getWeather(request.args.get('city')))

def getWeather(city):
    url = f"https://weather-broker-cdn.api.bbci.co.uk/en/forecast/rss/3day/{city}"
    w = fp.parse(url)
    allData = {'feed':w.feed,
               'forecast':w.entries}
    return  allData