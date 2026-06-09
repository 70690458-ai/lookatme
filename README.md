# Dashboard Scopus - Instagram y Autoestima en Adolescentes

Aplicación web desarrollada en **Streamlit** para analizar artículos científicos exportados desde **Scopus**.

## Pregunta de investigación

¿Cómo influye Instagram en la autoestima de los adolescentes?

## Keywords

- Instagram
- Adolescents
- Social Media
- Self-esteem

## Funcionalidades principales

- Carga dinámica de CSV local.
- Lectura opcional desde URL RAW de GitHub.
- Uso de CSV incluido en el proyecto.
- Métricas generales del dataset.
- Filtros por año, tipo de documento y búsqueda textual.
- Evolución de publicaciones por año.
- Citas acumuladas por año.
- Revistas o fuentes más frecuentes.
- Distribución por tipo de documento.
- Disponibilidad de acceso abierto.
- Artículos más citados.
- Autores con mayor presencia.
- Análisis de términos asociados a autoestima, adolescentes, redes sociales e Instagram.
- Frecuencia de keywords y palabras en abstracts.
- Tabla filtrable y descarga del dataset filtrado.

## Estructura modular

```text
app.py
src/
  config.py
  data_loader.py
  preprocessing.py
  visualizations.py
  text_analysis.py
data/
  scopus_instagram_social_development.csv
requirements.txt
LICENSE
README.md
```

## Ejecución local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Despliegue en Streamlit Community Cloud

1. Subir este proyecto a GitHub.
2. Entrar a Streamlit Community Cloud.
3. Conectar el repositorio.
4. Seleccionar `app.py` como archivo principal.
5. Desplegar.

## Licencia

Este proyecto utiliza licencia MIT.
