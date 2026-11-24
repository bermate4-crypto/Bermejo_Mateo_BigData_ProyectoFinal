
from pathlib import Path
import pandas as pd
import pycountry_convert as pc

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

RUTA_CSV = (
    BASE_DIR
    / "Data3"
    / "Connacionales_inscritos_en_el_Registro_Ciudadano_en_Línea_20261117.csv"
)

CARPETA_PROCESADOS = BASE_DIR / "data" / "processed"
RUTA_PARQUET = CARPETA_PROCESADOS / "connacionales_procesados.parquet"

# 1. Cargar datos originales
print("CARGANDO DATASET ORIGINAL...")
df = pd.read_csv(RUTA_CSV, low_memory=False)

print("Registros originales:", f"{len(df):,}")

# 2. Limpieza inicial
df_etl = df.copy()

df_etl["Fecha de Registro"] = pd.to_datetime(
    df_etl["Fecha de Registro"],
    format="%Y-%m",
    errors="coerce"
)

fechas_atipicas = df_etl["Fecha de Registro"].dt.year == 1900

df_etl.loc[fechas_atipicas, "Fecha de Registro"] = pd.NaT

df_etl["Año_Registro"] = df_etl["Fecha de Registro"].dt.year

print("\nRESULTADOS DE LA LIMPIEZA")
print("Fechas del año 1900 tratadas:", fechas_atipicas.sum())
print("Fechas faltantes:", df_etl["Fecha de Registro"].isna().sum())
print("Localizaciones faltantes:", df_etl["Localización"].isna().sum())
print("Registros duplicados:", df_etl.duplicated().sum())

# 3. Preparación del enriquecimiento geográfico
paises_enriquecimiento = (
    df_etl[["País", "Código ISO país"]]
    .drop_duplicates()
    .sort_values("País")
    .reset_index(drop=True)
)

# 4. Obtener continente mediante códigos ISO
def obtener_continente(codigo_iso):
    try:
        codigo_pais = pc.country_alpha3_to_country_alpha2(codigo_iso)
        codigo_continente = pc.country_alpha2_to_continent_code(codigo_pais)

        continentes = {
            "AF": "ÁFRICA",
            "AS": "ASIA",
            "EU": "EUROPA",
            "NA": "AMÉRICA DEL NORTE",
            "SA": "AMÉRICA DEL SUR",
            "OC": "OCEANÍA",
            "AN": "ANTÁRTIDA"
        }

        return continentes.get(codigo_continente, "NO IDENTIFICADO")

    except Exception:
        return "NO IDENTIFICADO"


paises_enriquecimiento["Continente"] = (
    paises_enriquecimiento["Código ISO país"]
    .apply(obtener_continente)
)

# 5. Correcciones geográficas especiales
correcciones_continente = {
    "KOSOVO": "EUROPA",
    "ST. MAARTEN": "AMÉRICA DEL NORTE"
}

for pais, continente in correcciones_continente.items():
    paises_enriquecimiento.loc[
        paises_enriquecimiento["País"] == pais,
        "Continente"
    ] = continente

# 6. Incorporar continente al DataFrame principal
df_etl = df_etl.drop(columns=["Continente"], errors="ignore")

df_etl = df_etl.merge(
    paises_enriquecimiento[["País", "Continente"]],
    on="País",
    how="left"
)

# 7. Crear variables derivadas

df_etl["Grupo_Edad"] = pd.cut(
    df_etl["Edad (años)"],
    bins=[24, 30, 35, 40],
    labels=["25-30", "31-35", "36-40"]
)

df_etl["Decada_Registro"] = (
    (df_etl["Año_Registro"] // 10) * 10
).astype("Int64")

df_etl["Total_Personas"] = df_etl["Cantidad de personas"]

print("\nVARIABLES DERIVADAS CREADAS")
print("Total de personas:", df_etl["Total_Personas"].sum())

print("\nDISTRIBUCIÓN DE PERSONAS POR CONTINENTE:")

print(
    df_etl.groupby("Continente", dropna=False)["Total_Personas"]
    .sum()
    .sort_values(ascending=False)
)

print("\nValores sin continente:", df_etl["Continente"].isna().sum())

# 7. Guardar dataset procesado
CARPETA_PROCESADOS.mkdir(parents=True, exist_ok=True)

df_etl.to_parquet(
    RUTA_PARQUET,
    engine="pyarrow",
    index=False
)

print("\nETL COMPLETADO")
print("Registros:", f"{len(df_etl):,}")
print("Columnas:", len(df_etl.columns))
print("Archivo generado:", RUTA_PARQUET)
print("Tamaño:", round(RUTA_PARQUET.stat().st_size / (1024**2), 2), "MB")
