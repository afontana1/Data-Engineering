import streamlit as st
from pyspark.sql.functions import col, expr, explode, monotonically_increasing_id, sum, min, max, count, countDistinct, to_date, unix_timestamp, to_timestamp, date_format
from pyspark.sql import SparkSession
import pandas as pd
import altair as alt

from pages.Data.data import *

st.set_page_config(page_title="Target Ads", page_icon="📊", layout="wide")
st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 100px;
    align-items: center;
    justify-content: center;
    width: fit-content;
    margin: auto;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown("# User-Target Ads")

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

    #TotalUsers
    total_users = spark.sql("SELECT  COUNT(DISTINCT user_id) as count FROM user").first()['count']

    #List of Categories
    categories_all = spark.sql("""
                SELECT 
                    DISTINCT category as category
                FROM business_category as bc
                GROUP BY 1
                ORDER BY 1 ASC""")

    #User-Reviews
    users_cat = spark.sql("""
            SELECT 
                u.user_id
                , u.name as user_name
                , b.name as business_name
                , r.review_id
                , r.date as review_date
                , r.stars
                , b.state
                , b.city
                , b.latitude
                , b.longitude
                , bc.category
                , b.is_open
            FROM user as u
            JOIN review as r on u.user_id = r.user_id
            JOIN business as b on r.business_id = b.business_id
            JOIN business_category_id as bci on bci.business_id = b.business_id
            JOIN business_category as bc on bci.category_id = bc.category_id
            """)

    #Review Timeline
    date_review = users_cat.withColumn('review_date', to_date(unix_timestamp('review_date', 'yyyy-MM-dd HH:mm:ss').cast('timestamp')))
    date_review_f = date_review.withColumn("month_year", date_format("review_date", "yyyy-MM"))
    date_review_m = date_review_f.groupBy("month_year").agg(countDistinct("review_id").alias("review_count")).orderBy("month_year", ascending=True)

    return spark, business, total_users, categories_all, users_cat, date_review_m
    
spark, business, total_users, categories_all, users_cat, date_review_m = get_data()

#TotalUsers
total_users_f = "{:,}".format(total_users)

#List of Categories
categories = categories_all.collect()
categories_row_list = [row['category'] for row in categories]
if "restaurants" in categories_row_list:
    categories_row_list.remove("restaurants")  
    categories_row_list.insert(0, "restaurants")  
categories_list = tuple(categories_row_list)

#List of Cities
cities = business.select("city").distinct().collect()
cities_row_list = [row['city'] for row in cities]
cities_list = tuple(cities_row_list)

#List of States
states = business.select("state").distinct().collect()
states_row_list = [row['state'] for row in states]
states_list = tuple(states_row_list)


col6, col7 = st.columns(2)
with col6:
    st.header("Total Number of Users")
    st.metric(label="",value=total_users_f)

with col7:
    st.header("Number of User Reviews per Date")
    st.line_chart(date_review_m, x="month_year", y="review_count")

# Control Filters
st.divider()
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    cat = st.selectbox(
        "Categories",
        categories_list,
        index=0,
        key = "category",
        placeholder = "Please select a Category....")

with col2:
    city = st.selectbox(
        "City",
        cities_list,
        index=None,
        key = "city",
        placeholder = "Please select City....")

with col3:
    state = st.selectbox(
        "State",
        states_list,
        index=None,
        key = "state",
        placeholder = "Please select State....")

with col4:
    star = st.selectbox(
        "Stars",
        (2,3,4,5),
        index=3,
        key = "star",
        placeholder = "Please select ≥ Star....")

with col5:
    option = st.selectbox(
        "Business Status",
        ("Open","Close"),
        index=0,
        key = "status",
        placeholder = "Please select a Business Status....")
    if option == "Open":
        status = 1
    elif option == "Close":
        status = 0
    else:
        status = option
        
#applying filters
st.divider()

if city != None and state != None and cat != None and status != None and star != None:
    users_cat_f = users_cat.filter(users_cat.city == city) \
                     .filter(users_cat.state == state) \
                     .filter(users_cat.category == cat) \
                     .filter(users_cat.is_open == status) \
                     .filter(users_cat.stars >= star)
elif city != None and state == None and cat == None and status == None and star == None:
    users_cat_f = users_cat.filter(users_cat.city == city)
elif city == None and state != None and cat == None and status == None and star == None:
    users_cat_f = users_cat.filter(users_cat.state == state)
elif city == None and state == None and cat != None and status == None and star == None:
    users_cat_f = users_cat.filter(users_cat.category == cat)
elif city == None and state == None and cat == None and status != None and star == None:
    users_cat_f = users_cat.filter(users_cat.is_open == status)
elif city == None and state == None and cat == None and status == None and star != None:
    users_cat_f = users_cat.filter(users_cat.stars >= star)
elif city != None and state != None and cat == None and status == None and star == None:
    users_cat_f = users_cat.filter(users_cat.city == city) \
                         .filter(users_cat.state == state)
elif city != None and state == None and cat != None and status == None and star == None:
    users_cat_f = users_cat.filter(users_cat.city == city) \
                         .filter(users_cat.category == cat)
elif city != None and state == None and cat == None and status != None and star == None:
    users_cat_f = users_cat.filter(users_cat.city == city) \
                         .filter(users_cat.is_open == status)
elif city != None and state == None and cat == None and status == None and star != None:
    users_cat_f = users_cat.filter(users_cat.city == city) \
                         .filter(users_cat.stars >= star)
elif city == None and state != None and cat != None and status == None and star == None:
    users_cat_f = users_cat.filter(users_cat.state == state) \
                         .filter(users_cat.category == cat)
elif city == None and state != None and cat == None and status != None and star == None:
    users_cat_f = users_cat.filter(users_cat.state == state) \
                         .filter(users_cat.is_open == status)
elif city == None and state != None and cat == None and status == None and star != None:
    users_cat_f = users_cat.filter(users_cat.state == state) \
                         .filter(users_cat.stars >= star)
elif city == None and state == None and cat != None and status != None and star == None:
    users_cat_f = users_cat.filter(users_cat.category == cat) \
                         .filter(users_cat.is_open == status)
elif city == None and state == None and cat != None and status == None and star != None:
    users_cat_f = users_cat.filter(users_cat.category == cat) \
                         .filter(users_cat.stars >= star)
elif city == None and state == None and cat == None and status != None and star != None:
    users_cat_f = users_cat.filter(users_cat.is_open == status) \
                         .filter(users_cat.stars >= star)
elif city != None and state != None and cat != None and status == None and star == None:
    users_cat_f = users_cat.filter(users_cat.city == city) \
                         .filter(users_cat.state == state) \
                         .filter(users_cat.category == cat)
elif city != None and state != None and cat == None and status != None and star == None:
    users_cat_f = users_cat.filter(users_cat.city == city) \
                         .filter(users_cat.state == state) \
                         .filter(users_cat.is_open == status)
elif city != None and state != None and cat == None and status == None and star != None:
    users_cat_f = users_cat.filter(users_cat.city == city) \
                         .filter(users_cat.state == state) \
                         .filter(users_cat.stars >= star)
elif city == None and state == None and cat != None and status != None and star != None:
    users_cat_f = users_cat.filter(users_cat.category == cat) \
                         .filter(users_cat.is_open == status) \
                         .filter(users_cat.stars >= star)
elif city == None and state != None and cat != None and status != None and star != None:
    users_cat_f = users_cat.filter(users_cat.category == cat) \
                         .filter(users_cat.state == state) \
                         .filter(users_cat.is_open == status) \
                         .filter(users_cat.stars >= star)
else:
    users_cat_f = users_cat

col6, col7 = st.columns(2)

with col6:
    users_cat_f_20 = users_cat_f.groupBy("user_name").agg(countDistinct("review_id").alias("review_count")).orderBy("review_count", ascending=False).limit(20)
    top_20_pd = users_cat_f_20.toPandas()
    st.header("Top 20 Users with the most number of Reviews")
    st.write(alt.Chart(top_20_pd).mark_bar().encode(
    x=alt.X('user_name', sort=None),
    y='review_count',
    ))

with col7:
    st.map(users_cat_f, latitude = users_cat_f.latitude, longitude = users_cat_f.longitude)

st.divider()
st.dataframe(users_cat_f)