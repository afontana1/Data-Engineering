import ast
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import re
import requests
import time

def get_measurments(station: str, past_days: int) -> pd.DataFrame:
    '''Scraper to get the weather measurments from the weather station.
    
    Args:
        station: string representing the name of the weather station.
        past_days: number of past measurment days.
    Returns:
        pandas dataframe representing measurments in 10 min intervals.'''
    df = pd.DataFrame()
    
    # Calculate the start and end dates for the past N days
    end_date = datetime.today()
    start_date = end_date - timedelta(days=past_days)
    
    # Create a list of dates for the date range
    day_list = pd.date_range(start=start_date, end=end_date)

    for date in day_list:
        # Extract info for url
        day = date.day
        month = date.month
        year = date.year

        url = f"http://www.wiatrkadyny.pl/{station}/wxwugraphs/graphd1a.php?theme=pepper&d={day}&m={month}&y={year}&w=900&h=350"

        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Regex to retrive data from html
            patternWindSpeed = r'var dAvgWS\s*=\s*(\[.*?\]);'
            patternWindGust = r'var dGustWS\s*=\s*(\[.*?\]);'

            # Use re.findall to find all matches in the HTML content
            WindSpeed = re.findall(patternWindSpeed, str(soup.contents), re.IGNORECASE | re.DOTALL)
            WindGust = re.findall(patternWindGust, str(soup.contents), re.IGNORECASE | re.DOTALL)

            # Remove the trailing comma to make it a valid JSON-like format
            WindSpeed = ast.literal_eval(WindSpeed[0].rstrip(','))[:-1]
            WindGust = ast.literal_eval(WindGust[0].rstrip(','))[:-1]

            # Convert from m/s to knots
            WindSpeed = [np.round(speed * 1.94384449,2) for speed in WindSpeed]
            WindGust = [np.round(speed * 1.94384449,2) for speed in WindGust]

            # Define the date and time components
            hour = 0  # Starting hour
            minute = 0  # Starting minute
            second = 0  # Starting second
            datetime_values = [] # Create a list to store datetime values
            # Create datetime values with 10-minute intervals for the entire day
            while hour < 24:
                current_datetime = datetime(year, month, day, hour, minute, second)
                datetime_values.append(current_datetime)
                minute += 10
                if minute == 60:
                    minute = 0
                    hour += 1

            # Find the minimum length between datetime_values, WindSpeed, and WindGust
            min_len = min(len(datetime_values), len(WindSpeed), len(WindGust))

            # Trim all the lists to the minimum length
            datetime_values = datetime_values[:min_len]
            WindSpeed = WindSpeed[:min_len]
            WindGust = WindGust[:min_len]

            # Create a DataFrame
            data = {
                'Time': datetime_values,
                'WindSpeed': WindSpeed,
                'WindGust': WindGust,
            }

            # Concat to the global dataframe, skip if data corrupted for current day
            try:
                df_i = pd.DataFrame(data)
                df = pd.concat([df,df_i])
            except ValueError:
                print(f'Data inconsistent for day: {day}.{month}.{year}. Skiping...')
                pass
            time.sleep(3)

        else:
            print(f"Failed to fetch data from {url}")

    df['Update'] = date.today()

    return df

