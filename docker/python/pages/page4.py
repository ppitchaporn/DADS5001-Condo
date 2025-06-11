import streamlit as st
import pandas as pd
import pydeck as pdk

from sqlalchemy import create_engine
import duckdb

st.set_page_config(layout="wide")

# --------------------------
# 🗺️ Page 4 - Map
# --------------------------
def page4():
    st.title("🏙️ Bangkok Condo Map Insights")

    @st.cache_data
    def load_data():
        url = "https://raw.githubusercontent.com/ppitchaporn/DADS5001-Condo/refs/heads/main/data_cleaned.csv"
        df = pd.read_csv(url)
        df['rent_cd_price'] = df['rent_cd_price'].astype(str).str.replace(',', '', regex=False).astype(float)
        df.dropna(subset=['latitude', 'longitude'], inplace=True)
        return df

    # Load and group data
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

    # Flatten columns
    grouped.columns = ['Condo Name', 'Latitude', 'Longitude', 'Min Price', 'Max Price', 'Avg Price',
                   'Bedrooms', 'Bathrooms', 'Min Area', 'Max Area', 'Avg Area', 'Avg Rating', 'MRT Distance']
    
    # Round Avg Price to int
    #grouped['Avg Price'] = grouped['Avg Price'].round().astype(int)
    grouped['Avg Area'] = grouped['Avg Area'].round()
    grouped['Min Area'] = grouped['Min Area'].round()
    grouped['Max Area'] = grouped['Max Area'].round()

    # Sidebar filters
    st.markdown("#### 🔍 Filter Condos")
    bedroom = st.selectbox("Number of Bedrooms", sorted(grouped['Bedrooms'].dropna().unique()))
    bathroom = st.selectbox("Number of Bathrooms", sorted(grouped['Bathrooms'].dropna().unique()))
        
    st.markdown("#### 💰 Price Range (THB)")
    min_price = st.number_input("Minimum Price", min_value=int(grouped['Min Price'].min()), value=10000, step=1000)
    max_price = st.number_input("Maximum Price", min_value=int(min_price), max_value=int(grouped['Max Price'].max()), value=30000, step=1000)

    st.markdown("#### 📐 Floor Area Range (m²)")
    min_area = st.number_input("Minimum Area", min_value=int(grouped['Avg Area'].min()), value=25, step=5)
    max_area = st.number_input("Maximum Area", min_value=int(min_area), max_value=int(grouped['Avg Area'].max()), value=80, step=5)

    st.markdown("#### ⭐ Rating")
    rating = st.slider("Minimum Rating", 3.50, 5.00, 4.00, step=0.1, format="%.1f")
    
    # Apply filters
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

    # Tooltip
    filtered['tooltip'] = (
        "🏢 " + filtered['Condo Name'] + "<br>" +
        "💰 Avg Price: " + filtered['Avg Price'].astype(int).astype(str) + " THB<br>" +
        "🛏️ Bed: " + filtered['Bedrooms'].astype(str) +
        ", 🛁 Bath: " + filtered['Bathrooms'].astype(str) + "<br>" +
        "⭐ Rating: " + filtered['Avg Rating'].round(1).astype(str) + "<br>" +
        "🚆 MRT Distance: " + filtered['MRT Distance'].fillna(-1).apply(lambda x: f"{int(x)} m" if x >= 0 else "N/A")
    )

    # Icon column
    filtered['icon_data'] = [{
        "url": "https://cdn-icons-png.flaticon.com/512/684/684908.png",
        "width": 128,
        "height": 128,
        "anchorY": 128
    }] * len(filtered)

    # Map layer
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
    view_state = pdk.ViewState(
        latitude=13.75,
        longitude=100.52,
        zoom=11,
        pitch=0
    )
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

    # Dropdown to specify condo name
    # Filter for map display (using user inputs)
    filtered_df = df[
        (df['rent_cd_bed'] == bedroom) &
        (df['rent_cd_price'] >= min_price) &
        (df['rent_cd_price'] <= max_price) &
        (df['star'] >= rating)
    ].copy()

    # Create dropdown from unique condo names based on filter
    condo_names = filtered_df['new_condo_name'].dropna().unique()
    selected_condo = st.selectbox("📌 Select a Condo to View All Listings", condo_names)
    
    # Filter another df to show all listings based on filter
    condo_details_df = filtered_df[filtered_df['new_condo_name'] == selected_condo]

    # Display the details table for the selected condo
    st.dataframe(
        condo_details_df[[
            'new_condo_name', 'rent_cd_price', 'rent_cd_bed', 'rent_cd_bath','rent_cd_floorarea', 'star', 'rent_cd_agent', 'rent_cd_tel'
        ]].rename(columns={
            'new_condo_name': 'Condo Name',
            'rent_cd_price': 'Price (THB)',
            'rent_cd_bed': 'Bedrooms',
            'rent_cd_bath': 'Bathrooms',
            'rent_cd_floorarea':'Area',
            'star': 'Rating',
            'rent_cd_agent': 'Agent',
            'rent_cd_tel': 'Tel'
        }), 
        use_container_width=True
    )

# Copy from page 3
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
