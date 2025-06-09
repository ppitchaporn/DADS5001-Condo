import streamlit as st
import pandas as pd
import pydeck as pdk
st.set_page_config(page_title="Bangkok Condo Cluster Map", layout="wide")
st.title("🏙️ Bangkok Condo Map")
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/PTUNTUK/DADS5001_Condo/main/Data%20Cleaned.csv"
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
        'star': 'mean',
        'near_rail_meter': 'min'
    })
)
# Flatten columns
grouped.columns = ['Condo Name', 'Latitude', 'Longitude', 'Min Price', 'Max Price', 'Avg Price',
                   'Bedrooms', 'Bathrooms', 'Avg Rating', 'MRT Distance']
# Round Avg Price to int
grouped['Avg Price'] = grouped['Avg Price'].round().astype(int)
# Sidebar filters
st.sidebar.header("🔍 Filter Condos")
bedroom = st.sidebar.selectbox("Number of Bedrooms", sorted(grouped['Bedrooms'].dropna().unique()))
bedroom = st.sidebar.selectbox("Number of Bathrooms", sorted(grouped['Bathrooms'].dropna().unique()))

st.sidebar.markdown("#### 💰 Price Range (THB)")
min_price = st.sidebar.number_input("Minimum Price", min_value=int(grouped['Min Price'].min()), value=10000, step=1000)
max_price = st.sidebar.number_input("Maximum Price", min_value=int(min_price), max_value=int(grouped['Max Price'].max()), value=30000, step=1000)
rating = st.sidebar.slider("Minimum Rating", 3.50, 5.00, 4.00, step=0.1, format="%.1f")
# Apply filters
filtered = grouped[
    (grouped['Bedrooms'] == bedroom) &
    (grouped['Avg Price'] >= min_price) &
    (grouped['Avg Price'] <= max_price) &
    (grouped['Avg Rating'] >= rating)
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
            'Bedrooms', 'Bathrooms', 'Avg Rating', 'MRT Distance'
        ]].rename(columns={
            'Avg Price': 'Avg Price (THB)',
            'Min Price': 'Min Price (THB)',
            'Max Price': 'Max Price (THB)',
            'Avg Rating': 'Rating',
            'MRT Distance': 'Distance to MRT/BTS'
        })
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
#condo_names = df['new_condo_name'].dropna().unique()
condo_names = filtered_df['new_condo_name'].dropna().unique()
selected_condo = st.selectbox("📌 Select a Condo to View All Listings", condo_names)
# Filter another df to show all listings based on filter
#condo_details_df = df[df['new_condo_name'] == selected_condo]
condo_details_df = filtered_df[filtered_df['new_condo_name'] == selected_condo]
# Display the details table for the selected condo
st.dataframe(
    condo_details_df[[
        'new_condo_name', 'rent_cd_price', 'rent_cd_bed', 'rent_cd_bath', 'star', 'rent_cd_agent', 'rent_cd_tel'
    ]].rename(columns={
        'new_condo_name': 'Condo Name',
        'rent_cd_price': 'Price (THB)',
        'rent_cd_bed': 'Bedrooms',
        'rent_cd_bath': 'Bathrooms',
        'star': 'Rating',
        'rent_cd_agent': 'Agent',
        'rent_cd_tel': 'Tel'
    })
)
