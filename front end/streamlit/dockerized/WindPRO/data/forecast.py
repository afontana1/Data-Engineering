from datetime import date
import pandas as pd
import requests

URL = "https://api.open-meteo.com/v1/gfs"
LATIUDE = 54.76
LONGITUDE = 18.51

def get_forecast(past_days = 0, forecast_days = 3) -> pd.DataFrame:
    '''Get the forecast using open-meteo api.
       
    Args:
        past_days: numbers of forecast days into the past.
        forecast_days: days of forecast into the future.
    Returns:
        forecast in tabular form in 2h intervals.'''
    today = date.today()
    # Define the parameters for the API request
    params = {
        "latitude": LATIUDE,
        "longitude": LONGITUDE,
        "hourly": "windspeed_10m,windgusts_10m,winddirection_10m,temperature_2m,precipitation,cloudcover",
        "windspeed_unit": "kn",
        "timezone": "Europe/Berlin",
        "forecast_days": forecast_days,
        "past_days": past_days
    }
    # Make the GET request to the API
    response = requests.get(URL, params=params)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        df = pd.DataFrame()
        # Access the specific data you need (e.g., windspeed, wind direction, and wind gusts)
        df['Time'] = pd.to_datetime(data['hourly']['time'])
        df['WindForecast'] = data["hourly"]["windspeed_10m"]
        df['GustForecast'] = data["hourly"]["windgusts_10m"]
        df['WindDirForecast'] = data["hourly"]["winddirection_10m"]
        df['Temperature'] = data["hourly"]["temperature_2m"]
        df['Precipitation'] = data["hourly"]["precipitation"]
        df['Cloudcover'] = data["hourly"]["cloudcover"]
        

        # Set the 'Time' column as the index
        df.set_index('Time', inplace=True)

        # Resample the data with a two-hour interval and apply mean aggregation
        df = df.resample('2H').mean()

        df.reset_index(inplace=True)

        df['Month'] = df['Time'].dt.month
        df['Hour'] = df['Time'].dt.hour
        df['Update'] = today

    else:
        # Handle the error
        print(f"Failed to retrieve data. Status code: {response.status_code}")
    if past_days==7:
        df = df[df['Time'].dt.date < today]
    return df
