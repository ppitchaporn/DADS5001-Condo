import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree


# --------------------------
# 🔧 Config
# --------------------------
st.set_page_config(page_title="Bangkok Condo Insights", layout="wide")

# --------------------------
# 🗺️ Page 4 - Map & Decision Tree Classification
# --------------------------
def page4():
    st.title("🏙️ Bangkok Condo Map and Decision Tree Classifier")
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
        df['price_per_sqm'] = df['rent_cd_price'] / df['rent_cd_floorarea']
        df['rate_type'] = df['rent_cd_price'].apply(lambda x: 0 if x < 10000 else (1 if x < 20000 else 2))
        return df

    df = load_data()

    tab1, tab2 = st.tabs(["🗺️ Condo Map Insights", "🌲 Decision Tree Structure"])


    # --------------------------
    # Tab 1: Condo Map
    # --------------------------
    with tab1:
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
        min_price = st.number_input("Minimum Price", value=10000, step=1000)
        max_price = st.number_input("Maximum Price", value=30000, step=1000)
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

        if st.checkbox("Show condo data table"):
            st.dataframe(filtered, use_container_width=True)

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
    # Tab 2: Decision Tree
    # --------------------------
    with tab2:
        st.subheader("Decision Tree Structure")

        X = df.drop(columns=['rate_type'])
        X = X.select_dtypes(include=['number'])  # Keep only numeric columns
        y = df['rate_type']
        X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        param_grid = {
            'max_depth': [3, 4, 5, 6],
            'min_samples_leaf': [1, 5, 10],
            'criterion': ['gini', 'entropy']
        }

        grid_search = GridSearchCV(DecisionTreeClassifier(random_state=42),
                                param_grid=param_grid,
                                cv=5, n_jobs=-1)
        grid_search.fit(X_train_scaled, y_train)
        model = grid_search.best_estimator_

        tree_fig = plt.figure(figsize=(10, 8))
        plot_tree(model, filled=True,
                feature_names=X.columns.tolist(),
                class_names=["Low", "Medium", "High"],
                rounded=True,
                fontsize=10,
                max_depth=5)
        plt.title("Decision Tree Classifier", fontsize=16, fontweight='bold')

        st.markdown("""
        **Class Definitions**  
        - 🟧 **Low**: Rental price < 10,000 THB  
        - 🟩 **Medium**: Rental price between 10,000–19,999 THB  
        - 🟪 **High**: Rental price ≥ 20,000 THB  
        
        """)

        st.pyplot(tree_fig)

        # --------------------------
        # Classification Map (based on rate_type)
        # --------------------------
        st.markdown("### 🗺️ Condo Classification Map by Price Category")

        # Assign colors by class
        # 1. Define readable labels
        rate_label_map = {
            0: "Low",
            1: "Medium",
            2: "High"
        }
        df['rate_label'] = df['rate_type'].map(rate_label_map)

        # 2. Assign colors based on text labels
        color_map = {
            "Low": [255, 165, 0],     # Orange
            "Medium": [0, 200, 0],    # Green
            "High": [128, 0, 128]     # Purple
        }
        df['color'] = df['rate_label'].map(color_map)

                # Create PyDeck layer
        classification_layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position='[longitude, latitude]',
            get_fill_color='color',
            get_radius=60,
            pickable=True,
            opacity=0.8,
        )

        # View settings
        view_state = pdk.ViewState(latitude=13.75, longitude=100.52, zoom=11)

        # Display map
        classification_map = pdk.Deck(
            layers=[classification_layer],
            initial_view_state=view_state,
            tooltip={"text": "🏢 {new_condo_name}\n💰 Price: {rent_cd_price} THB\n🎯 Class: {rate_label}"}
        )

        st.pydeck_chart(classification_map)


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
