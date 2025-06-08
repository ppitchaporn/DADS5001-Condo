import streamlit as st


def page4():
    st.markdown("# Dashboard ❄️")
    st.write("Here's our first attempt at using data to create a table:")

## page
home_page = st.Page("page1.py",title='Home page', icon=":material/home:")
descipt = st.Page("page2.py", title='Descriptive Analysis', icon=":material/database:")
relation_predict = st.Page("page3.py", title='Relationship Analysis & Price Prediction', icon=":material/bar_chart:")
geospatial_class = st.Page(page4, title='Geospatial Analysis & Classification Result', icon=":material/bar_chart:")
Ai_search = st.Page("page5.py", title=' Advanced Search & Comparison', icon=":material/note:")

## create menu tree
pg = st.navigation(
    {
        "Menu": [home_page, descipt, relation_predict, geospatial_class, Ai_search]

    }
)

pg.run()