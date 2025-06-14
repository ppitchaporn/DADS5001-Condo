import streamlit as st

# MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Advanced Search & Comparison", layout="wide")

# THEN imports or other Streamlit code
import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
from phi.agent.python import PythonAgent
from phi.model.groq import Groq
from tabulate import tabulate

# --- Load environment variables ---
load_dotenv()

# Set TMP_DIR to the correct directory
BASE_DIR = Path(__file__).parent.resolve()
TMP_DIR = BASE_DIR / "tmp"
TMP_DIR.mkdir(exist_ok=True, parents=True)

COMPARE_PATH = TMP_DIR / "compare.csv"

# --- Load CSV from GitHub raw URL ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/ppitchaporn/DADS5001-Condo/main/Data_Cleaned_AI.csv"
    try:
        return pd.read_csv(url, encoding="utf-8", nrows=1000)
    except:
        return pd.read_csv(url, encoding="cp874", nrows=1000)

df = load_data()

# --- Rename columns for display ---
DISPLAY_COLUMNS = {
    "rent_cd_price": "Price (THB)",
    "rent_cd_bed": "Bedrooms",
    "rent_cd_bath": "Bathrooms",
    "new_condo_name": "Project Name",
    "rent_cd_features_station": "Nearest Station",
    "star": "Review Stars"
}
def rename_columns(df):
    return df.rename(columns=DISPLAY_COLUMNS)

# --- Summary insights ---
@st.cache_data
def summarize_data(df):
    return {
        "max_bedroom": df[df["rent_cd_bed"] == df["rent_cd_bed"].max()],
        "min_price": df[df["rent_cd_price"] == df["rent_cd_price"].min()],
        "avg_price": df["rent_cd_price"].mean(),
        "total_projects": df["new_condo_name"].nunique()
    }

insights = summarize_data(df)

# --- Price bin generator ---
def generate_price_bins(df, column="rent_cd_price", step=5000):
    min_price = int(df[column].min())
    max_price = int(df[column].max())
    bins = list(range(min_price, max_price + step, step))
    return {
        f"{bins[i]:,}–{bins[i+1]-1:,}": (bins[i], bins[i+1] - 1)
        for i in range(len(bins) - 1)
    }

# --- Markdown table generator ---
def generate_markdown_table(df):
    df = df.rename(columns={
        "new_condo_name": "โครงการ",
        "price": "ราคา (บาท)",
        "bedrooms": "ห้องนอน",
        "bathrooms": "ห้องน้ำ"
    })
    min_price = df["ราคา (บาท)"].min()
    max_bed = df["ห้องนอน"].max()

    df["ข้อได้เปรียบหลัก"] = df.apply(lambda row:
        "ราคาถูกที่สุด" if row["ราคา (บาท)"] == min_price else
        "มีห้องนอนมากที่สุด" if row["ห้องนอน"] == max_bed else "-", axis=1)

    return tabulate(df, headers="keys", tablefmt="github")

# --- New: Run LLM chatbot using real CSV data directly ---
def run_chatbot_with_data(question, data_df):
    try:
        agent = PythonAgent(
            model=Groq(id="meta-llama/llama-4-maverick-17b-128e-instruct"),
            markdown=True
        )

        # เลือกเฉพาะ column ที่ใช้ได้ดีในคำถามทั่วไป
        table_text = data_df[[
            "new_condo_name", "rent_cd_price", "rent_cd_bed",
            "rent_cd_bath", "rent_cd_features_station"
        ]].head(50).to_markdown(index=False)

        # Prompt ใหม่ที่สั่งให้ "ห้ามเขียนโค้ด" และ "ตอบเหมือนมนุษย์"
        prompt = f"""
You are a real estate expert in Thailand.

Below is a table of condo listings with their name, price, bedrooms, bathrooms, and nearest station.

{table_text}

Please answer the following question based only on this data.

⚠️ Do not write code. Just explain your answer clearly like a human expert.  
Use natural Thai or English depending on the question.

Question: {question}
"""
        return agent.run(prompt).content
    except Exception as e:
        return f"❌ Chatbot error: {e}"


# --- Streamlit App ---
def page5():
    st.markdown("# 🏢 Advanced Search & Comparison")

    # --- Chatbot ---
    show_chatbot = st.toggle("🧠 Enable Chatbot", value=True)
    if show_chatbot:
        st.subheader("Thailand Condo Chatbot")
        question = st.text_area("Enter your question:", placeholder="เช่น คอนโดที่ใกล้ BTS ที่สุดคือที่ไหน")
        if st.button("Run Flow"):
            if not question.strip():
                st.error("Please enter a valid question.")
            else:
                with st.spinner("Thinking..."):
                    q = question.lower()
                    if "most bedrooms" in q or "ห้องนอนมากที่สุด" in q:
                        st.dataframe(rename_columns(insights["max_bedroom"]))
                    elif "cheapest" in q or "ราคาถูกที่สุด" in q:
                        st.dataframe(rename_columns(insights["min_price"]))
                    elif "average price" in q or "ราคาเฉลี่ย" in q:
                        st.metric("Average Price (THB)", f"{insights['avg_price']:,.0f}")
                    elif "how many projects" in q or "มีกี่โครงการ" in q:
                        st.metric("Total Projects", insights["total_projects"])
                    else:
                        response = run_chatbot_with_data(question, df)
                        st.markdown(response)

    # --- Filter Section ---
    st.header("🔍 Advanced Search & Filters")
    price_bins = generate_price_bins(df)

    col1, col2 = st.columns(2)
    with col1:
        station_options = st.multiselect("Nearest Station", sorted(df["rent_cd_features_station"].dropna().unique()))
        project_options = st.multiselect("Project Name", sorted(df["new_condo_name"].dropna().unique()))
    with col2:
        price_selection = st.multiselect("Price Range (THB)", list(price_bins.keys()))
        bedroom_options = st.multiselect("Bedrooms", sorted(df["rent_cd_bed"].dropna().unique()))

    filtered_df = df.copy()
    if station_options:
        filtered_df = filtered_df[filtered_df["rent_cd_features_station"].isin(station_options)]
    if project_options:
        filtered_df = filtered_df[filtered_df["new_condo_name"].isin(project_options)]
    if price_selection:
        mask = pd.Series(False, index=filtered_df.index)
        for label in price_selection:
            low, high = price_bins[label]
            mask |= filtered_df["rent_cd_price"].between(low, high)
        filtered_df = filtered_df[mask]
    if bedroom_options:
        filtered_df = filtered_df[filtered_df["rent_cd_bed"].isin(bedroom_options)]

    st.subheader("🎯 Filtered Condo Results")
    st.dataframe(rename_columns(filtered_df))

    # --- Compare ---
    if not filtered_df.empty and st.button("Compare with LLM"):
        top10 = filtered_df.head(10).copy()
        top10 = top10.rename(columns={
            "rent_cd_price": "price",
            "rent_cd_bed": "bedrooms",
            "rent_cd_bath": "bathrooms"
        })
        top10 = top10[["new_condo_name", "price", "bedrooms", "bathrooms"]]
        top10.to_csv(COMPARE_PATH, index=False)

        st.info("Generating markdown table using LLM...")
        try:
            markdown = generate_markdown_table(top10)
            st.markdown(markdown)
        except Exception as e:
            st.error(f"❌ Table generation failed: {str(e)}")


page5()

# --------------------------
# 🧭 Navigation
# --------------------------
#home_page = st.Page("page1.py", title="Home Page", icon=":material/home:")
#desc_page = st.Page("page2.py", title="Descriptive Analysis", icon=":material/database:")
#relation_page = st.Page("page3.py", title="Relationship Analysis & Prediction", icon=":material/bar_chart:")
#geo_page = st.Page("page4.py", title="Condo Map Insights & Classification", icon=":material/map:")
#ai_page = st.Page(page5, title="Advanced Search & Comparison", icon=":material/compare:")

#pg = st.navigation({
#    "Menu": [home_page, desc_page, relation_page, geo_page, ai_page],
#})
#pg.run()
