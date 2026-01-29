import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="Analyse MovieLens",
    page_icon=""
)

# Navigation

page1 = st.Page("page1.py", title="Vue d'ensemble", icon="")
page2 = st.Page("page2.py", title="Analyse des tags", icon="")
page3 = st.Page("page3.py", title="Exploration des films", icon="")

pg = st.navigation([page1, page2, page3])
pg.run()

