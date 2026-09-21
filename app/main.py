"""API de inferencia Saber 11 — FastAPI.

Sirve el pipeline serializado en model/model.pkl. El modelo se carga UNA sola
vez al iniciar la aplicación (evento lifespan); las funciones de predicción
solo lo consultan.
"""

import json
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse


class UTF8JSONResponse(JSONResponse):
    """JSON con charset explícito: los navegadores muestran los tildes bien."""

    media_type = "application/json; charset=utf-8"

from app.schemas import Estudiante, LoteEstudiantes, Prediccion, PrediccionLote

MODEL_PATH = Path("model/model.pkl")
METADATA_PATH = Path("model/metadata.json")

ARTIFACTS: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    ARTIFACTS["model"] = joblib.load(MODEL_PATH)
    ARTIFACTS["metadata"] = json.loads(METADATA_PATH.read_text())
    yield
    ARTIFACTS.clear()


app = FastAPI(
    title="API Saber 11 · UAI",
    description=(
        "¿Puede el contexto socioeconómico de un estudiante predecir si quedará "
        "sobre o bajo la mediana nacional de matemáticas en la prueba Saber 11? "
        "Modelo de clasificación servido como API. Tarea final · Cloud Computing · "
        "Diploma en Data Science UAI 2026."
    ),
    version="1.0.0",
    lifespan=lifespan,
    default_response_class=UTF8JSONResponse,
)


def _predecir_df(df: pd.DataFrame) -> list[Prediccion]:
    """Aplica el pipeline a un DataFrame y arma la respuesta por fila."""
    meta = ARTIFACTS["metadata"]
    try:
        probas = ARTIFACTS["model"].predict_proba(df)[:, 1]
    except Exception:
        # Nunca exponer el traceback al cliente: 500 con mensaje controlado.
        raise HTTPException(status_code=500, detail="Error al generar la predicción")
    ahora = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return [
        Prediccion(
            rendimiento_alto=int(p >= 0.5),
            probabilidad=round(float(p), 4),
            modelo=meta["modelo"],
            version_sklearn=meta["sklearn"],
            timestamp_utc=ahora,
        )
        for p in probas
    ]


@app.get("/", include_in_schema=False)
def home():
    """Puerta de entrada: orienta a quien llega a la raíz del servicio."""
    return {
        "servicio": "API Saber 11 · UAI",
        "mensaje": "API de predicción funcionando. Documentación interactiva en /docs",
        "endpoints": ["/health", "/model-info", "/predict", "/predict-batch", "/docs"],
    }


@app.get("/health")
def health():
    """Estado del servicio y confirmación de que el modelo está en memoria."""
    return {"status": "ok", "model_loaded": "model" in ARTIFACTS}


@app.get("/model-info")
def model_info():
    """Metadatos del modelo: estimador, features esperadas, métricas, versión."""
    if "metadata" not in ARTIFACTS:
        raise HTTPException(status_code=503, detail="Modelo no cargado")
    return ARTIFACTS["metadata"]


@app.post("/predict", response_model=Prediccion)
def predict(estudiante: Estudiante):
    """Predicción para un estudiante. Entrada inválida → 422 (Pydantic)."""
    df = pd.DataFrame([estudiante.model_dump()])
    return _predecir_df(df)[0]


@app.post("/predict-batch", response_model=PrediccionLote)
def predict_batch(lote: LoteEstudiantes):
    """Predicciones para una lista de estudiantes, en el mismo orden."""
    df = pd.DataFrame([e.model_dump() for e in lote.estudiantes])
    preds = _predecir_df(df)
    return PrediccionLote(predicciones=preds, n=len(preds))
