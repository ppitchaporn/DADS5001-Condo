import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
import numpy as np


# --------------------------
# 🔧 Config
# --------------------------
#st.set_page_config(page_title="Bangkok Condo Insights", layout="wide")

# --------------------------
# 🗺️ Page 4 - Map & Decision Tree Classification
# --------------------------
def page4():
    st.title("🏙️ Bangkok Condo Map & Price Classification")
# --------------------------
# 🔄 Load Data
# --------------------------
    @st.cache_data
    def load_data():
        url = 'https://raw.githubusercontent.com/ppitchaporn/DADS5001-Condo/refs/heads/main/data_cleaned.csv'
        df = pd.read_csv(url)
        df['rent_cd_price'] = df['rent_cd_price'].astype(str).str.replace(',', '', regex=False).astype(float)
        df.dropna(subset=['latitude', 'longitude'], inplace=True)
        df = df[df['rent_cd_price'] <= 1000000] 
        df['rate_type'] = df['rent_cd_price'].apply(lambda x: 0 if x < 10000 else (1 if x < 20000 else 2))
        return df

    df = load_data()

    # --------------------------
    # Classification Map (based on rate_type)
    # --------------------------
    st.markdown("### 🗺️ Condo Classification Map by Rental Price")

    st.markdown(""" 
        🟧 **Low**: Rental price < 10,000 THB  
        🟩 **Medium**: Rental price between 10,000–19,999 THB  
        🟪 **High**: Rental price ≥ 20,000 THB  
        
        """)
    
    # Map rate_type to label
    rate_label_map = {0: "Low", 1: "Medium", 2: "High"}
    df['rate_label'] = df['rate_type'].map(rate_label_map)

    selected_class = st.multiselect(
        "Filter by Price Class",
        options=["Low", "Medium", "High"],
        default=["Low", "Medium", "High"]
    )

    df = df[df['rate_label'].isin(selected_class)].copy()

    # Map rate_type to label
    rate_label_map = {0: "Low", 1: "Medium", 2: "High"}
    df['rate_label'] = df['rate_type'].map(rate_label_map)

    # Assign actual icon URLs (replace these with your preferred icons if needed)
    icon_url_map = {
        "Low": "https://cdn-icons-png.flaticon.com/128/5111/5111178.png",       # Orange
        "Medium": "https://cdn-icons-png.flaticon.com/128/8838/8838901.png",    # Green 
        "High": "https://cdn-icons-png.flaticon.com/128/16740/16740174.png",      # Purple
    }


    # Create icon column for each row
    df['icon_data'] = df['rate_label'].apply(lambda x: {
        "url": icon_url_map[x],
        "width": 128,
        "height": 128,
        "anchorY": 128
    })

    # Apply slight jitter for overlapping icons
    df['latitude'] = df['latitude'] + np.random.uniform(-0.0001, 0.0001, size=len(df))
    df['longitude'] = df['longitude'] + np.random.uniform(-0.0001, 0.0001, size=len(df))

    # Create the icon layer
    icon_layer = pdk.Layer(
        "IconLayer",
        data=df,
        get_icon="icon_data",
        get_position='[longitude, latitude]',
        get_size=4,
        size_scale=15,
        pickable=True,
    )

    # Setup map view
    view_state_classified = pdk.ViewState(latitude=13.75, longitude=100.52, zoom=11)

    # Render map
    st.pydeck_chart(
        pdk.Deck(
            layers=[icon_layer],
            initial_view_state=view_state_classified,
            tooltip={"text": "🏢 {new_condo_name}\n💰 Price: {rent_cd_price} THB\n🎯 Class: {rate_label}"}
        )
    )

    # --------------------------
    # Condo Map
    # --------------------------
    df = load_data()
    grouped = (
        df.groupby(['new_condo_name', 'latitude', 'longitude'], as_index=False)
        .agg({
            'rent_cd_price': ['min', 'max', 'mean'],
            'rent_cd_bed': 'max',
            'rent_cd_bath': 'max',
            'rent_cd_floorarea': ['min', 'max', 'mean'],
            'star': 'mean',
            'near_rail_meter': 'min'
        })
    )

    grouped.columns = ['Condo Name', 'Latitude', 'Longitude', 'Min Price', 'Max Price', 'Avg Price',
                    'Bedrooms', 'Bathrooms', 'Min Area', 'Max Area', 'Avg Area', 'Avg Rating', 'MRT Distance']
    
    grouped['Avg Area'] = grouped['Avg Area'].round()
    grouped['Min Area'] = grouped['Min Area'].round()
    grouped['Max Area'] = grouped['Max Area'].round()

    st.markdown("#### 🔍 Filter Condos")
    bedroom = st.selectbox("Number of Bedrooms", sorted(grouped['Bedrooms'].dropna().unique()))
    bathroom = st.selectbox("Number of Bathrooms", sorted(grouped['Bathrooms'].dropna().unique()))

    st.markdown("#### 💰 Price Range (THB)")
    min_price = st.number_input("Minimum Price", min_value=int(grouped['Min Price'].min()), value=10000, step=1000)
    max_price = st.number_input("Maximum Price", min_value=int(min_price), max_value=int(grouped['Max Price'].max()), value=30000, step=1000)

    st.markdown("#### 📐 Floor Area Range (m²)")
    min_area = st.number_input("Minimum Area", value=25, step=5)
    max_area = st.number_input("Maximum Area", value=80, step=5)

    st.markdown("#### ⭐ Rating")
    rating = st.slider("Minimum Rating", 3.5, 5.0, 4.0, step=0.1)

    filtered = grouped[
        (grouped['Bedrooms'] == bedroom) &
        (grouped['Bathrooms'] == bathroom) &
        (grouped['Avg Price'] >= min_price) &
        (grouped['Avg Price'] <= max_price) &
        (grouped['Avg Rating'] >= rating) &
        (grouped['Avg Area'] >= min_area) &
        (grouped['Avg Area'] <= max_area)
    ].copy()

    st.success(f"Found {len(filtered)} condos matching your filters.")

    filtered['tooltip'] = (
        "🏢 " + filtered['Condo Name'] + "<br>" +
        "💰 Avg Price: " + filtered['Avg Price'].astype(int).astype(str) + " THB<br>" +
        "🛏️ Bed: " + filtered['Bedrooms'].astype(str) +
        ", 🛁 Bath: " + filtered['Bathrooms'].astype(str) + "<br>" +
        "⭐ Rating: " + filtered['Avg Rating'].round(1).astype(str) + "<br>" +
        "🚆 MRT Distance: " + filtered['MRT Distance'].fillna(-1).apply(lambda x: f"{int(x)} m" if x >= 0 else "N/A")
    )

    filtered['icon_data'] = [{
        "url": "https://cdn-icons-png.flaticon.com/512/684/684908.png",
        "width": 128,
        "height": 128,
        "anchorY": 128
    }] * len(filtered)

    layer = pdk.Layer(
        "IconLayer",
        data=filtered,
        get_position='[Longitude, Latitude]',
        get_icon='icon_data',
        get_size=4,
        size_scale=15,
        pickable=True,
        auto_highlight=True
    )
    view_state = pdk.ViewState(latitude=13.75, longitude=100.52, zoom=11)
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/streets-v11',
        tooltip={"html": "{tooltip}", "style": {"backgroundColor": "white", "color": "black"}}
    )
    st.pydeck_chart(r)

    # Table of all results
    if st.checkbox("Show condo data table"):
        st.dataframe(
            filtered[[
                'Condo Name', 'Avg Price', 'Min Price', 'Max Price',
                'Bedrooms', 'Bathrooms', 'Min Area', 'Max Area', 'Avg Rating', 'MRT Distance'
            ]].rename(columns={
                'Avg Price': 'Avg Price (THB)',
                'Min Price': 'Min Price (THB)',
                'Max Price': 'Max Price (THB)',
                'Min Area' : 'Min Area',
                'Max Area' : 'Max Area',
                'Avg Rating': 'Rating',
                'MRT Distance': 'Distance to MRT/BTS'
            }),
            use_container_width=True
        )

    filtered_df = df[
        (df['rent_cd_bed'] == bedroom) &
        (df['rent_cd_price'] >= min_price) &
        (df['rent_cd_price'] <= max_price) &
        (df['star'] >= rating)
    ].copy()

    selected_condo = st.selectbox("📌 Select a Condo to View All Listings", filtered_df['new_condo_name'].dropna().unique())
    condo_details_df = filtered_df[filtered_df['new_condo_name'] == selected_condo]

    st.dataframe(condo_details_df[[
        'new_condo_name', 'rent_cd_price', 'rent_cd_bed', 'rent_cd_bath',
        'rent_cd_floorarea', 'star', 'rent_cd_agent', 'rent_cd_tel'
    ]].rename(columns={
        'new_condo_name': 'Condo Name',
        'rent_cd_price': 'Price (THB)',
        'rent_cd_bed': 'Bedrooms',
        'rent_cd_bath': 'Bathrooms',
        'rent_cd_floorarea': 'Area',
        'star': 'Rating',
        'rent_cd_agent': 'Agent',
        'rent_cd_tel': 'Tel'
    }), use_container_width=True)

# --------------------------
# 🧭 Navigation
# --------------------------
home_page = st.Page("page1.py", title="Home Page", icon=":material/home:")
desc_page = st.Page("page2.py", title="Descriptive Analysis", icon=":material/database:")
relation_page = st.Page("page3.py", title="Relationship Analysis & Prediction", icon=":material/bar_chart:")
geo_page = st.Page(page4, title="Condo Map Insights & Classification", icon=":material/map:")
ai_page = st.Page("page5.py", title="Advanced Search & Comparison", icon=":material/compare:")

# Create menu
pg = st.navigation({
    "Menu": [home_page, desc_page, relation_page, geo_page, ai_page],
})
pg.run()
