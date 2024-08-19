import streamlit as st
from pyspark.sql.functions import col, expr, explode, monotonically_increasing_id, sum, min, max
from pyspark.sql import SparkSession
import pandas as pd
import altair as alt

from pages.Data.data import *

st.set_page_config(page_title="Business Insights", page_icon="🌍", layout="wide")
st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 100px;
    align-items: center;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown("# Business Insights")

@st.cache_resource
def get_data():
    spark = spark_session()
    business_1 = business_data(spark)
    business_categories_result, business_categories, category_mapping = business_category(business_1)
    
    #creating Table views
    business_categories_result.createOrReplaceTempView("business_category_id")
    category_mapping.createOrReplaceTempView("business_category")

    business = spark.sql("""
            SELECT 
                bci.category_id
                , b.business_id
                , b.name
                , b.state
                , b.city
                , b.review_count
                , b.stars
                , b.is_open
                , b.latitude
                , b.longitude
                , bc.category
            FROM business_category_id as bci
            JOIN business as b on bci.business_id = b.business_id
            JOIN business_category as bc on bci.category_id = bc.category_id
            """)
    #Category_Top10
    category_id_T10 = spark.sql("""
                SELECT 
                    bci.category_id
                    , bc.category
                    , COUNT(bci.business_id) AS business_count
                FROM business_category_id as bci
                JOIN business_category as bc on bci.category_id = bc.category_id
                GROUP BY 1,2
                ORDER BY business_count DESC
                LIMIT 20""")
    category_id_T10_pd = category_id_T10.toPandas()

    #TotalBusiness
    total_business = spark.sql("SELECT  COUNT(DISTINCT business_id) as count FROM business").first()['count']

    #List of Categories
    categories_all = spark.sql("""
                SELECT 
                    DISTINCT category as category
                FROM business_category as bc
                GROUP BY 1
                ORDER BY 1 ASC""")

    return spark, business, business_categories_result, business_categories, category_mapping, category_id_T10_pd, total_business, categories_all
    
spark, business, business_categories_result, business_categories, category_mapping, category_id_T10_pd, total_business, categories_all = get_data()


#TotalBusiness
total_business_f = "{:,}".format(total_business)

#List of Categories
categories = categories_all.collect()
categories_row_list = [row['category'] for row in categories]
categories_list = tuple(categories_row_list)

#List of Cities
cities = business.select("city").distinct().collect()
cities_row_list = [row['city'] for row in cities]
cities_list = tuple(cities_row_list)


#List of States
states = business.select("state").distinct().collect()
states_row_list = [row['state'] for row in states]
states_list = tuple(states_row_list)

#min and max review counts
min_max_df = business.agg(
    min("review_count").alias("min_value"),
    max("review_count").alias("max_value")
)
min_reviews, max_reviews = min_max_df.first()

#Resume
col1, col2 = st.columns([4, 2])

with col1:
    st.header("Top 20 Categories with most number of businesses")
    st.write(alt.Chart(category_id_T10_pd).mark_bar().encode(
    x=alt.X('category', sort=None),
    y='business_count',
    ))
    
with col2:
    st.header("Total Number of Businesses")
    st.metric(label="",value=total_business_f)

#Map all
business_pd_all = business.toPandas()
st.map(business_pd_all, latitude = business_pd_all.latitude, longitude = business_pd_all.longitude)


# Control Filters
st.divider()
col3, col4, col5, col6, col7, col8 = st.columns(6)

with col3:
    cat = st.selectbox(
        "Categories",
        categories_list,
        index=None,
        key = "category",
        placeholder = "Please select a Category....")

with col4:
    city = st.selectbox(
        "City",
        cities_list,
        index=None,
        key = "city",
        placeholder = "Please select City....")

with col5:
    state = st.selectbox(
        "State",
        states_list,
        index=None,
        key = "state",
        placeholder = "Please select State....")

with col6:
    star = st.selectbox(
        "Stars",
        (2,3,4,5),
        index=None,
        key = "star",
        placeholder = "Please select ≤ Star....")

with col7:
    values = st.slider(
        'Reviews Between', 
        min_value=min_reviews, 
        max_value=max_reviews, 
        value=(100, 1000),
        key="values")
    min_value = values[0]
    max_value = values[1]

with col8:
    option = st.selectbox(
        "Business Status",
        ("Open","Close"),
        index=None,
        key = "status",
        placeholder = "Please select a Business Status....")
    if option == "Open":
        status = 1
    elif option == "Close":
        status = 0
    else:
        status = option

# Map
st.divider()

if city != None and state != None and cat != None and status != None and star != None:
    business_f = business.filter(business.city == city) \
                     .filter(business.state == state) \
                     .filter(business.category == cat) \
                     .filter(business.is_open == status) \
                     .filter(business.stars <= star) \
                     .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
elif city != None and state == None and cat == None and status == None and star == None:
    business_f = business.filter(business.city == city) \
                         .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
elif city == None and state != None and cat == None and status == None and star == None:
    business_f = business.filter(business.state == state) \
                         .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
elif city == None and state == None and cat != None and status == None and star == None:
    business_f = business.filter(business.category == cat) \
                         .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
elif city == None and state == None and cat == None and status != None and star == None:
    business_f = business.filter(business.is_open == status) \
                         .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
elif city == None and state == None and cat == None and status == None and star != None:
    business_f = business.filter(business.stars <= star) \
                         .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
elif city != None and state != None and cat == None and status == None and star == None:
    business_f = business.filter(business.city == city) \
                         .filter(business.state == state) \
                         .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
elif city != None and state == None and cat != None and status == None and star == None:
    business_f = business.filter(business.city == city) \
                         .filter(business.category == cat) \
                         .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
elif city != None and state == None and cat == None and status != None and star == None:
    business_f = business.filter(business.city == city) \
                         .filter(business.is_open == status) \
                         .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
elif city != None and state == None and cat == None and status == None and star != None:
    business_f = business.filter(business.city == city) \
                         .filter(business.stars <= star) \
                         .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
elif city == None and state != None and cat != None and status == None and star == None:
    business_f = business.filter(business.state == state) \
                         .filter(business.category == cat) \
                         .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
elif city == None and state != None and cat == None and status != None and star == None:
    business_f = business.filter(business.state == state) \
                         .filter(business.is_open == status) \
                         .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
elif city == None and state != None and cat == None and status == None and star != None:
    business_f = business.filter(business.state == state) \
                         .filter(business.stars <= star) \
                         .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
elif city == None and state == None and cat != None and status != None and star == None:
    business_f = business.filter(business.category == cat) \
                         .filter(business.is_open == status) \
                         .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
elif city == None and state == None and cat != None and status == None and star != None:
    business_f = business.filter(business.category == cat) \
                         .filter(business.stars <= star) \
                         .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
elif city == None and state == None and cat == None and status != None and star != None:
    business_f = business.filter(business.is_open == status) \
                         .filter(business.stars <= star) \
                         .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
elif city != None and state != None and cat != None and status == None and star == None:
    business_f = business.filter(business.city == city) \
                         .filter(business.state == state) \
                         .filter(business.category == cat) \
                         .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
elif city != None and state != None and cat == None and status != None and star == None:
    business_f = business.filter(business.city == city) \
                         .filter(business.state == state) \
                         .filter(business.is_open == status) \
                         .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
elif city != None and state != None and cat == None and status == None and star != None:
    business_f = business.filter(business.city == city) \
                         .filter(business.state == state) \
                         .filter(business.stars <= star) \
                         .filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
else:
    business_f = business.filter((business.review_count >= min_value) & (business.review_count <= max_value))
    business_pd = business_f.toPandas()
    
col9, col10 = st.columns(2)
with col9:
    bottom_20 = business_f.orderBy("review_count", ascending=True).limit(20)
    bottom_20_pd = bottom_20.toPandas()
    st.header("Bottom 20 Businesses with the least number of Reviews")
    st.write(alt.Chart(bottom_20_pd).mark_bar().encode(
    x=alt.X('name', sort=None),
    y='review_count',
    ))
with col10:
    top_20 = business_f.orderBy("review_count", ascending=False).limit(20)
    top_20_pd = top_20.toPandas()
    st.header("Top 20 Businesses with the most number of Reviews")
    st.write(alt.Chart(top_20_pd).mark_bar().encode(
    x=alt.X('name', sort=None),
    y='review_count',
    ))

st.dataframe(business_pd)
st.map(business_pd, latitude = business_pd.latitude, longitude = business_pd.longitude)

