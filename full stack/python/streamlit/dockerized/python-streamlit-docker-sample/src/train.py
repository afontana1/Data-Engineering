from sklearn.linear_model import LinearRegression
from datetime import datetime
import pandas as pd
import pickle

def train():
    df = pd.read_csv('data/beach_chairs.csv')
    dependent_var = "beach_chairs"

    df['Date'] = df['Date'].apply(check_weekday)

    X = df.drop(dependent_var, axis="columns")
    y = df[dependent_var]

    linear_model = LinearRegression()
    linear_model.fit(X, y)

    pickle.dump(linear_model, open(f"./model/model.sav", 'wb'))

# returns the day of week as numeric value from 0 to 6
def check_weekday(date):
    return datetime.strptime(date, '%Y-%m-%d').weekday()

if(__name__ == "__main__"):
    train()
