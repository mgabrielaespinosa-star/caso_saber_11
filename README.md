# saber11-api — del modelo entrenado al servicio en línea

> Tarea final · Cloud Computing · Diploma en Data Science UAI 2026

**¿Puede el contexto socioeconómico de un estudiante predecir su desempeño académico?**
Modelo de clasificación que predice si un estudiante quedará sobre o bajo la mediana nacional
de matemáticas en la prueba Saber 11 (Colombia), conociendo **solo su contexto**: estrato,
educación de los padres, internet y computador en casa, tipo de colegio, área, jornada,
género y departamento. Servido como API HTTP con FastAPI.

## 🌐 Servicio en línea

**URL pública:** <https://caso-saber-11.onrender.com> · Documentación interactiva: <https://caso-saber-11.onrender.com/docs>

```bash
curl https://caso-saber-11.onrender.com/health
# {"status":"ok","model_loaded":true}

curl -X POST https://caso-saber-11.onrender.com/predict -H "Content-Type: application/json" -d '{
  "fami_estratovivienda": "Estrato 2", "fami_educacionmadre": "Secundaria (Bachillerato) completa",
  "fami_educacionpadre": "Primaria incompleta", "fami_tieneinternet": "No", "fami_tienecomputador": "No",
  "cole_naturaleza": "OFICIAL", "cole_area_ubicacion": "RURAL", "cole_jornada": "MAÑANA",
  "estu_genero": "F", "estu_depto_reside": "CAUCA"}'
# {"rendimiento_alto":0,"probabilidad":0.1979,"modelo":"logistic_regression",...}
```

> Nota del plan gratuito: la instancia se suspende tras ~15 min sin tráfico; la primera
> visita siguiente tarda ~50 s en despertarla. Las siguientes responden al instante.

## Equipo

- Roxana Arriagada
- Sebastián Bórquez
- María Gabriela Espinosa
- Eduardo Palma
- Jairo Vega
- Iñaki Zúñiga

## Resultados

| Modelo | ROC AUC (test) | F1 (test) |
|---|---|---|
| **Regresión logística** (seleccionada) | **0,7377** | 0,691 |
| Random forest | 0,7319 | 0,676 |

**El hallazgo:** el contexto socioeconómico por sí solo — sin ninguna información académica
del estudiante — predice con ROC AUC 0,74. Un mismo perfil pasa de 19,8% a 85,9% de
probabilidad de quedar sobre la mediana al cambiar solo sus condiciones de contexto.
Y el modelo simple superó al complejo.

**Interpretación de resultados:** Alcanzar un ROC AUC de 0,74 nos deja algo muy en claro: el entorno del alumno pesa tanto que es posible predecir su desempeño sin siquiera evaluar sus conocimientos académicos. Pero el dato que más causa impacto es ese salto del 19,8% al 85,9%. Esto demuestra que, con el simple hecho de cambiar las condiciones económicas y tecnológicas de un alumno (como darle internet, un computador o pasar de colegio público a privado), sus chances de éxito aumentan en 66 puntos porcentuales aproximadamente. Los datos puros de la exploración lo respaldan: tener internet en casa sube el promedio de 46,3 a 52,7, y estudiar en un colegio privado marca 54,9 frente al 49,4 de uno público. En términos generales, el modelo evidencia con datos reales la notable desigualdad estructural del sistema educativo. Queda claro que estas variables exógenas impactan significativamente, demostrando que el mérito individual no es suficiente al momento de dar una prueba, sino que todo el contexto previo condiciona el resultado final.

## Estructura del repositorio

```
caso_saber_11/
├── app/
│   ├── main.py            # aplicación FastAPI (4 endpoints)
│   └── schemas.py         # contratos Pydantic de entrada y salida
├── model/
│   ├── model.pkl          # pipeline completo serializado (OneHot + reg. logística)
│   └── metadata.json      # versiones, features, métricas, definición del target
├── notebooks/
│   └── exploracion.ipynb  # EDA: brechas, nulos, construcción del target
├── tests/
│   └── test_api.py        # 7 pruebas automatizadas (TestClient)
├── docs/                  # evidencia: /docs, llamadas, salida de pytest
├── data/
│   ├── saber11_muestra.parquet  # 150.000 estudiantes, 13 columnas (772 KB)
│   └── README.md          # fuente, licencia y cómo re-obtener la muestra
├── train.py               # entrenamiento y serialización
├── requirements.txt · runtime.txt · Procfile
└── README.md
```

## Cómo reproducir todo el flujo

Requisito: Python 3.12 (la versión exacta está en `runtime.txt`).

```bash
# 1) Clonar e instalar
git clone https://github.com/mgabrielaespinosa-star/caso_saber_11.git
cd caso_saber_11
python3.12 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2) (Opcional) Re-entrenar el modelo — regenera model/model.pkl y metadata.json
python train.py

# 3) Levantar la API
uvicorn app.main:app --reload --port 8000
# → documentación interactiva en http://localhost:8000/docs

# 4) Probar
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{
  "fami_estratovivienda": "Estrato 2",
  "fami_educacionmadre": "Secundaria (Bachillerato) completa",
  "fami_educacionpadre": "Primaria incompleta",
  "fami_tieneinternet": "No",
  "fami_tienecomputador": "No",
  "cole_naturaleza": "OFICIAL",
  "cole_area_ubicacion": "RURAL",
  "cole_jornada": "MAÑANA",
  "estu_genero": "F",
  "estu_depto_reside": "CAUCA"
}'
# → {"rendimiento_alto":0,"probabilidad":0.1979,...}

# 5) Correr las pruebas
pytest
```

## Endpoints

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/health` | Estado del servicio y confirmación de modelo en memoria |
| GET | `/model-info` | Metadatos: estimador, features, métricas, versión |
| POST | `/predict` | Predicción para un estudiante (con probabilidad) |
| POST | `/predict-batch` | Predicciones para una lista, en el mismo orden |
| GET | `/docs` | Documentación interactiva (Swagger) |

Una entrada con campos faltantes, tipos incorrectos o categorías fuera de catálogo devuelve
**422** con el detalle; un fallo interno devuelve **500** con mensaje controlado.

## Pruebas automatizadas

`pytest` ejecuta 7 pruebas con el TestClient de FastAPI (salida completa en
`docs/pytest_salida.txt`):

```
tests/test_api.py::test_health_reporta_modelo_cargado PASSED
tests/test_api.py::test_model_info_expone_metadatos PASSED
tests/test_api.py::test_predict_devuelve_prediccion_valida PASSED
tests/test_api.py::test_predict_captura_la_brecha_socioeconomica PASSED
tests/test_api.py::test_predict_batch_respeta_el_orden PASSED
tests/test_api.py::test_entrada_invalida_devuelve_422 PASSED
tests/test_api.py::test_campo_faltante_devuelve_422 PASSED
======================== 7 passed in 0.86s ========================
```

Evidencia adicional en `docs/`: captura de `/docs` en el navegador y transcripción de las
llamadas exigidas (predicción exitosa, lote y entrada inválida con 422).

## Decisiones técnicas (criterios que el enunciado deja abiertos)

- **Target:** `rendimiento_alto` = puntaje de matemáticas ≥ **51** (mediana nacional del
  período 2022-4, verificada en la exploración). Se fija como constante para que la
  definición de la etiqueta no dependa de la muestra ni del split.
- **Pipeline completo serializado:** `ColumnTransformer(OneHotEncoder) + estimador` en un
  solo objeto. Las 10 features son categóricas: serializar solo el estimador habría
  obligado a replicar la codificación en la API (training–serving skew).
- **Selección de modelo:** mayor ROC AUC en test (métrica independiente del umbral,
  apropiada con clases balanceadas 51/49); F1 reportada como métrica de operación.
  Split estratificado 80/20 con semilla 42.
- **Categorías nuevas en producción:** `handle_unknown="ignore"` — un valor nunca visto
  no rompe el servicio.
- **Nulos:** categoría explícita "Sin dato" (no responder también informa; los
  estudiantes "Sin Estrato" promedian el peor puntaje).
- **Privacidad:** extracción con `$select` — ningún cuasi-identificador (ID, fecha de
  nacimiento, colegio, municipio) entra al pipeline. Detalle en `data/README.md`.

## Fuente de datos

**ICFES** (Instituto Colombiano para la Evaluación de la Educación) · *Resultados únicos
Saber 11* · Portal de datos abiertos del Estado colombiano.
Página: <https://www.datos.gov.co/d/kgxf-xxbe> · Cita completa, licencia y comando de
re-obtención en [`data/README.md`](data/README.md).

## Despliegue en Render (documentación del proceso)

**Elección del proveedor:** evaluamos Google Cloud Run (la nube del curso) vs. Render.
Elegimos **Render** porque lee nuestro contrato de entorno sin contenedorizar, su plan
gratuito no exige tarjeta de crédito (el enunciado recomienda evitarla) y trae deploy
continuo nativo — mínima fricción para el propósito. Cloud Run queda documentado como
alternativa viable si el servicio requiriera escala real.

**Configuración usada:** Web Service conectado a este repo (rama `main`) · Runtime
Python 3 · Build `pip install -r requirements.txt` · Start `uvicorn app.main:app
--host 0.0.0.0 --port $PORT` (la misma línea del `Procfile`) · Instancia Free ·
Variable de entorno `PYTHON_VERSION=3.12.14` para fijar el intérprete exacto con el
que se entrenó y serializó el modelo.

**Problemas encontrados y su solución:**

1. *El nombre del servicio no admitía guion bajo:* propusimos `caso_saber_11` (el nombre
   del repo) pero los hostnames no aceptan `_`. Solución: renombrar el servicio a
   `caso-saber-11`, que se convirtió en la URL pública.
2. *Versión de Python por defecto distinta a la de entrenamiento:* Render usa su Python
   más reciente si no se le indica otro, lo que arriesga la deserialización del `.pkl`
   (el descuento de −20 del enunciado). Solución preventiva: variable `PYTHON_VERSION=3.12.14`,
   verificada en el build log ("Installing Python 3.12.14") y en `/model-info`.
3. *Cold start del plan gratuito:* la instancia se suspende sin tráfico y la primera
   visita tarda ~50 s. Mitigación: está documentado aquí para el corrector, y el equipo
   verificará que el servicio esté despierto el día de la entrega, como pide el enunciado.

**Deploy continuo:** activado con la integración nativa de Render — cada push a `main`
reconstruye y publica automáticamente (este mismo README se publicó así: el commit que
lo agregó gatilló el deploy sin intervención manual).
