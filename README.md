# Proyecto Final de Big Data
## Análisis de colombianos inscritos en el Registro Ciudadano en Línea

**Autor:** Mateo Bermejo

## Descripción
Proyecto de Big Data orientado al procesamiento, análisis y visualización de los registros de colombianos en el exterior.

## Tecnologías utilizadas
- Python
- Pandas y PySpark
- MongoDB Atlas
- Scikit-learn
- Streamlit
- Docker

## Estructura del proyecto
- `data/`: datos procesados.
- `notebooks/`: desarrollo y análisis.
- `src/`: scripts del proyecto.
- `models/`: modelo de Machine Learning.
- `reports/`: informe PDF y gráficas.
- `app/`: dashboard interactivo y Dockerfile.

## Ejecución del proyecto

### Requisitos
- Docker Desktop instalado y en ejecución.

### Iniciar el dashboard

Desde la carpeta principal del proyecto, ejecutar:

```bash
docker compose up --build

```

Luego abrir en el navegador:

http://localhost:8502

### Detener el proyecto

```bash
docker compose down
```