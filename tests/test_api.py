"""Pruebas automatizadas de la API (TestClient de FastAPI).

Se ejecutan desde la raíz del proyecto:  pytest
El TestClient levanta la aplicación completa —incluido el lifespan que carga
model/model.pkl— sin necesidad de un servidor corriendo.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

ESTUDIANTE_VULNERABLE = {
    "fami_estratovivienda": "Estrato 2",
    "fami_educacionmadre": "Secundaria (Bachillerato) completa",
    "fami_educacionpadre": "Primaria incompleta",
    "fami_tieneinternet": "No",
    "fami_tienecomputador": "No",
    "cole_naturaleza": "OFICIAL",
    "cole_area_ubicacion": "RURAL",
    "cole_jornada": "MAÑANA",
    "estu_genero": "F",
    "estu_depto_reside": "CAUCA",
}

ESTUDIANTE_FAVORECIDO = {
    "fami_estratovivienda": "Estrato 5",
    "fami_educacionmadre": "Educación profesional completa",
    "fami_educacionpadre": "Educación profesional completa",
    "fami_tieneinternet": "Si",
    "fami_tienecomputador": "Si",
    "cole_naturaleza": "NO OFICIAL",
    "cole_area_ubicacion": "URBANO",
    "cole_jornada": "COMPLETA",
    "estu_genero": "M",
    "estu_depto_reside": "BOGOTÁ",
}


@pytest.fixture(scope="module")
def client():
    # El "with" activa el lifespan: el modelo se carga una vez para el módulo.
    with TestClient(app) as c:
        yield c


def test_health_reporta_modelo_cargado(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "model_loaded": True}


def test_model_info_expone_metadatos(client):
    r = client.get("/model-info")
    assert r.status_code == 200
    meta = r.json()
    assert meta["modelo"] == "logistic_regression"
    assert len(meta["features"]) == 10
    assert "roc_auc" in meta["metricas_test"]["logistic_regression"]


def test_predict_devuelve_prediccion_valida(client):
    r = client.post("/predict", json=ESTUDIANTE_VULNERABLE)
    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["rendimiento_alto"] in (0, 1)
    assert 0.0 <= cuerpo["probabilidad"] <= 1.0
    assert cuerpo["version_sklearn"]
    assert cuerpo["timestamp_utc"]


def test_predict_captura_la_brecha_socioeconomica(client):
    """El contexto favorecido debe tener mayor probabilidad que el vulnerable."""
    p_vuln = client.post("/predict", json=ESTUDIANTE_VULNERABLE).json()["probabilidad"]
    p_fav = client.post("/predict", json=ESTUDIANTE_FAVORECIDO).json()["probabilidad"]
    assert p_fav > p_vuln


def test_predict_batch_respeta_el_orden(client):
    lote = {"estudiantes": [ESTUDIANTE_VULNERABLE, ESTUDIANTE_FAVORECIDO]}
    r = client.post("/predict-batch", json=lote)
    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["n"] == 2
    # mismo orden que la entrada: el primero es el vulnerable (menor probabilidad)
    assert cuerpo["predicciones"][0]["probabilidad"] < cuerpo["predicciones"][1]["probabilidad"]


def test_entrada_invalida_devuelve_422(client):
    invalido = {**ESTUDIANTE_VULNERABLE, "fami_estratovivienda": "Estrato 99"}
    r = client.post("/predict", json=invalido)
    assert r.status_code == 422


def test_campo_faltante_devuelve_422(client):
    incompleto = {k: v for k, v in ESTUDIANTE_VULNERABLE.items() if k != "estu_genero"}
    r = client.post("/predict", json=incompleto)
    assert r.status_code == 422
