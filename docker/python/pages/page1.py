import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, URL, MetaData, Table
import mysql.connector
import toml
from pymongo import MongoClient
import duckdb

st.set_page_config(initial_sidebar_state="collapsed")

## Connection
engine = create_engine("mysql+mysqlconnector://root:admin@localhost:3306/dads5001db")
client = MongoClient("mongodb://root:admin@localhost:27017/?authSource=admin")
# Load into DuckDB
duck_con = duckdb.connect()

## main page func
def main_page():
    st.markdown("## Connect to MySQL with duckdb ")
    st.markdown("### Unclean data ")
    df1 = pd.read_sql(f'SELECT * FROM unclean_data', con=engine)

    # Register the DataFrame as a DuckDB table
    duck_con.register('unclean_data', df1)
    result = duck_con.execute("SELECT * FROM unclean_data").df()
    st.write(result)

    st.markdown("### Clean data ")
    df1 = pd.read_sql(f'SELECT * FROM clean_data', con=engine)

    # Register the DataFrame as a DuckDB table
    duck_con.register('clean_data', df1)
    result = duck_con.execute("SELECT * FROM clean_data").df()
    st.write(result)
    
    st.markdown("## Connect to Mongodb ")
    db = client.dads5001db
    st.write(db.list_collection_names())

## page
home_page = st.Page(main_page,title='Home page', icon=":material/home:")
descipt = st.Page("page2.py", title='Descriptive Analysis', icon=":material/database:")
relation_predict = st.Page("page3.py", title='Relationship Analysis & Price Prediction', icon=":material/bar_chart:")
geospatial_class = st.Page("page4.py", title='Geospatial Analysis & Classification Result', icon=":material/bar_chart:")
Ai_search = st.Page("page5.py", title=' Advanced Search & Comparison', icon=":material/note:")

## create menu tree
pg = st.navigation(
    {
        "Menu": [home_page, descipt, relation_predict, geospatial_class, Ai_search],

    }
)
pg.run()