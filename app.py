import streamlit as st
import pandas as pd
import duckdb
from pymongo import MongoClient
import os

# ตั้งค่าหน้า
st.set_page_config(
    page_title="Condo Rental Explorer",
    page_icon="🏠",
    layout="wide"
)

# === DuckDB Section ===
def create_duckdb_from_csv():
    try:
        if not os.path.exists("condo.duckdb"):
            df = pd.read_csv("data_cleaned.csv")
            con = duckdb.connect("condo.duckdb")
            con.execute("DROP TABLE IF EXISTS condo")
            con.execute("CREATE TABLE condo AS SELECT * FROM df")
            con.close()
            return "created"
        else:
            return "exists"
    except Exception as e:
        return f"error: {e}"


def create_duckdb_from_sql(sql_file="dads5001db.sql", db_file="condo_sql.duckdb"):
    try:
        if not os.path.exists(db_file):
            # 1️⃣ Connect to DuckDB (จะสร้าง condo.duckdb อัตโนมัติถ้ายังไม่มี)
            con = duckdb.connect(db_file)

            # 2️⃣ Load SQL script
            with open(sql_file, "r", encoding="utf-8") as f:
                sql_script = f.read()

            # 3️⃣ Execute SQL commands (อาจรองรับหลายคำสั่งในไฟล์เดียวได้เลย)
            con.execute(sql_script)

            con.close()
            return "✅ DuckDB created from SQL successfully."
        else:
            return "ℹ️ DuckDB file already exists."
    except Exception as e:
        return f"❌ Error: {e}"


def check_duckdb_connection():
    try:
        con = duckdb.connect("condo.duckdb")
        con.execute("SHOW TABLES").fetchall()
        con.close()
        return True
    except:
        return False


# === MongoDB Section ===
mongo_uri = st.secrets["MONGO_URI"]
def check_mongo_connection(uri=mongo_uri):
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        dbs = client.list_database_names()  # จะ error ถ้าต่อไม่ได้
        return True, dbs
    except Exception as e:
        return False, str(e)

# === Sidebar: Connection Status ===
st.sidebar.header("🔌 Database Connections")

# DuckDB
duck_status = create_duckdb_from_csv()

#create_duckdb_from_sql()

if check_duckdb_connection():
    if duck_status == "created":
        st.sidebar.success("✅ DuckDB created and connected")
    elif duck_status == "exists":
        st.sidebar.info("📦 DuckDB exists and connected")
else:
    st.sidebar.error("❌ Failed to connect to DuckDB")

# MongoDB
mongo_ok, mongo_info = check_mongo_connection()
if mongo_ok:
    st.sidebar.success("✅ MongoDB connected")
    st.sidebar.caption(f"Found databases: {', '.join(mongo_info)}")
else:
    st.sidebar.error("❌ MongoDB connection failed")
    st.sidebar.caption(f"{mongo_info}")

# === Main Welcome Content ===
st.title("🏠 Welcome to Condo Rental Explorer")

st.markdown("""
Explore condo rental prices in Bangkok using interactive analytics and AI tools.

Use the menu on the left to navigate to:

- 📊 Descriptive Analysis  
- 📈 Relationship & Price Prediction  
- 🗺 Geospatial Analysis  
- 🤖 Advanced Search & Comparison  
""")

st.image("https://cdn.pixabay.com/photo/2020/01/15/07/27/condominium-4769185_1280.jpg", use_container_width=True)

st.caption("Built with ❤️ using Streamlit, Plotly, DuckDB & MongoDB")
