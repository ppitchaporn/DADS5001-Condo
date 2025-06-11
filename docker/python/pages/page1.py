import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, URL, MetaData, Table
import mysql.connector
import toml
from pymongo import MongoClient
import duckdb

# st.set_page_config()

## Connection
engine = create_engine("mysql+mysqlconnector://admin:admin@localhost:3306/dads5001db")
client = MongoClient("mongodb://root:admin@localhost:27017/?authSource=admin")
# Load into DuckDB
duck_con = duckdb.connect()

## main page func
def rating_to_stars(rating, max_stars=5):
    # ตรวจสอบให้แน่ใจว่า rating ไม่เป็น NaN ก่อนทำการแปลง
    if pd.isna(rating):
        return "N/A" # หรือ "☆☆☆☆☆"
    integer_part = int(rating)
    decimal_part = rating - integer_part

    full_stars = "⭐" * integer_part
    half_star = "½" if decimal_part >= 0.5 else ""
    empty_stars = "☆" * (max_stars - integer_part - (1 if decimal_part >= 0.5 else 0))

    return full_stars + half_star + empty_stars

def convert_for_download(df):
    return df.to_csv(index=False).encode("utf-8")

def main_page():
    st.title("Smart Rent BKK 🌆")
    st.text("ทำความเข้าใจตลาดเช่าคอนโดกรุงเทพฯ ที่ไม่หยุดนิ่ง! รายงานนี้สรุปภาพรวมราคาในแต่ละพื้นที่ ปัจจัยที่ส่งผลต่อค่าเช่า และการพยากรณ์ราคา พร้อมการเปรียบเทียบเชิงลึก และแนะนำการใช้ AI สุดล้ำเพื่อช่วยคุณค้นหาห้องเช่าที่ใช่ได้อย่างรวดเร็วและแม่นยำ ไม่ว่าจะเป็นการลงทุนหรือหาที่พักอาศัย นี่คือข้อมูลที่คุณต้องรู้!")
    st.image("https://raw.githubusercontent.com/ppitchaporn/DADS5001-Condo/a785a69fe796a14d3023d993a8c89289c4bd067a/Condo_image.jpg")
    st.header("Data Viewer")
    st.caption("(Connect via MySQL with DuckDb)")

    options = [5, 10, 25, 50, 100, "All"]
    selection_rows = st.pills("Select Top Rows:", options, selection_mode="single", default=5)
    st.markdown(f"Displaying {selection_rows} rows.")

    sql_base_query = (f"""SELECT a.rent_cd_id ID,
                      a.new_condo_name "Condo Name",
                      a.rent_cd_address Address,
                      FORMAT(a.rent_cd_price,0) "Rental Price (Baht)",
                      COALESCE(a.rent_cd_bed, b.rent_cd_bed) "#Bed",
                      COALESCE(a.rent_cd_bath, b.rent_cd_bath) "#Baht",
                      COALESCE(a.rent_cd_features_station) "Rail Station",
                      FORMAT(COALESCE(a.near_rail_meter, b.near_rail_meter),0) "Distance from rails (Meters)",
                      COALESCE(a.rent_cd_features_time, b.rent_cd_features_time) "Time to rails (Minutes)",
                      cast(a.star AS Decimal(6,1)) star
                      
                      FROM unclean_data a
					  
					  LEFT JOIN clean_data b
                      ON a.rent_cd_id = b.id
                      WHERE a.rent_cd_price < 1000000""")
    
    # Condition to limit display
    final_sql_query = sql_base_query

    if selection_rows != "All":
        final_sql_query += f" LIMIT {selection_rows}"

    df1 = pd.read_sql(final_sql_query, con=engine)

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
    
    # CSV Busston
    csv = convert_for_download(df1)
    st.download_button(
    label="Download CSV",
    data=csv,
    file_name="data.csv",
    mime="text/csv",
    icon=":material/download:",)

    # --- Footer Section ---
    st.markdown("---") # Optional: Add a horizontal line to separate content from footer

    # You can use st.write, st.markdown, st.caption, st.info, etc.
    st.write("### About Our Team")
    st.write("This project is part of DADS5001 - Data Analytics and Data Science Tools.")
    # st.markdown("For more information, visit our [website](https://www.example.com).")

    # You can also use columns for a more structured footer
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Name")
        st.write("Mr.Kitisak Namtae")
        st.write("Mr.Kantapong Charusiri")
        st.write("Miss Pitchaporn Nimdum")
        st.write("Miss Pornchanok Tuntikulwattanakit")
        st.write("Mr.Suparerk Jankam ")
    with col2:
        st.subheader("ID")
        st.write("6710422007")
        st.write("6710422015")
        st.write("6710422016")
        st.write("6710422023")
        st.write("6710422028")

    st.subheader("Rate Us")
    sentiment_mapping = ["one", "two", "three", "four", "five"]
    selected = st.feedback("stars")
    if selected is not None:
        st.markdown(f"You selected {sentiment_mapping[selected]} star(s). \n Thank You. 😊")
    # st.write(df_display)

    # st.markdown("### Clean data ")
    # df2 = pd.read_sql(f'SELECT * FROM clean_data', con=engine)
    # st.write(df2)
    # Register the DataFrame as a DuckDB table
    # duck_con.register('clean_data', df2)
    # result = duck_con.execute("SELECT * FROM clean_data").df()
    # st.write(result)
    
    # st.markdown("## Connect to Mongodb ")
    # db = client.dads5001db
    # st.write(db.list_collection_names())

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
