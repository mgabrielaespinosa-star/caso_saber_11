# Evidencias Eduardo Palma

## 1) Clonar e instalar

### Clonar repositorio

```bash
gh repo clone mgabrielaespinosa-star/caso_saber_11
```

![alt text](evidencias_reproducibilidad/edu-clone.png)

### cd caso_saber_11

![alt text](evidencias_reproducibilidad/edu-clone-succesfully.png)

### creación de doc de reproducibilidad

![alt text](evidencias_reproducibilidad/edu-docFile.png)

### Ajustar versión a 3.12.14

![alt text](evidencias_reproducibilidad/edu-install-Python-3-12-14.png)

### pip install -r requirements.txt

![alt text](evidencias_reproducibilidad/edu-Requirements.png)
Successfully installed



## 2) (Opcional) Re-entrenar el modelo — regenera model/model.pkl y metadata.json
```bash
python train.py
```

![alt text](evidencias_reproducibilidad/edu-ejecucion-train.png)



## 3) Levantar la API
```bash
uvicorn app.main:app --reload --port 8000
```

![alt text](evidencias_reproducibilidad/edu-Uvicorn.png)


### → documentación interactiva en http://localhost:8000/docs

![alt text](evidencias_reproducibilidad/edu-swagger-docs.png)


## 4) Probar

### health

```bash
curl http://localhost:8000/health
```

![alt text](evidencias_reproducibilidad/edu-curl-health.png)

### predict

```bash
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
```

![alt text](evidencias_reproducibilidad/edu-curl-predict.png)



## 5) Correr las pruebas
```bash
python -m pytest -v
```

![alt text](evidencias_reproducibilidad/edu-pytest.png)
