
import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# CONFIGURACIÓN DE LA APLICACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Dashboard - Big Data",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# CARGA DEL CONJUNTO DE DATOS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RUTA_DATOS = (
    BASE_DIR
    / "data"
    / "processed"
    / "connacionales_procesados.parquet"
)

@st.cache_data
def cargar_datos():
    return pd.read_parquet(RUTA_DATOS)

df = cargar_datos()

# Crear grupos de edad
df["Grupo de edad"] = pd.cut(
    df["Edad (años)"],
    bins=[24, 28, 32, 36, 40],
    labels=["25-28 años", "29-32 años", "33-36 años", "37-40 años"]
)

# --------------------------------------------------
# ENCABEZADO PRINCIPAL
# --------------------------------------------------

st.title("📊 Dashboard - Colombianos en el Exterior")

st.markdown("""
### Proyecto Final de Big Data

Aplicación interactiva para explorar los registros de colombianos
en el exterior mediante análisis de datos, visualizaciones y
modelos de Machine Learning.
""")

st.divider()

# --------------------------------------------------
# MENÚ DE NAVEGACIÓN
# --------------------------------------------------

seccion = st.sidebar.selectbox(
    "Selecciona una sección:",
    [
        "Resumen general",
        "Análisis geográfico",
        "Análisis demográfico",
        "Machine Learning",
        "MongoDB"
    ]
)

# --------------------------------------------------
# RESUMEN GENERAL
# --------------------------------------------------

if seccion == "Resumen general":

    st.header("Resumen general")

    st.success("Conjunto de datos cargado correctamente.")

    st.subheader("Indicadores generales")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total de registros",
        f"{len(df):,}".replace(",", ".")
    )

    col2.metric(
        "Total de columnas",
        len(df.columns)
    )

    col3.metric(
        "Edad promedio",
        f"{df['Edad (años)'].mean():.1f} años"
    )

    col4.metric(
        "Continentes",
        df["Continente"].nunique()
    )

    st.subheader("Vista previa de los datos")

    st.dataframe(df.head(), use_container_width=True)


# --------------------------------------------------
# ANÁLISIS GEOGRÁFICO
# --------------------------------------------------

elif seccion == "Análisis geográfico":

    st.header("Análisis geográfico")

    st.subheader("Distribución de colombianos por continente")

    distribucion_continentes = (
        df["Continente"]
        .value_counts()
        .reset_index()
    )

    distribucion_continentes.columns = [
        "Continente",
        "Total de personas"
    ]

    st.bar_chart(
        distribucion_continentes,
        x="Continente",
        y="Total de personas",
        color="#2F75B5"
    )

    st.dataframe(
        distribucion_continentes,
        hide_index=True,
        use_container_width=True
    )

    st.divider()

    st.subheader("Top 10 países con más colombianos registrados")

    top_paises = (
        df["País"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_paises.columns = [
        "País",
        "Total de personas"
    ]

    st.bar_chart(
        top_paises,
        x="País",
        y="Total de personas",
        color="#2F75B5",
        horizontal=True
    )

    st.dataframe(
        top_paises,
        hide_index=True,
        use_container_width=True
    )


# --------------------------------------------------
# ANÁLISIS DEMOGRÁFICO
# --------------------------------------------------

elif seccion == "Análisis demográfico":

    st.header("Análisis demográfico")

    st.subheader("Distribución de colombianos por grupo de edad")

    distribucion_edades = (
        df["Grupo de edad"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    distribucion_edades.columns = [
        "Grupo de edad",
        "Total de personas"
    ]

    st.bar_chart(
        distribucion_edades,
        x="Grupo de edad",
        y="Total de personas",
        color="#2F75B5"
    )

    st.dataframe(
        distribucion_edades,
        hide_index=True,
        use_container_width=True
    )

    st.divider()

    st.subheader("Distribución por continente y grupo de edad")

    distribucion_continente_edad = (
        df.groupby(
            ["Continente", "Grupo de edad"],
            observed=False
        )
        .size()
        .reset_index(name="Total de personas")
    )

    tabla_continente_edad = distribucion_continente_edad.pivot(
        index="Continente",
        columns="Grupo de edad",
        values="Total de personas"
    ).fillna(0)

    st.bar_chart(tabla_continente_edad)

    st.dataframe(
        tabla_continente_edad,
        use_container_width=True
    )


# --------------------------------------------------
# MACHINE LEARNING
# --------------------------------------------------

elif seccion == "Machine Learning":

    st.header("🤖 Análisis de Machine Learning")

    st.markdown("""
    En esta sección se presentan los resultados obtenidos
    durante el entrenamiento y evaluación de los modelos
    de clasificación utilizados para predecir el continente.
    """)

    st.subheader("Comparación del rendimiento de los modelos")

    resultados_modelos = pd.DataFrame({
        "Modelo": [
            "Dummy Classifier",
            "Decision Tree",
            "Random Forest"
        ],
        "Accuracy": [0.4188, 0.3217, 0.3458],
        "Precision Macro": [0.0698, 0.2549, 0.2596],
        "Recall Macro": [0.1667, 0.3148, 0.3474],
        "F1-Score Macro": [0.0984, 0.2230, 0.2352]
    })

    st.dataframe(
        resultados_modelos,
        hide_index=True,
        use_container_width=True
    )

    st.bar_chart(
        resultados_modelos.set_index("Modelo")[
            ["Accuracy", "Precision Macro", "Recall Macro", "F1-Score Macro"]
        ]
    )

    st.divider()

    st.subheader("Modelo seleccionado")

    st.success("Random Forest fue seleccionado como el mejor modelo.")

    col1, col2, col3 = st.columns(3)

    col1.metric("Accuracy", "34.58%")
    col2.metric("Recall Macro", "34.74%")
    col3.metric("F1-Score Macro", "23.52%")

    st.info("""
    Random Forest fue seleccionado porque obtuvo el mejor
    resultado en F1-Score macro y Recall macro frente a los
    otros modelos evaluados. Esto permite considerar el
    rendimiento en las diferentes clases, teniendo en cuenta
    el desbalance de los datos.
    """)

    st.divider()

    st.subheader("Matriz de confusión - Random Forest")

    RUTA_MATRIZ = (
        BASE_DIR
        / "reports"
        / "graficas"
        / "grafica_6.png"
    )

    st.image(
        str(RUTA_MATRIZ),
        caption="Matriz de confusión del modelo Random Forest",
        use_container_width=True
    )


# --------------------------------------------------
# MONGODB
# --------------------------------------------------

elif seccion == "MongoDB":

    st.header("🍃 Integración con MongoDB")

    st.markdown("""
    En esta sección se presentan los resultados almacenados
    en MongoDB Atlas durante la integración de la base de datos
    NoSQL con el proyecto de Big Data.
    """)

    st.subheader("Colecciones almacenadas")

    col1, col2, col3 = st.columns(3)

    col1.metric("Métricas de modelos", "3 registros")
    col2.metric("Hallazgos", "5 registros")
    col3.metric("Recomendaciones", "3 registros")

    st.write("Total de documentos almacenados: **11**")

    st.divider()

    st.subheader("Hallazgos principales")

    hallazgos = [
        "El conjunto de datos contiene 639.041 registros de colombianos en el exterior.",
        "España y Estados Unidos concentran la mayor cantidad de registros.",
        "Se evidencia una distribución desigual de los registros entre continentes.",
        "Los modelos de Machine Learning presentan dificultades para clasificar las clases minoritarias.",
        "Random Forest obtuvo el mejor F1-Score macro entre los modelos evaluados."
    ]

    for i, hallazgo in enumerate(hallazgos, start=1):
        st.write(f"**{i}.** {hallazgo}")

    st.divider()

    st.subheader("Recomendaciones")

    recomendaciones = [
        "Mantener actualizada la información de los colombianos registrados en el exterior.",
        "Mejorar el equilibrio entre las clases para fortalecer el rendimiento de los modelos de Machine Learning.",
        "Continuar evaluando diferentes algoritmos y técnicas para mejorar la clasificación de los continentes."
    ]

    for i, recomendacion in enumerate(recomendaciones, start=1):
        st.write(f"**{i}.** {recomendacion}")



