import streamlit as st
import pandas as pd

from src.config import APP_TITLE, DEFAULT_CSV_PATH, RESEARCH_QUESTION, KEYWORDS
from src.data_loader import load_csv, validate_scopus_columns
from src.preprocessing import prepare_dataframe, get_summary_metrics
from src.visualizations import (
    plot_publications_by_year,
    plot_citations_by_year,
    plot_top_cited_articles,
    plot_sources_distribution,
    plot_document_types,
    plot_open_access,
    plot_top_authors,
    plot_keyword_frequency,
    plot_self_esteem_terms,
    plot_relevance_radar,
)
from src.text_analysis import get_top_words_from_abstracts


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,75,139,0.16), rgba(124,58,237,0.10));
        border: 1px solid rgba(255,255,255,0.10);
        padding: 16px;
        border-radius: 16px;
    }
    .section-card {
        padding: 18px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.12);
        background: rgba(255,255,255,0.035);
        margin-bottom: 14px;
    }
    .small-muted {
        color: #cbd5e1;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title(APP_TITLE)
st.caption(
    "Dashboard interactivo para analizar artículos científicos de Scopus sobre Instagram, adolescentes, redes sociales y autoestima."
)

st.info(
    """
    👋 **Bienvenido al dashboard de investigación.**

    Esta aplicación permite explorar artículos científicos exportados desde Scopus sobre la relación entre
    **Instagram**, **redes sociales**, **adolescentes** y **autoestima**. Usa los filtros de la barra lateral para
    analizar años, tipos de documento, autores, artículos más citados y conceptos recurrentes en abstracts y keywords.
    """
)

with st.expander("📌 Pregunta de investigación y keywords", expanded=True):
    st.markdown(f"**Pregunta de investigación:** {RESEARCH_QUESTION}")
    st.markdown("**Keywords usadas:** " + " · ".join([f"`{k}`" for k in KEYWORDS]))
    st.info(
        "Puedes cargar un CSV local desde la barra lateral, leerlo desde una URL RAW de GitHub o usar el dataset incluido. "
        "El dashboard detecta automáticamente columnas clave como autores, título, año, citas, abstract y keywords."
    )

st.sidebar.header("📁 Fuente de datos")
st.sidebar.info(
    """
    💡 **Guía rápida**

    1. Elige la fuente del CSV.
    2. Filtra por año y tipo de documento.
    3. Busca términos como `self-esteem`, `body image` o `Instagram`.
    4. Explora los gráficos y descarga el dataset filtrado.
    """
)

data_source = st.sidebar.radio(
    "Selecciona cómo cargar el CSV:",
    ["Usar CSV incluido", "Subir CSV local", "Leer CSV desde URL de GitHub"],
)

uploaded_file = None
github_url = ""

if data_source == "Subir CSV local":
    uploaded_file = st.sidebar.file_uploader("Sube tu archivo CSV de Scopus", type=["csv"])
    csv_source = uploaded_file
elif data_source == "Leer CSV desde URL de GitHub":
    github_url = st.sidebar.text_input(
        "Pega el enlace RAW del CSV en GitHub",
        placeholder="https://raw.githubusercontent.com/usuario/repositorio/main/data/scopus.csv",
    )
    csv_source = github_url.strip() if github_url.strip() else None
else:
    csv_source = DEFAULT_CSV_PATH

if csv_source is None:
    st.warning("Carga un archivo CSV o pega una URL RAW de GitHub para iniciar.")
    st.stop()

try:
    raw_df = load_csv(csv_source)
except Exception as exc:
    st.error(f"No se pudo leer el archivo CSV. Detalle: {exc}")
    st.stop()

missing = validate_scopus_columns(raw_df)
df = prepare_dataframe(raw_df)

if missing:
    st.warning(
        "El archivo fue cargado, pero faltan algunas columnas recomendadas para Scopus: "
        + ", ".join(missing)
    )
else:
    st.success("CSV cargado correctamente con las columnas principales de Scopus.")

st.sidebar.header("🔎 Filtros")
years = sorted(df["Year"].dropna().astype(int).unique().tolist()) if "Year" in df.columns else []

if years:
    min_year, max_year = min(years), max(years)
    selected_years = st.sidebar.slider(
        "Rango de años",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
    )
    df = df[(df["Year"] >= selected_years[0]) & (df["Year"] <= selected_years[1])]

doc_types = sorted(df["Document Type"].dropna().unique().tolist()) if "Document Type" in df.columns else []
if doc_types:
    selected_doc_types = st.sidebar.multiselect(
        "Tipo de documento",
        options=doc_types,
        default=doc_types,
    )
    df = df[df["Document Type"].isin(selected_doc_types)]

search_text = st.sidebar.text_input("Buscar por título, autor o keyword")
if search_text:
    search_cols = [c for c in ["Title", "Authors", "Author Keywords", "Index Keywords", "Abstract"] if c in df.columns]
    mask = pd.Series(False, index=df.index)
    for col in search_cols:
        mask = mask | df[col].astype(str).str.contains(search_text, case=False, na=False)
    df = df[mask]

st.sidebar.success("✅ Dashboard listo para explorar")

metrics = get_summary_metrics(df)

st.subheader("📊 Métricas generales")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Artículos", metrics["articles"])
m2.metric("Años analizados", metrics["years"])
m3.metric("Citas totales", metrics["citations"])
m4.metric("Promedio de citas", metrics["avg_citations"])

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Producción científica",
    "🧠 Autoestima e Instagram",
    "🏆 Impacto académico",
    "🔤 Keywords y abstracts",
    "📄 Dataset",
])

with tab1:
    st.markdown(
        """
        <div class="section-card">
        <b>Objetivo:</b> observar la evolución temporal de investigaciones sobre Instagram, adolescentes y autoestima,
        además de identificar fuentes, tipos de documento y acceso abierto.
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        fig = plot_publications_by_year(df)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = plot_citations_by_year(df)
        st.plotly_chart(fig, use_container_width=True)

    c5, c6 = st.columns([1.1, 1])
    with c5:
        fig = plot_sources_distribution(df)
        st.plotly_chart(fig, use_container_width=True)
    with c6:
        st.info(
            "📌 La producción por año muestra la actualidad del tema. Las citas por año ayudan a reconocer períodos con mayor impacto académico."
        )

    c3, c4 = st.columns(2)
    with c3:
        fig = plot_document_types(df)
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        fig = plot_open_access(df)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown(
        """
        <div class="section-card">
        <b>Relación con la pregunta:</b> esta sección identifica la presencia de conceptos vinculados a autoestima,
        adolescentes, comparación social, imagen corporal, salud mental e Instagram dentro del dataset.
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns([1.2, 1])
    with c1:
        fig = plot_self_esteem_terms(df)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = plot_relevance_radar(df)
        st.plotly_chart(fig, use_container_width=True)

    st.success(
        "Estos gráficos responden directamente a la pregunta de investigación porque muestran qué conceptos aparecen con mayor frecuencia en títulos, abstracts y keywords."
    )

with tab3:
    st.markdown(
        """
        <div class="section-card">
        <b>Objetivo:</b> reconocer los artículos y autores con mayor influencia científica dentro del tema seleccionado.
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns([1.3, 1])
    with c1:
        fig = plot_top_cited_articles(df)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = plot_top_authors(df)
        st.plotly_chart(fig, use_container_width=True)

    st.info(
        "🏆 Los artículos más citados ayudan a identificar investigaciones influyentes sobre Instagram, autoestima y adolescentes."
    )

with tab4:
    st.markdown(
        """
        <div class="section-card">
        <b>Objetivo:</b> analizar los términos más repetidos en keywords y abstracts para detectar tendencias del tema.
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        fig = plot_keyword_frequency(df)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        top_words = get_top_words_from_abstracts(df, top_n=20)
        st.subheader("Top palabras en abstracts")
        st.dataframe(top_words, use_container_width=True, hide_index=True)

    st.info(
        "🔎 El análisis de palabras permite detectar conceptos recurrentes como autoestima, redes sociales, bienestar, imagen corporal o salud mental."
    )

with tab5:
    st.subheader("Tabla de artículos")
    st.caption("Explora los artículos filtrados y descarga el resultado para continuar el análisis en Excel, Python o Power BI.")
    preferred_cols = [
        "Authors", "Title", "Year", "Source title", "Cited by", "DOI",
        "Author Keywords", "Index Keywords", "Abstract"
    ]
    visible_cols = [c for c in preferred_cols if c in df.columns]
    st.dataframe(df[visible_cols], use_container_width=True, hide_index=True)

    csv_download = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Descargar dataset filtrado",
        data=csv_download,
        file_name="scopus_filtrado.csv",
        mime="text/csv",
    )

st.divider()
st.success(
    """
    📌 **Conclusión general**

    El dashboard evidencia que existe producción científica reciente sobre la relación entre Instagram,
    redes sociales, adolescentes y autoestima. La evolución de publicaciones, los artículos más citados,
    los autores frecuentes y los términos presentes en abstracts y keywords permiten identificar tendencias
    de investigación relacionadas con autoestima, comparación social, imagen corporal y bienestar psicológico.
    """
)
