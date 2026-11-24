
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
    Table,
    TableStyle
)

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
CARPETA_GRAFICAS = BASE_DIR / "reports" / "graficas"
RUTA_PDF = BASE_DIR / "reports" / "informe_final_big_data.pdf"

# Configuración del documento
documento = SimpleDocTemplate(
    str(RUTA_PDF),
    pagesize=A4,
    rightMargin=2 * cm,
    leftMargin=2 * cm,
    topMargin=2 * cm,
    bottomMargin=2 * cm
)

# Estilos iniciales
estilos = getSampleStyleSheet()

estilos.add(ParagraphStyle(
    name="TituloProyecto",
    parent=estilos["Title"],
    fontSize=20,
    leading=26,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#17365D"),
    spaceAfter=20
))

estilos.add(ParagraphStyle(
    name="Subtitulo",
    parent=estilos["Heading2"],
    fontSize=14,
    leading=18,
    textColor=colors.HexColor("#2F75B5"),
    spaceBefore=12,
    spaceAfter=10
))

estilos.add(ParagraphStyle(
    name="TextoInforme",
    parent=estilos["BodyText"],
    fontSize=10,
    leading=15,
    alignment=TA_JUSTIFY,
    spaceAfter=8
))

# Contenido del documento
contenido = []

print("Configuración inicial del informe completada.")
print(f"Carpeta de gráficas: {CARPETA_GRAFICAS}")
print(f"PDF de salida: {RUTA_PDF}")


# --------------------------------------------------
# PORTADA DEL INFORME
# --------------------------------------------------

contenido.append(Spacer(1, 3 * cm))

contenido.append(Paragraph(
    "ANÁLISIS DE COLOMBIANOS EN EL EXTERIOR",
    estilos["TituloProyecto"]
))

contenido.append(Spacer(1, 1 * cm))

contenido.append(Paragraph(
    "Proyecto Final de Big Data",
    estilos["Subtitulo"]
))

contenido.append(Spacer(1, 1 * cm))

contenido.append(Paragraph(
    "Procesamiento de datos, análisis exploratorio, "
    "modelos de Machine Learning e integración con MongoDB.",
    estilos["TextoInforme"]
))

contenido.append(Spacer(1, 2 * cm))

contenido.append(Paragraph(
    "<b>Estudiante:</b> Mateo Bermejo",
    estilos["TextoInforme"]
))

contenido.append(Paragraph(
    "<b>Programa:</b> Ingeniería de Sistemas",
    estilos["TextoInforme"]
))

contenido.append(Paragraph(
    "<b>Institución:</b> Fundación Universitaria Los Libertadores",
    estilos["TextoInforme"]
))

contenido.append(Spacer(1, 2 * cm))

contenido.append(Paragraph(
    "2026",
    estilos["TextoInforme"]
))

contenido.append(PageBreak())


# --------------------------------------------------
# INTRODUCCIÓN Y OBJETIVOS
# --------------------------------------------------

contenido.append(Paragraph(
    "1. INTRODUCCIÓN",
    estilos["Subtitulo"]
))

contenido.append(Paragraph(
    "El presente proyecto desarrolla un proceso de análisis de datos "
    "sobre los colombianos registrados en el exterior, mediante la "
    "aplicación de herramientas y técnicas de Big Data. Se busca "
    "transformar los datos en información útil para comprender la "
    "distribución geográfica y demográfica de esta población.",
    estilos["TextoInforme"]
))

contenido.append(Paragraph(
    "Para ello, se implementaron procesos de extracción, transformación "
    "y carga (ETL), utilizando Python, Pandas y Apache Spark. También se "
    "realizó un análisis exploratorio, se construyeron agregaciones OLAP, "
    "se entrenaron modelos de Machine Learning y se integraron resultados "
    "en una base de datos MongoDB.",
    estilos["TextoInforme"]
))

contenido.append(Paragraph(
    "2. OBJETIVOS",
    estilos["Subtitulo"]
))

contenido.append(Paragraph(
    "<b>Objetivo general:</b> Aplicar técnicas y herramientas de Big Data "
    "para procesar y analizar información de colombianos registrados "
    "en el exterior, identificando patrones geográficos y demográficos.",
    estilos["TextoInforme"]
))

contenido.append(Paragraph(
    "<b>Objetivos específicos:</b>",
    estilos["TextoInforme"]
))

objetivos = [
    "Procesar y limpiar los datos mediante herramientas de Python y Spark.",
    "Realizar análisis exploratorios y visualizaciones para identificar patrones.",
    "Construir agregaciones OLAP para facilitar el análisis multidimensional.",
    "Entrenar y evaluar modelos de Machine Learning para predecir el continente.",
    "Almacenar y consultar métricas, hallazgos y recomendaciones en MongoDB."
]

for objetivo in objetivos:
    contenido.append(Paragraph(
        f"• {objetivo}",
        estilos["TextoInforme"]
    ))

contenido.append(Spacer(1, 0.5 * cm))


# --------------------------------------------------
# CONJUNTO DE DATOS Y PROCESO ETL
# --------------------------------------------------

contenido.append(Paragraph(
    "3. DESCRIPCIÓN DEL CONJUNTO DE DATOS",
    estilos["Subtitulo"]
))

contenido.append(Paragraph(
    "El conjunto de datos utilizado corresponde a los colombianos "
    "inscritos en el Registro Ciudadano en Línea, publicado en el "
    "portal de Datos Abiertos de Colombia. La información permite "
    "analizar características demográficas, académicas y geográficas "
    "de los ciudadanos registrados en el exterior.",
    estilos["TextoInforme"]
))

contenido.append(Paragraph(
    "<b>Fuente:</b> Datos Abiertos Colombia",
    estilos["TextoInforme"]
))

contenido.append(Paragraph(
    '<link href="https://www.datos.gov.co/Estad-sticas-Nacionales/'
    'Colombianos-en-el-exterior-de-25-a-40-a-os/3k8j-4d42" '
    'color="blue">Consultar conjunto de datos</link>',
    estilos["TextoInforme"]
))

contenido.append(Paragraph(
    "4. PROCESO ETL",
    estilos["Subtitulo"]
))

contenido.append(Paragraph(
    "El proceso ETL se desarrolló en tres etapas. En la extracción "
    "se obtuvo el conjunto de datos desde la fuente pública. En la "
    "transformación se realizó la limpieza, revisión de valores "
    "faltantes, adecuación de variables y preparación de los datos "
    "para el análisis. Finalmente, en la carga se almacenó la "
    "información procesada en formato Parquet.",
    estilos["TextoInforme"]
))

contenido.append(Paragraph(
    "Para estas actividades se utilizaron Pandas y Apache Spark, "
    "permitiendo trabajar con el conjunto de datos y preparar la "
    "información para las etapas posteriores del proyecto.",
    estilos["TextoInforme"]
))

contenido.append(Paragraph(
    "<b>Archivo procesado:</b> "
    "Data3/procesados/connacionales_procesados.parquet",
    estilos["TextoInforme"]
))

contenido.append(Spacer(1, 0.5 * cm))


# --------------------------------------------------
# ANÁLISIS EXPLORATORIO Y VISUALIZACIONES
# --------------------------------------------------

contenido.append(Paragraph(
    "5. ANÁLISIS EXPLORATORIO DE LOS DATOS",
    estilos["Subtitulo"]
))

contenido.append(Paragraph(
    "Se realizó un análisis exploratorio para identificar patrones "
    "en los registros de colombianos en el exterior. Mediante "
    "visualizaciones se examinaron la evolución temporal, la "
    "distribución geográfica y las características demográficas "
    "de la población estudiada.",
    estilos["TextoInforme"]
))

graficas = [
    (
        "grafica_1.png",
        "5.1. Evolución de los registros de colombianos en el exterior",
        "Esta visualización permite observar el comportamiento de los "
        "registros a través del tiempo e identificar sus variaciones."
    ),
    (
        "grafica_2.png",
        "5.2. Top 10 países con mayor cantidad de colombianos registrados",
        "Presenta los diez países con mayor número de colombianos "
        "registrados, permitiendo identificar los principales destinos."
    ),
    (
        "grafica_3.png",
        "5.3. Distribución de colombianos registrados por continente",
        "Muestra cómo se distribuyen los registros entre los diferentes "
        "continentes."
    ),
    (
        "grafica_4.png",
        "5.4. Distribución de colombianos registrados por grupo de edad",
        "Permite examinar la composición de la población según los "
        "grupos de edad considerados en el análisis."
    ),
    (
        "grafica_5.png",
        "5.5. Distribución de personas por continente y grupo de edad",
        "Relaciona la distribución geográfica con los grupos de edad, "
        "facilitando una comparación entre continentes."
    ),
    (
        "grafica_6.png",
        "5.6. Matriz de confusión del modelo Random Forest",
        "Permite comparar las clases reales con las predicciones "
        "realizadas por el modelo Random Forest y observar sus aciertos "
        "y errores de clasificación."
    ),
    (
        "grafica_7.png",
        "5.7. Comparación del rendimiento de los modelos",
        "Compara los resultados obtenidos por los modelos evaluados "
        "durante el proceso de Machine Learning."
    )
]

for nombre, titulo, descripcion in graficas:

    ruta_imagen = CARPETA_GRAFICAS / nombre

    contenido.append(Paragraph(
        titulo,
        estilos["Subtitulo"]
    ))

    contenido.append(Paragraph(
        descripcion,
        estilos["TextoInforme"]
    ))

    if ruta_imagen.exists():
        imagen = Image(
            str(ruta_imagen),
            width=16 * cm,
            height=9 * cm,
            kind="proportional"
        )

        contenido.append(imagen)
    else:
        contenido.append(Paragraph(
            f"No se encontró la imagen: {nombre}",
            estilos["TextoInforme"]
        ))

    contenido.append(PageBreak())


# --------------------------------------------------
# RESULTADOS DE MACHINE LEARNING
# --------------------------------------------------

contenido.append(Paragraph(
    "6. ENTRENAMIENTO Y EVALUACIÓN DE MODELOS",
    estilos["Subtitulo"]
))

contenido.append(Paragraph(
    "Se desarrollaron modelos de clasificación con el propósito de "
    "predecir el continente de residencia de los colombianos registrados. "
    "Para ello, se utilizaron variables demográficas y académicas como "
    "edad, año de registro, área de conocimiento, nivel académico, "
    "estado civil, sexo y pertenencia étnica.",
    estilos["TextoInforme"]
))

contenido.append(Paragraph(
    "El conjunto de datos utilizado para el entrenamiento estuvo "
    "conformado por 638.881 registros. La división se realizó mediante "
    "una estrategia estratificada, destinando el 80 % para entrenamiento "
    "y el 20 % para prueba.",
    estilos["TextoInforme"]
))

contenido.append(Paragraph(
    "<b>Distribución de los datos:</b> 511.104 registros de entrenamiento "
    "y 127.777 registros de prueba.",
    estilos["TextoInforme"]
))

contenido.append(Paragraph(
    "6.1. Comparación de los modelos",
    estilos["Subtitulo"]
))

contenido.append(Paragraph(
    "Se evaluaron tres modelos utilizando las métricas de exactitud "
    "(accuracy), precisión macro, recall macro y F1-score macro. "
    "Los resultados obtenidos fueron los siguientes:",
    estilos["TextoInforme"]
))

datos_modelos = [
    ["Modelo", "Accuracy", "Precisión macro", "Recall macro", "F1 macro"],
    ["Dummy Classifier", "0.4188", "0.0698", "0.1667", "0.0984"],
    ["Decision Tree", "0.3217", "0.2549", "0.3148", "0.2230"],
    ["Random Forest", "0.3458", "0.2596", "0.3474", "0.2352"]
]

tabla_modelos = Table(
    datos_modelos,
    colWidths=[3.2 * cm, 2.2 * cm, 2.8 * cm, 2.5 * cm, 2.0 * cm],
    repeatRows=1
)

tabla_modelos.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 8),
    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 8)
]))

contenido.append(tabla_modelos)
contenido.append(Spacer(1, 0.5 * cm))

contenido.append(Paragraph(
    "6.2. Modelo seleccionado: Random Forest",
    estilos["Subtitulo"]
))

contenido.append(Paragraph(
    "El modelo Random Forest obtuvo los mejores resultados en "
    "precisión macro (0.2596), recall macro (0.3474) y F1-score "
    "macro (0.2352), por lo que fue seleccionado como el modelo "
    "principal del proyecto. Su configuración incluyó 100 árboles, "
    "una profundidad máxima de 20, un mínimo de 10 muestras por hoja "
    "y el balanceo de clases mediante balanced_subsample.",
    estilos["TextoInforme"]
))

contenido.append(Paragraph(
    "Los resultados evidencian que existe un desequilibrio en la "
    "cantidad de registros entre continentes. Por esta razón, la "
    "exactitud por sí sola no representa suficientemente el "
    "desempeño del modelo. Se dio mayor importancia a las métricas "
    "macro para evaluar el comportamiento frente a las diferentes clases.",
    estilos["TextoInforme"]
))

contenido.append(Spacer(1, 0.5 * cm))


# --------------------------------------------------
# INTEGRACIÓN CON MONGODB
# --------------------------------------------------

contenido.append(Paragraph(
    "7. INTEGRACIÓN CON MONGODB ATLAS",
    estilos["Subtitulo"]
))

contenido.append(Paragraph(
    "Como parte de la solución, se implementó una integración con "
    "MongoDB Atlas, utilizando PyMongo para almacenar y consultar "
    "los resultados obtenidos durante el desarrollo del proyecto. "
    "Se creó la base de datos proyecto_bigdata, organizada en tres "
    "colecciones principales.",
    estilos["TextoInforme"]
))

contenido.append(Paragraph(
    "<b>metricas_modelos:</b> almacena las métricas de evaluación "
    "de los modelos de Machine Learning.",
    estilos["TextoInforme"]
))

contenido.append(Paragraph(
    "<b>hallazgos:</b> contiene los principales resultados identificados "
    "durante el análisis de los datos.",
    estilos["TextoInforme"]
))

contenido.append(Paragraph(
    "<b>recomendaciones:</b> registra las recomendaciones generadas "
    "a partir de los hallazgos del proyecto.",
    estilos["TextoInforme"]
))

contenido.append(Paragraph(
    "7.1. Resultados de la integración",
    estilos["Subtitulo"]
))

datos_mongodb = [
    ["Colección", "Documentos almacenados"],
    ["metricas_modelos", "3"],
    ["hallazgos", "5"],
    ["recomendaciones", "3"],
    ["Total", "11"]
]

tabla_mongodb = Table(
    datos_mongodb,
    colWidths=[8 * cm, 5 * cm]
)

tabla_mongodb.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("ALIGN", (1, 0), (1, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 8)
]))

contenido.append(tabla_mongodb)
contenido.append(Spacer(1, 0.5 * cm))

contenido.append(Paragraph(
    "También se realizaron consultas para ordenar los modelos según "
    "su F1-score macro, recuperar recomendaciones de prioridad alta "
    "y consultar hallazgos relacionados con Machine Learning. "
    "Estas operaciones permitieron verificar el almacenamiento "
    "y la recuperación de la información.",
    estilos["TextoInforme"]
))

contenido.append(Spacer(1, 0.5 * cm))


# --------------------------------------------------
# CONCLUSIONES Y RECOMENDACIONES
# --------------------------------------------------

contenido.append(Paragraph(
    "8. CONCLUSIONES",
    estilos["Subtitulo"]
))

conclusiones = [
    "El uso de herramientas de Big Data permitió procesar y analizar "
    "un conjunto amplio de registros de colombianos en el exterior, "
    "facilitando la identificación de patrones geográficos y demográficos.",

    "La aplicación de Pandas y Apache Spark permitió desarrollar "
    "actividades de limpieza, transformación y preparación de los datos "
    "para su posterior análisis.",

    "Las visualizaciones y agregaciones OLAP facilitaron la interpretación "
    "de la información desde diferentes perspectivas, como el tiempo, "
    "el continente, los países y los grupos de edad.",

    "Entre los modelos evaluados, Random Forest obtuvo el mejor "
    "desempeño en las métricas macro de precisión, recall y F1-score. "
    "Sin embargo, sus resultados muestran que todavía existen "
    "dificultades para clasificar correctamente todas las clases.",

    "La integración con MongoDB Atlas permitió almacenar y consultar "
    "métricas, hallazgos y recomendaciones, complementando el proceso "
    "de análisis con una solución de persistencia de datos."
]

for conclusion in conclusiones:
    contenido.append(Paragraph(
        f"• {conclusion}",
        estilos["TextoInforme"]
    ))

contenido.append(Paragraph(
    "9. RECOMENDACIONES",
    estilos["Subtitulo"]
))

recomendaciones = [
    "Incorporar nuevos registros y mantener actualizado el conjunto "
    "de datos para ampliar el análisis.",

    "Revisar el desequilibrio entre las clases para mejorar la capacidad "
    "de clasificación de los modelos de Machine Learning.",

    "Explorar técnicas adicionales de balanceo y ajuste de hiperparámetros "
    "para evaluar posibles mejoras en el rendimiento.",

    "Ampliar las visualizaciones y consultas para facilitar la exploración "
    "de los resultados por parte de los usuarios.",

    "Mantener organizados y actualizados los registros almacenados "
    "en MongoDB Atlas."
]

for recommendation in recomendaciones:
    contenido.append(Paragraph(
        f"• {recommendation}",
        estilos["TextoInforme"]
    ))

contenido.append(Spacer(1, 1 * cm))

contenido.append(Paragraph(
    "FIN DEL INFORME",
    estilos["TituloProyecto"]
))


# --------------------------------------------------
# GENERACIÓN DEL INFORME PDF
# --------------------------------------------------

documento.build(contenido)

print("----------------------------------------")
print("INFORME PDF GENERADO CORRECTAMENTE")
print(f"Ubicación: {RUTA_PDF}")
print("----------------------------------------")
