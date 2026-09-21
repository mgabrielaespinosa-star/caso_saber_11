# Evidencia de ejecución en localhost

Servicio levantado con: `uvicorn app.main:app --port 8000` · 21-09-2026 18:58 (hora Chile)

## 1 · Predicción exitosa (POST /predict)
```
$ curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d @estudiante.json
{
    "rendimiento_alto": 0,
    "probabilidad": 0.1979,
    "modelo": "logistic_regression",
    "version_sklearn": "1.9.1",
    "timestamp_utc": "2026-09-21T21:58:34+00:00"
}
```

## 2 · Predicción por lote (POST /predict-batch)
```
{
    "predicciones": [
        {
            "rendimiento_alto": 0,
            "probabilidad": 0.1979,
            "modelo": "logistic_regression",
            "version_sklearn": "1.9.1",
            "timestamp_utc": "2026-09-21T21:58:34+00:00"
        },
        {
            "rendimiento_alto": 1,
            "probabilidad": 0.8585,
            "modelo": "logistic_regression",
            "version_sklearn": "1.9.1",
            "timestamp_utc": "2026-09-21T21:58:34+00:00"
        }
    ],
    "n": 2
}
```

## 3 · Entrada inválida → 422 (estrato fuera de catálogo)
```
$ curl -X POST /predict con "fami_estratovivienda": "Estrato 99"
{
    "detail": [
        {
            "type": "literal_error",
            "loc": [
                "body",
                "fami_estratovivienda"
            ],
            "msg": "Input should be 'Estrato 1', 'Estrato 2', 'Estrato 3', 'Estrato 4', 'Estrato 5', 'Estrato 6', 'Sin Estrato' or 'Sin dato'",
            "input": "Estrato 99",
            "ctx": {
                "expected": "'Estrato 1', 'Estrato 2', 'Estrato 3', 'Estrato 4', 'Estrato 5', 'Estrato 6', 'Sin Estrato' or 'Sin dato'"
            }
        }
    ]
}
HTTP status: 422
```

## 4 · Salida de pytest
Ver `pytest_salida.txt` en esta carpeta: **7 passed** en 0,86 s.
