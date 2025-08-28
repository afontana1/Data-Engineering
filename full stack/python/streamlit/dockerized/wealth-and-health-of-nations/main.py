import pandas as pd
import plotly.express as px
import streamlit as st
from os.path import exists
from functions import download_data

# Get data

if exists("data.csv"):
    df = pd.read_csv("data.csv")
else:
    df = download_data()
    df.to_csv("data.csv")

st.set_page_config(layout="wide")

# Configure sidebar

years = list(range(1800, 2023))
max_population = int(max(list(df.population.unique())))

# Add filters to page

pcol = st.columns(5, gap="large")
with pcol[0]:
    continent = st.multiselect('Continent', df.continent.unique())
with pcol[1]:
    country = st.multiselect('Country', df.country.unique())
with pcol[2]:
    years = st.slider('Year Span', 1800, 2022, (1800, 2022), step=10)
with pcol[3]:
    population = st.slider('Population', 1000, max_population, (10000, max_population), step=100000)
with pcol[4]:
    income = st.multiselect('Current Income', df.income_groups.unique())

# Apply filters to dataframe

df = df[(df.year >= years[0]) & (df.year <= years[1])]
df = df[(df.population >= population[0]) & (df.population <= population[1])]
if continent:
    df = df[df.continent.isin(continent)]
if country:
    df = df[df.country.isin(country)]
if income:
    df = df[df.income_groups.isin(income)]

# Plot

fig = px.scatter(df, x='gdpPercap', y='lifeExp', color='region', size='population', size_max=130,
                 hover_name='country', log_x=True, animation_frame='year',
                 animation_group='country', range_x=[300, 130000], range_y=[10, 115],
                 labels=dict(population="Population", gdpPercap="Income per person (GDP/capita, PPP$ inflation-adjusted)", lifeExp="Life Expectancy (Years)"))

fig.update_layout({
    'autosize': False,
    'width': 1200,
    'height': 500,
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'xaxis': dict(showgrid=False),
    'yaxis': dict(showgrid=False),
    'legend': dict(
        title=None,
        yanchor="bottom",
        xanchor="right",
        y=0.1,
        x=1
    )
})

# Make it faster
# fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 130
# fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 5

# Export to html
# fig.write_html("data.html")

st.plotly_chart(fig, use_container_width=True)

st.write("full code can be found [here](https://github.com/justdataplease/wealth-and-health-of-nations).")