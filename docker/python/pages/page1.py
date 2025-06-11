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
def rating_to_stars(rating, max_stars=5):
    # ตรวจสอบให้แน่ใจว่า rating ไม่เป็น NaN ก่อนทำการแปลง
    if pd.isna(rating):
        return "N/A" # หรือ "☆☆☆☆☆"
    full_stars = "⭐" * int(rating)
    empty_stars = "☆" * (max_stars - int(rating))
    return full_stars + empty_stars

def main_page():
    st.title("Smart Rent BKK")
    st.text("ทำความเข้าใจตลาดเช่าคอนโดกรุงเทพฯ ที่ไม่หยุดนิ่ง! รายงานนี้สรุปภาพรวมราคาในแต่ละพื้นที่ ปัจจัยที่ส่งผลต่อค่าเช่า และการพยากรณ์ราคา พร้อมการเปรียบเทียบเชิงลึก และแนะนำการใช้ AI สุดล้ำเพื่อช่วยคุณค้นหาห้องเช่าที่ใช่ได้อย่างรวดเร็วและแม่นยำ ไม่ว่าจะเป็นการลงทุนหรือหาที่พักอาศัย นี่คือข้อมูลที่คุณต้องรู้!")
    st.image("https://raw.githubusercontent.com/ppitchaporn/DADS5001-Condo/a785a69fe796a14d3023d993a8c89289c4bd067a/Condo_image.jpg")
    st.header("All Condomunium List")
    st.markdown("(Connect via MySQL with duckdb)")
    df1 = pd.read_sql(f"""SELECT rent_cd_id ID,
                      new_condo_name "Condo Name",
                      rent_cd_address Address,
                      FORMAT(rent_cd_price,0) "Rental Price (Baht)",
                      rent_cd_bed "#Bed",
                      rent_cd_bath "#Baht",
                      rent_cd_features_station "Rail Station",
                      FORMAT(near_rail_meter, 0) "Distance from rails (Meters)",
                      rent_cd_features_time "Time to rails (Minutes)",
                      cast(star AS Decimal(6,1)) star
                      
                      FROM unclean_data
                      WHERE rent_cd_price < 1000000""", con=engine)

    # Register the DataFrame as a DuckDB table
    duck_con.register('unclean_data', df1)
    result = duck_con.execute("SELECT * FROM unclean_data").df()

    df_display = result.copy()
    df_display['Rating'] = df_display['star'].apply(rating_to_stars)
    
    st.dataframe(
            df_display,
            column_config={
                "Rating": st.column_config.Column(
                    "Rating",
                    help="คะแนนรีวิว",
                    width="small"
                ),
                # Hide Star Column
                "star": None
            },
            column_order=[
                "Condo Name",
                "Rating",
                "Address",
                "Rental Price (Baht)",
                "#Bed",
                "#Bath",
                "Rail Station",
                "Distance from rails (Meters)",
                "Time to rails (Minutes)"
            ],
            hide_index=True
        )
    # st.write(df_display)

    # st.markdown("### Clean data ")
    # df1 = pd.read_sql(f'SELECT * FROM clean_data', con=engine)

    # Register the DataFrame as a DuckDB table
    # duck_con.register('clean_data', df1)
    # result = duck_con.execute("SELECT * FROM clean_data").df()
    # st.write(result)
    
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
