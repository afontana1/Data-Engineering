import base64
import numpy as np
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

######################################################## HELPER FUNCTIONS ########################################################
def get_config() -> str:
    '''Retrieves the database configuration from Streamlit's secrets and constructs the database URL.'''
    PG_HOST=st.secrets.db_credentials.pg_host 
    PG_PORT=st.secrets.db_credentials.pg_port
    PG_DATABASE=st.secrets.db_credentials.pg_database
    PG_USER=st.secrets.db_credentials.pg_user
    PG_PASSWORD=st.secrets.db_credentials.pg_password

    # Create the MySQL database connection string
    db_url = f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'
    
    return db_url

# Function to apply the transformations
def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies transformations to the input dataframe, including formatting of time and wind data.

    Args:
        df: The original dataframe from RDS postgres with wind and time data.

    Returns:
        The transformed dataframe suitable for display in streamlit.
    """
    # Convert the 'Time' column to datetime if it's not already
    df['Time'] = pd.to_datetime(df['Time'])

    # Extract the day and format it
    df['Day'] = df['Time'].apply(lambda x: x.strftime(f"%A {format_day_suffix(x.day)}"))

    # Extract the hour
    df['Hour'] = df['Time'].dt.hour

    # Round the 'Wind' column to 0 decimal places
    df['Wind [kt]'] = df['Wind'].round(0).astype(int)

    # Round the 'Wind' column to 0 decimal places
    df['Gust [kt]'] = df['Gust'].round(0).astype(int)

    # Drop the original 'Time' column
    df = df.drop(columns=['Time'])

    # Define refined bins and labels for wind direction
    bins = np.arange(0, 361, 22.5)
    labels = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N']

    # Bin wind directions with the refined bins and labels
    df['Direction'] = pd.cut(df['Direction'] % 360, bins=bins, labels=labels[:-1], include_lowest=True)

    # Mapping for direction arrows
    arrows = {
        'N': '↓', 'NNE': '↓', 'NE': '↙', 'ENE': '←',
        'E': '←', 'ESE': '←', 'SE': '↖', 'SSE': '↑',
        'S': '↑', 'SSW': '↑', 'SW': '↗', 'WSW': '→',
        'W': '→', 'WNW': '→', 'NW': '↘', 'NNW': '↓'
    }

    # Add a new column for the arrows
    df['Arrow'] = df['Direction'].map(arrows)

    return df[['Day', 'Hour', 'Wind [kt]', 'Gust [kt]', 'Direction', 'Arrow']]

def _get_base64(file_path: str) -> str:
    '''Reads a file and converts it to a base64 encoded string.'''
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(file_path: str) -> None:
    '''Sets a background image for a Streamlit app using a base64 encoded image.'''
    base64_image = _get_base64(file_path)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_image}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def get_metrics() -> pd.DataFrame:
    '''
    Fetches test metrics from the database and processes them into a pandas dataframe.

    Returns:
        A dataframe containing processed test metrics in a suitable format for streamlit.
    '''
    db_url = get_config()

    engine = create_engine(db_url)

    # Use the engine to connect to the database
    connection = engine.connect()

    df_metrics = pd.read_sql('select * from latest_metrics', connection)
    df_params = pd.read_sql('select * from params', connection)
    df_runs = pd.read_sql('select * from runs', connection)
    
    connection.close()

    df_params.rename(columns={'key': 'param', 'value': 'param_value'}, inplace=True)

    df_metrics_runs = pd.merge(left=df_metrics, right=df_runs, how='left', on='run_uuid')
    df_metrics_runs = df_metrics_runs[df_metrics_runs['name'].str.contains('test')].drop_duplicates()
    df_metrics_runs['date'] = df_metrics_runs['name'].str.extract(r'test_run_prod_(\d{4}-\d{2}-\d{2}-\d{2}-\d{2})')

    # Convert the extracted string to a datetime object
    df_metrics_runs['date'] = pd.to_datetime(df_metrics_runs['date'], format='%Y-%m-%d-%H-%M')

    df_joined = pd.merge(left=df_metrics_runs, right=df_params, how='inner', on='run_uuid')
    df_joined = df_joined[df_joined['experiment_id'] == 1]
    df_joined = df_joined[df_joined['param_value'].isin(['gust', 'base', 'rewa', 'kuznica'])]
    df_joined = df_joined[df_joined['key'].isin(['test_rmse','forecast_rmse'])]
    df_joined = df_joined.sort_values(by='date', ascending=False).head(16)
    
    df_result = df_joined.groupby('timestamp').agg({
        'param_value': lambda x: ', '.join(map(str, x)),
        'key': 'first',
        'value': 'first'
    }).reset_index()[['param_value','key','value']]

    df_result['param_value'] = df_result['param_value'].apply(lambda x: ', '.join(sorted(x.split(', '))))
    df_result = df_result.pivot_table(index='param_value', columns='key', values='value').reset_index()[['param_value','forecast_rmse','test_rmse']]
    
    df_result.rename(columns={'forecast_rmse':'Forecast Accuracy (RMSE)', 'test_rmse':'WindPRO Accuracy (RMSE)', 'param_value': 'Model'}, inplace = True )
    df_result['Improvement [%]'] = (df_result['Forecast Accuracy (RMSE)'] - df_result['WindPRO Accuracy (RMSE)'])/df_result['Forecast Accuracy (RMSE)'] * 100
    return df_result


#############################################################################################################################################

if __name__ == '__main__': 
    set_background('kuznica.jpeg')
    df_metrics = get_metrics()

    # Dropdown to select the table
    option = st.selectbox(
        'Which location would you like to display?',
        ('rewa', 'kuznica'),
        placeholder="Select location...",
        index=None,
    )

    db_url = get_config()

    # Create an SQLAlchemy engine
    engine = create_engine(db_url)

    # Use the engine to connect to the database
    connection = engine.connect()

    query_rewa = 'SELECT * FROM current_pred_rewa'
    query_kuznica = 'SELECT * FROM current_pred_kuznica'

    df_rewa = pd.read_sql(query_rewa, connection)
    df_kuznica = pd.read_sql(query_kuznica, connection)

    connection.close()
    # Function to format the day with suffix

    def format_day_suffix(d):
        if 10 <= d <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')
        return f"{d}{suffix}"

    # Transform the DataFrame
    transformed_df_rewa = transform(df_rewa)
    transformed_df_kuznica = transform(df_kuznica)


    if option == 'rewa':
        set_background('rewa.jpeg')
        # Title for the table
        st.markdown("### Forecast for Rewa, Poland enhanced with Machine Learning")

        # Display the transformed DataFrame
        st.dataframe(transformed_df_rewa, width = 500, height = 800)
        st.dataframe(df_metrics)
    elif option == 'kuznica':
        set_background('kuznica.jpeg')
        st.markdown("### Forecast for Kuznica, Poland enhanced with Machine Learning")

        # Display the transformed DataFrame
        st.dataframe(transformed_df_kuznica, width = 500, height = 800)
        st.dataframe(df_metrics)
