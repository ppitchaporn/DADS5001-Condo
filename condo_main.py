import pandas as pd
import streamlit as st
import plotly.express as px
from pymongo import MongoClient
import duckdb
import os

# ฟังก์ชันสร้าง DuckDB จาก CSV (เรียกครั้งเดียว)
def create_duckdb_from_csv():
    if not os.path.exists("condo.duckdb"):
        df = pd.read_csv("data_cleaned.csv")
        con = duckdb.connect("condo.duckdb")
        con.execute("DROP TABLE IF EXISTS condo")
        con.execute("CREATE TABLE condo AS SELECT * FROM df")
        con.close()
        print("DuckDB database created from CSV")
    else:
        print("DuckDB database already exists")


# ใช้ cache สำหรับโหลดข้อมูล
@st.cache_data
def load_data():
    con = duckdb.connect("condo.duckdb")
    df = con.execute("SELECT * FROM condo").df()
    con.close()
    return df

def main():
    st.set_page_config(page_title='Condo Rental Explorer', layout='wide')
    create_duckdb_from_csv()  # เรียกฟังก์ชันสร้าง DB
    df = load_data()

    st.write(f"Loaded {len(df):,} rows from DuckDB")
    st.dataframe(df.head())

if __name__ == '__main__':
    main()
