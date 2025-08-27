import requests
from flask import Flask, render_template, request
import geocoder

app = Flask(__name__)

API_KEY = "03cb5a4d0f2e6fe64268bb64ff10651b"
BASE_URL = "http://api.openweathermap.org/data/2.5/"

#cities weather
def get_weather(city):
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

def get_forecast(city):
    url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

#gps weather coordinates
def get_weather_by_coords(lat, lon):
    url = f"{BASE_URL}weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

def get_forecast_by_coords(lat, lon):
    url = f"{BASE_URL}forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    forecast = None

    if request.method == "POST":
        lat = request.form.get("lat")
        lon = request.form.get("lon")
        city = request.form.get("city")

        if lat and lon:  #GPS detected
            weather = get_weather_by_coords(lat, lon)
            forecast = get_forecast_by_coords(lat, lon)
        else:
            if not city:
                g = geocoder.ip("me")
                city = g.city
            weather = get_weather(city)
            forecast = get_forecast(city)


    return render_template("index.html", weather=weather, forecast=forecast)
# info route
@app.route("/info")

def info():
    return render_template("info.html")
if __name__ == "__main__":
    app.run(debug=True)
