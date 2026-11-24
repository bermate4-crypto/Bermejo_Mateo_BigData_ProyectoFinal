
from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    precision_score,
    recall_score,
    f1_score
)

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

RUTA_PARQUET = (
    BASE_DIR
    / "data"
    / "processed"
    / "connacionales_procesados.parquet"
)

CARPETA_MODELOS = BASE_DIR / "models"
RUTA_MODELO = CARPETA_MODELOS / "modelo_random_forest.pkl"

# 1. Cargar datos procesados
print("CARGANDO DATOS PROCESADOS...")

df_visual = pd.read_parquet(RUTA_PARQUET)

print("Registros:", f"{len(df_visual):,}")

# 2. Definir variables predictoras
columnas_numericas = [
    "Edad (años)",
    "Año_Registro"
]

columnas_categoricas = [
    "Área Conocimiento",
    "Nivel Académico",
    "Estado civil",
    "Sexo",
    "Pertenencia étnica"
]

columnas_modelo = (
    columnas_numericas
    + columnas_categoricas
    + ["Continente"]
)

# 3. Preparar conjunto de datos
df_ml = df_visual[
    df_visual["Continente"] != "NO IDENTIFICADO"
].copy()

df_ml = df_ml.dropna(subset=columnas_modelo)

X = df_ml[columnas_numericas + columnas_categoricas]
y = df_ml["Continente"]

print("\nCONJUNTO DE DATOS PREPARADO")
print("Registros:", f"{len(df_ml):,}")
print("Variables predictoras:", X.shape[1])
print("Clases:", y.nunique())

# 4. Dividir datos para entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nDIVISIÓN DE DATOS COMPLETADA")
print("Entrenamiento:", f"{len(X_train):,}")
print("Prueba:", f"{len(X_test):,}")

# 5. Configurar preprocesamiento
preprocesador = ColumnTransformer(
    transformers=[
        ("numericas", StandardScaler(), columnas_numericas),
        (
            "categoricas",
            OneHotEncoder(handle_unknown="ignore"),
            columnas_categoricas
        )
    ]
)

# 6. Configurar modelo Random Forest
modelo_random_forest = Pipeline(steps=[
    ("preprocesamiento", preprocesador),
    ("clasificador", RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_leaf=10,
        class_weight="balanced_subsample",
        random_state=42,
        n_jobs=-1
    ))
])

# 7. Entrenar modelo
print("\nENTRENANDO RANDOM FOREST...")

modelo_random_forest.fit(X_train, y_train)

# 8. Evaluar modelo
predicciones_rf = modelo_random_forest.predict(X_test)

accuracy_rf = accuracy_score(y_test, predicciones_rf)
precision_rf = precision_score(
    y_test, predicciones_rf, average="macro", zero_division=0
)
recall_rf = recall_score(
    y_test, predicciones_rf, average="macro", zero_division=0
)
f1_rf = f1_score(
    y_test, predicciones_rf, average="macro", zero_division=0
)

print("\nRESULTADOS DE RANDOM FOREST")
print("--------------------------------")
print("Accuracy:", round(accuracy_rf, 4))
print("Precisión macro:", round(precision_rf, 4))
print("Recall macro:", round(recall_rf, 4))
print("F1 macro:", round(f1_rf, 4))

print("\nREPORTE DE CLASIFICACIÓN:")
print(classification_report(
    y_test,
    predicciones_rf,
    zero_division=0
))

# 9. Guardar modelo entrenado
CARPETA_MODELOS.mkdir(parents=True, exist_ok=True)

joblib.dump(modelo_random_forest, RUTA_MODELO)

print("\nMODELO GUARDADO CORRECTAMENTE")
print("Ruta:", RUTA_MODELO)
