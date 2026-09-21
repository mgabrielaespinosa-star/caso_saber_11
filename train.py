"""Entrenamiento del modelo Saber 11 y serialización del pipeline completo.

Caso: ¿puede el contexto socioeconómico de un estudiante predecir si quedará
sobre o bajo la mediana nacional de matemáticas en la prueba Saber 11?

Produce:
    model/model.pkl       -> Pipeline completo (preprocesamiento + estimador)
    model/metadata.json   -> versiones, features, métricas y umbral del target

Uso:
    python train.py
"""

import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# ---------------------------------------------------------------------------
# Configuración (rutas relativas al proyecto: el script corre desde la raíz)
# ---------------------------------------------------------------------------
DATA_PATH = Path("data/saber11_muestra.parquet")
MODEL_DIR = Path("model")
SEED = 42

# Umbral del target: 51 puntos = mediana nacional de matemáticas del período
# 2022-4 (verificada en la exploración, notebooks/exploracion.ipynb). Se fija
# como constante para que la definición del target no dependa de la muestra
# (evita cualquier discusión de fuga de información en la etiqueta).
PUNTAJE_CORTE = 51

# Las 10 variables de contexto. Todas categóricas: por eso el preprocesamiento
# (OneHotEncoder) DEBE viajar dentro del pipeline serializado.
FEATURES = [
    "fami_estratovivienda",
    "fami_educacionmadre",
    "fami_educacionpadre",
    "fami_tieneinternet",
    "fami_tienecomputador",
    "cole_naturaleza",
    "cole_area_ubicacion",
    "cole_jornada",
    "estu_genero",
    "estu_depto_reside",
]
TARGET = "rendimiento_alto"


def cargar_datos() -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_parquet(DATA_PATH)
    # Los datos socioeconómicos son autorreportados: los vacíos se conservan
    # como categoría propia ("Sin dato") porque no responder también informa.
    df[FEATURES] = df[FEATURES].fillna("Sin dato").astype(str)
    df[TARGET] = (df["punt_matematicas"] >= PUNTAJE_CORTE).astype(int)
    return df[FEATURES], df[TARGET]


def construir_pipeline(estimador) -> Pipeline:
    pre = ColumnTransformer(
        [("cat", OneHotEncoder(handle_unknown="ignore"), FEATURES)]
    )
    return Pipeline([("pre", pre), ("clf", estimador)])


def main() -> None:
    X, y = cargar_datos()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=SEED
    )
    print(f"Datos: {len(X):,} filas | train {len(X_train):,} / test {len(X_test):,}")
    print(f"Balance del target (1 = sobre la mediana): {y.mean():.3f}\n")

    candidatos = {
        "logistic_regression": LogisticRegression(max_iter=1000, random_state=SEED),
        "random_forest": RandomForestClassifier(
            n_estimators=200, max_depth=12, class_weight="balanced",
            n_jobs=-1, random_state=SEED,
        ),
    }

    resultados = {}
    for nombre, est in candidatos.items():
        pipe = construir_pipeline(est)
        pipe.fit(X_train, y_train)
        proba = pipe.predict_proba(X_test)[:, 1]
        pred = pipe.predict(X_test)
        resultados[nombre] = {
            "pipeline": pipe,
            "roc_auc": round(float(roc_auc_score(y_test, proba)), 4),
            "f1": round(float(f1_score(y_test, pred)), 4),
        }
        print(f"--- {nombre} ---")
        print(f"ROC AUC: {resultados[nombre]['roc_auc']} | F1: {resultados[nombre]['f1']}")
        print(classification_report(y_test, pred, digits=3))

    # Selección por ROC AUC: con clases balanceadas (~51/49) y un problema de
    # ranking de riesgo, AUC compara los modelos de forma independiente del
    # umbral; F1 se reporta como métrica de operación en el punto de corte 0.5.
    ganador = max(resultados, key=lambda k: resultados[k]["roc_auc"])
    pipe_final = resultados[ganador]["pipeline"]
    print(f"Modelo seleccionado: {ganador}")

    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(pipe_final, MODEL_DIR / "model.pkl")

    metadata = {
        "modelo": ganador,
        "target": TARGET,
        "definicion_target": f"punt_matematicas >= {PUNTAJE_CORTE} (mediana nacional 2022-4)",
        "features": FEATURES,
        "metricas_test": {
            n: {"roc_auc": r["roc_auc"], "f1": r["f1"]} for n, r in resultados.items()
        },
        "seleccion": "mayor ROC AUC en el conjunto de test",
        "n_filas_entrenamiento": len(X_train),
        "semilla": SEED,
        "sklearn": sklearn.__version__,
        "python": platform.python_version(),
        "entrenado_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    with open(MODEL_DIR / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    tamano = (MODEL_DIR / "model.pkl").stat().st_size / 1e6
    print(f"\nGuardado model/model.pkl ({tamano:.1f} MB) y model/metadata.json")


if __name__ == "__main__":
    main()
