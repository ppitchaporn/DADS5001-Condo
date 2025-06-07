import os
from dotenv import load_dotenv
from pathlib import Path
from phi.agent.python import PythonAgent
from phi.file.local.csv import CsvFile
from phi.model.groq import Groq
import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

# Load environment variables
load_dotenv()

# Set up paths
cwd = Path(__file__).parent.resolve()
tmp = cwd.joinpath("tmp")
tmp.mkdir(exist_ok=True, parents=True)
csv_path = "Data_Cleaned_AI.csv"

# Load CSV (read first 1000 rows for speed)
@st.cache_data
def load_csv():
    try:
        return pd.read_csv(csv_path, encoding="utf-8", nrows=1000)
    except UnicodeDecodeError:
        return pd.read_csv(csv_path, encoding="cp874", nrows=1000)

# Rename columns for display
column_display_map = {
    "rent_cd_price": "Price (THB)",
    "rent_cd_bed": "Bedrooms",
    "rent_cd_bath": "Bathrooms",
    "new_condo_name": "Project Name",
    "rent_cd_features_station": "Nearest Station",
    "star": "Review Stars"
}


def translate_th_to_en(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        return text  # fallback


def rename_for_display(df):
    return df.rename(columns=column_display_map)

# Precompute insights
@st.cache_data
def compute_insights(df):
    insights = {
        "max_bedroom_condo": df[df["rent_cd_bed"] == df["rent_cd_bed"].max()],
        "min_price_condo": df[df["rent_cd_price"] == df["rent_cd_price"].min()],
        "closest_to_station": df[df["near_rail_meter"] == df["near_rail_meter"].min()],
        "avg_price": df["rent_cd_price"].mean(),
        "projects": df["new_condo_name"].nunique(),
        "agents": df["rent_cd_agent"].value_counts().to_dict()
    }
    return insights

# Load data and compute metrics
df = load_csv()
insights = compute_insights(df)

# Show preview only for user (not affect agent)
with st.expander("\U0001F4C4 Preview Condo Data (Top 5 Rows)", expanded=False):
    st.dataframe(rename_for_display(df.head()))

# Define alias for description (help LLM understand dataset)
schema_hint = """
This is a dataset of condos in Thailand.
- 'rent_cd_price' is the total price in THB.
- 'rent_cd_bed' means number of bedrooms.
- 'rent_cd_bath' means number of bathrooms.
- 'new_condo_name' refers to the project name.
- 'rent_cd_features_station' is the nearest BTS/MRT station.
- 'rent_cd_features_walk' is walking time to station.
- 'star' is the review star rating.
- 'review_list_all' contains user reviews.
"""

# Set up LLM-powered agent with schema hint
python_agent = PythonAgent(
    model=Groq(id="meta-llama/llama-4-maverick-17b-128e-instruct"),
    base_dir=tmp,
    files=[
        CsvFile(
            path=csv_path,
            description=schema_hint.strip()
        )
    ],
    markdown=True,
    pip_install=True,
    show_tool_calls=False,
)

# Streamlit app UI
def main():
    st.title("Thailand Condo Chatbot \U0001F3D9️")
    st.write("Ask questions about condos in Thailand — pricing, location, reviews, or agent listings.")

    question = st.text_area("Enter your question:", placeholder="e.g., Which condo has the most bedrooms?")

    if st.button("Run Flow"):
        if not question.strip():
            st.error("Please enter a valid question.")
            return

        with st.spinner("Thinking..."):
            try:
                q = question.lower()
                if "most bedrooms" in q:
                    st.dataframe(rename_for_display(insights["max_bedroom_condo"]))
                elif "cheapest" in q:
                    st.dataframe(rename_for_display(insights["min_price_condo"]))
                elif "closest to bts" in q or "closest to station" in q:
                    st.dataframe(rename_for_display(insights["closest_to_station"]))
                elif "average price" in q:
                    st.metric("Average Price (THB)", f"{insights['avg_price']:,.0f}")
                elif "how many projects" in q:
                    st.metric("Total Projects", insights["projects"])
                else:
                    translated_question = translate_th_to_en(question)
                    response = python_agent.run(translated_question)
                    # แปลกลับเป็นภาษาต้นฉบับ ถ้าคำถามเป็นภาษาไทย
                    if any(ch in question for ch in "กขฃฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ"):
                        translated_response = GoogleTranslator(source='en', target='th').translate(response.content)
                        st.markdown(translated_response)
                    else:
                        st.markdown(response.content)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()