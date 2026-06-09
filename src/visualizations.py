import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

COLOR_SEQ = ["#ff4b8b", "#7c3aed", "#38bdf8", "#22c55e", "#f59e0b", "#ef4444", "#a78bfa"]
TEMPLATE = "plotly_dark"


def _empty_fig(title: str):
    fig = go.Figure()
    fig.update_layout(template=TEMPLATE, title=title, height=380)
    fig.add_annotation(text="No hay datos disponibles", showarrow=False, x=0.5, y=0.5)
    return fig


def plot_publications_by_year(df: pd.DataFrame):
    if "Year" not in df.columns or df.empty:
        return _empty_fig("Publicaciones por año")
    data = df.dropna(subset=["Year"]).copy()
    data["Year"] = data["Year"].astype(int)
    counts = data.groupby("Year").size().reset_index(name="Artículos")
    fig = px.line(counts, x="Year", y="Artículos", markers=True, text="Artículos",
                  title="Evolución de publicaciones sobre Instagram, adolescentes y autoestima",
                  color_discrete_sequence=["#ff4b8b"], template=TEMPLATE)
    fig.update_traces(textposition="top center", line=dict(width=4), marker=dict(size=10))
    fig.update_layout(height=420, xaxis_title="Año", yaxis_title="Cantidad de artículos")
    return fig


def plot_citations_by_year(df: pd.DataFrame):
    if not {"Year", "Cited by"}.issubset(df.columns) or df.empty:
        return _empty_fig("Citas acumuladas por año")
    data = df.dropna(subset=["Year"]).copy()
    data["Year"] = data["Year"].astype(int)
    data["Cited by"] = pd.to_numeric(data["Cited by"], errors="coerce").fillna(0)
    grouped = data.groupby("Year", as_index=False)["Cited by"].sum()
    fig = px.bar(grouped, x="Year", y="Cited by", text="Cited by",
                 title="Impacto académico: citas acumuladas por año",
                 color="Cited by", color_continuous_scale="RdPu", template=TEMPLATE)
    fig.update_traces(textposition="outside")
    fig.update_layout(height=420, xaxis_title="Año", yaxis_title="Total de citas", coloraxis_showscale=False)
    return fig


def plot_top_cited_articles(df: pd.DataFrame):
    if not {"Title", "Cited by"}.issubset(df.columns) or df.empty:
        return _empty_fig("Artículos más citados")
    data = df.copy()
    data["Cited by"] = pd.to_numeric(data["Cited by"], errors="coerce").fillna(0)
    data = data.sort_values("Cited by", ascending=False).head(10)
    data["Título corto"] = data["Title"].astype(str).str.slice(0, 70) + "..."
    hover_cols = [c for c in ["Title", "Authors", "Year", "Source title", "DOI"] if c in data.columns]
    fig = px.bar(data, x="Cited by", y="Título corto", orientation="h", text="Cited by",
                 title="Top artículos más citados del dataset",
                 color="Cited by", color_continuous_scale="Bluered", template=TEMPLATE,
                 hover_data=hover_cols)
    fig.update_layout(height=520, yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False,
                      xaxis_title="Citas", yaxis_title="Artículo")
    return fig


def plot_sources_distribution(df: pd.DataFrame):
    if "Source title" not in df.columns or df.empty:
        return _empty_fig("Fuentes principales")
    data = df["Source title"].replace("", "No especificado").value_counts().head(8).reset_index()
    data.columns = ["Fuente", "Artículos"]
    fig = px.treemap(data, path=["Fuente"], values="Artículos", color="Artículos",
                     color_continuous_scale="Purpor", title="Revistas o fuentes con más publicaciones",
                     template=TEMPLATE)
    fig.update_layout(height=450)
    return fig


def plot_document_types(df: pd.DataFrame):
    if "Document Type" not in df.columns or df.empty:
        return _empty_fig("Tipo de documento")
    data = df["Document Type"].replace("", "No especificado").value_counts().reset_index()
    data.columns = ["Tipo", "Cantidad"]
    fig = px.pie(data, names="Tipo", values="Cantidad", hole=0.55,
                 title="Distribución por tipo de documento", color_discrete_sequence=COLOR_SEQ,
                 template=TEMPLATE)
    fig.update_traces(textinfo="percent+label", pull=[0.04] * len(data))
    fig.update_layout(height=420)
    return fig


def plot_open_access(df: pd.DataFrame):
    if "Open Access" not in df.columns or df.empty:
        return _empty_fig("Acceso abierto")
    data = df["Open Access"].replace("", "No especificado").value_counts().reset_index()
    data.columns = ["Acceso", "Cantidad"]
    fig = px.pie(data, names="Acceso", values="Cantidad", hole=0.45,
                 title="Disponibilidad de acceso abierto", color_discrete_sequence=COLOR_SEQ,
                 template=TEMPLATE)
    fig.update_layout(height=420)
    return fig


def plot_top_authors(df: pd.DataFrame):
    if "Authors" not in df.columns or df.empty:
        return _empty_fig("Autores frecuentes")
    authors = []
    for item in df["Authors"].dropna().astype(str):
        authors.extend([a.strip() for a in item.split(";") if a.strip()])
    if not authors:
        return _empty_fig("Autores frecuentes")
    data = pd.Series(authors).value_counts().head(12).reset_index()
    data.columns = ["Autor", "Artículos"]
    fig = px.bar(data, x="Artículos", y="Autor", orientation="h", text="Artículos",
                 title="Autores con mayor presencia en el dataset",
                 color="Artículos", color_continuous_scale="Teal", template=TEMPLATE)
    fig.update_layout(height=500, yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    return fig


def plot_keyword_frequency(df: pd.DataFrame):
    cols = [c for c in ["Author Keywords", "Index Keywords"] if c in df.columns]
    if not cols or df.empty:
        return _empty_fig("Frecuencia de keywords")
    keywords = []
    for col in cols:
        for row in df[col].dropna().astype(str):
            parts = row.replace(",", ";").split(";")
            keywords.extend([p.strip().lower().title() for p in parts if len(p.strip()) > 2])
    if not keywords:
        return _empty_fig("Frecuencia de keywords")
    data = pd.Series(keywords).value_counts().head(15).reset_index()
    data.columns = ["Keyword", "Frecuencia"]
    fig = px.bar(data, x="Frecuencia", y="Keyword", orientation="h", text="Frecuencia",
                 title="Conceptos más frecuentes en keywords",
                 color="Frecuencia", color_continuous_scale="Sunsetdark", template=TEMPLATE)
    fig.update_layout(height=520, yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    return fig


def plot_self_esteem_terms(df: pd.DataFrame):
    if df.empty:
        return _empty_fig("Términos asociados a autoestima")
    text_cols = [c for c in ["Title", "Abstract", "Author Keywords", "Index Keywords"] if c in df.columns]
    if not text_cols:
        return _empty_fig("Términos asociados a autoestima")
    combined = " ".join(df[text_cols].fillna("").astype(str).agg(" ".join, axis=1)).lower()
    terms = {
        "Self-esteem": ["self-esteem", "self esteem", "autoestima"],
        "Adolescents": ["adolescent", "adolescents", "teen", "teenagers"],
        "Social comparison": ["social comparison", "comparison"],
        "Body image": ["body image", "body satisfaction", "appearance"],
        "Mental health": ["mental health", "anxiety", "depression", "wellbeing", "well-being"],
        "Social media": ["social media", "instagram"],
    }
    rows = []
    for label, variants in terms.items():
        count = sum(combined.count(v) for v in variants)
        rows.append({"Tema": label, "Frecuencia": count})
    data = pd.DataFrame(rows).sort_values("Frecuencia", ascending=False)
    fig = px.bar(data, x="Tema", y="Frecuencia", text="Frecuencia",
                 title="Términos clave vinculados a la pregunta de investigación",
                 color="Frecuencia", color_continuous_scale="Magenta", template=TEMPLATE)
    fig.update_layout(height=420, xaxis_title="Tema", yaxis_title="Frecuencia", coloraxis_showscale=False)
    return fig


def plot_relevance_radar(df: pd.DataFrame):
    if df.empty:
        return _empty_fig("Alineación temática")
    text_cols = [c for c in ["Title", "Abstract", "Author Keywords", "Index Keywords"] if c in df.columns]
    labels = ["Instagram", "Adolescents", "Social Media", "Self-esteem"]
    patterns = {
        "Instagram": ["instagram"],
        "Adolescents": ["adolescent", "adolescents", "teen", "youth"],
        "Social Media": ["social media", "social network", "social networks"],
        "Self-esteem": ["self-esteem", "self esteem", "autoestima"],
    }
    scores = []
    for label in labels:
        n = 0
        for _, row in df[text_cols].fillna("").astype(str).iterrows():
            text = " ".join(row.values).lower()
            if any(p in text for p in patterns[label]):
                n += 1
        scores.append(n)
    fig = go.Figure(data=go.Scatterpolar(r=scores + [scores[0]], theta=labels + [labels[0]], fill="toself",
                                         line_color="#ff4b8b", name="Artículos relacionados"))
    fig.update_layout(template=TEMPLATE, title="Alineación del dataset con las 4 keywords usadas",
                      polar=dict(radialaxis=dict(visible=True, range=[0, max(max(scores), 1)])), height=450)
    return fig
