import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import duckdb
import plotly.express as px
import plotly.graph_objects as go
import joblib
from sklearn.preprocessing import StandardScaler
import numpy as np

# --------------------------
# 🔧 Setup
# --------------------------
df_columns = [
    'rent_cd_price', 'rent_cd_bed', 'rent_cd_bath',
    'rent_cd_features_time', 'rent_cd_features_station',
    'star', 'starnum_list', 'near_rail_meter'
]

engine = create_engine("mysql+mysqlconnector://root:admin@localhost:3306/dads5001db")
duck_con = duckdb.connect()

# --------------------------
# 📊 Page 3 - Correlation & Prediction
# --------------------------
def page3():
    st.title("Relationship Analysis & Price Prediction")

    # -----------------------------------
    # 🔗 Load and show description
    # -----------------------------------
    df = pd.read_sql('SELECT * FROM unclean_data', con=engine)
    duck_con.register('unclean_data', df)
    result = duck_con.execute("SELECT * FROM unclean_data").df()

    st.subheader("📄 Column Descriptions")
    description = pd.DataFrame({
        'ชื่อ columns': df_columns,
        'คำอธิบาย': [
            'ค่าเช่ารายเดือน (บาท)', 'จำนวนห้องนอน (ห้อง)', 'จำนวนห้องน้ำ (ห้อง)',
            'ระยะเวลาที่ใช้ในการเดินไปถึงสถานีรถไฟฟ้า (นาที)', 'ชื่อสถานีรถไฟฟ้าที่ใกล้ที่สุด',
            'คะแนน star rating (0 - 5)', 'จำนวนความคิดเห็น', 'ระยะทางระหว่างคอนโดกับรถไฟฟ้า (เมตร)'
        ]
    })
    st.write(description)

    # -----------------------------------
    # 📈 Scatter Plot Comparison
    # -----------------------------------
    st.subheader("🔍 Compare Any Two Columns")
    y_col = st.selectbox("Y Axis", df_columns, key="y_axis")
    x_col = st.selectbox("X Axis", df_columns, key="x_axis")

    fig_scatter = px.scatter(result, x=x_col, y=y_col, title="Scatter Plot")
    st.plotly_chart(fig_scatter, use_container_width=True)

    # -----------------------------------
    # 📊 Correlation Heatmap
    # -----------------------------------
    st.subheader("📊 Correlation Matrix")
    corr_df = result[df_columns].drop('rent_cd_features_station', axis=1).corr()
    z_text = [[f"{val:.2f}" for val in row] for row in corr_df.values]

    fig_corr = go.Figure(data=go.Heatmap(
        z=corr_df.values,
        x=corr_df.columns,
        y=corr_df.index,
        colorscale='RdBu',
        zmin=-1, zmax=1,
        text=z_text,
        texttemplate="%{text}",
        hovertemplate="Correlation: %{z:.2f}<extra></extra>"
    ))

    fig_corr.update_layout(
        width=900, height=800,
        margin=dict(l=100, r=100, t=50, b=50)
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    # -----------------------------------
    # 🤖 Price Prediction
    # -----------------------------------
    st.subheader("💡 Predict Condo Price")

    # Station Encoding
    station_list = result['rent_cd_features_station'].unique().tolist()
    station_to_code = {name: i for i, name in enumerate(station_list)}
    code_to_station = {v: k for k, v in station_to_code.items()}

    # 👤 User Inputs
    user_bed = st.number_input("Number of bedrooms", min_value=1, step=1, key="user_bed")
    user_bath = st.number_input("Number of bathrooms", min_value=1, step=1, key="user_bath")
    user_near_rail = st.number_input("Max distance to rail station (meters)", min_value=0.0, step=10.0, key="user_near_rail")
    user_station = st.selectbox("Nearest Station", station_list, key="user_station")

    # 🔢 Feature Scaling
    scaler = StandardScaler()
    features = ['rent_cd_bed', 'rent_cd_bath', 'near_rail_meter', 'rent_cd_features_station']
    df2 = result[features].copy()
    df2['rent_cd_features_station'] = df2['rent_cd_features_station'].map(station_to_code)
    scaler.fit(df2)

    user_features = pd.DataFrame([{
        'rent_cd_bed': user_bed,
        'rent_cd_bath': user_bath,
        'near_rail_meter': user_near_rail,
        'rent_cd_features_station': station_to_code[user_station]
    }])

    if st.button("Submit"):
        # -----------------------------------
        # 🧠 Load model based on input
        # -----------------------------------
        if user_station is None:
            model_path = r"D:\Nida\nida_term01_02\DADS5001\GIT_final\final2\python\model\random_forest_model_nostation.joblib"
        else:
            model_path = r"D:\Nida\nida_term01_02\DADS5001\GIT_final\final2\python\model\random_forest_model.joblib"

        model = joblib.load(model_path)

        # -----------------------------------
        # 🔍 Find similar condos
        # -----------------------------------
        filter_condos = result[
            (result['rent_cd_bed'] == user_bed) &
            (result['rent_cd_bath'] == user_bath) &
            (result['near_rail_meter'].between(user_near_rail - 100, user_near_rail + 100))
        ]

        if user_station is not None:
            filter_condos = filter_condos[filter_condos['rent_cd_features_station'] == user_station]

        if filter_condos.empty:
            st.warning("⚠️ No exact match found within 100m. Relaxing the filter...")
            filter_condos = result[
                (result['rent_cd_bed'] == user_bed) &
                (result['rent_cd_bath'] == user_bath)
            ]

        # -----------------------------------
        # 🔮 Predict and Show Price
        # -----------------------------------
        user_scaled = scaler.transform(user_features)
        predicted_price = model.predict(user_scaled)[0]
        st.markdown(f'##### 💰 Predicted Price is <u>{predicted_price:,.0f}</u> THB', unsafe_allow_html=True)

        # -----------------------------------
        # 🏢 Recommend Top Condos
        # -----------------------------------
        top_cheap = filter_condos.nsmallest(5, 'rent_cd_price').assign(label='CHEAPEST')
        top_expensive = filter_condos.nlargest(5, 'rent_cd_price').assign(label='EXPENSIVE')
        recommended = pd.concat([top_cheap, top_expensive])

        display_cols = ['label', 'new_condo_name', 'rent_cd_price', 'rent_cd_bed', 'rent_cd_bath',
                        'near_rail_meter', 'star', 'rent_cd_agent', 'rent_cd_tel', 'rent_cd_features_station']

        st.markdown("##### 📊 Top 5 Cheapest and Most Expensive Condos")
        st.dataframe(recommended[display_cols])

# --------------------------
# 🧭 Navigation
# --------------------------
home_page = st.Page("page1.py", title="Home Page", icon=":material/home:")
desc_page = st.Page("page2.py", title="Descriptive Analysis", icon=":material/database:")
relation_page = st.Page(page3, title="Relationship Analysis & Prediction", icon=":material/bar_chart:")
geo_page = st.Page("page4.py", title="Geospatial & Classification", icon=":material/map:")
ai_page = st.Page("page5.py", title="Advanced Search & Comparison", icon=":material/compare:")

# Create menu
pg = st.navigation({
    "Menu": [home_page, desc_page, relation_page, geo_page, ai_page],
})
pg.run()
