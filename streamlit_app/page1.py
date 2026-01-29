import streamlit as st
from pathlib import Path


OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

st.title("Analyse générale des films et évaluations")

@st.cache_data
def load_html_chart(file_name):
    html_path = OUTPUT_DIR / f"{file_name}.html"
    if html_path.exists():
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None


st.header("1. Distribution des genres")
genre_chart = load_html_chart("genre_counts")
if genre_chart:
    st.components.v1.html(genre_chart, height=600)
else:
    st.error("Graphique des genres non trouvé")

st.header("2. Films par année")
year_chart = load_html_chart("movies_by_year")
if year_chart:
    st.components.v1.html(year_chart, height=600)
else:
    st.error("Graphique des années non trouvé")

st.header("3. Top 20 des films par nombre d'évaluations")
movies_chart = load_html_chart("top_movies_by_ratings")
if movies_chart:
    st.components.v1.html(movies_chart, height=800)
else:
    st.error("Graphique des films non trouvé")

st.header("4. Top tags les plus utilisés")
tags_chart = load_html_chart("top_tags")
if tags_chart:
    st.components.v1.html(tags_chart, height=600)
else:
    st.error("Graphique des tags non trouvé")

