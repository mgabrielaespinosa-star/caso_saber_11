# Origen del dataset

**Fuente:** ICFES (Instituto Colombiano para la Evaluación de la Educación) · "Resultados únicos Saber 11" · Portal de datos abiertos del Estado colombiano (plataforma Socrata).

- Página del dataset: https://www.datos.gov.co/d/kgxf-xxbe
- API: https://www.datos.gov.co/resource/kgxf-xxbe.json

**Muestra de trabajo:** 150.000 estudiantes del período 2022-4 (`saber11_muestra.parquet`), extraída con `$select` para traer SOLO las columnas que el modelo necesita — minimización de datos: ningún cuasi-identificador (ID de estudiante, fecha de nacimiento, colegio, municipio) entra al pipeline.

**Cómo re-obtenerla** (una llamada a la API pública, sin autenticación):

```
https://www.datos.gov.co/resource/kgxf-xxbe.csv?$select=periodo,punt_matematicas,punt_ingles,fami_estratovivienda,fami_educacionmadre,fami_educacionpadre,fami_tieneinternet,fami_tienecomputador,cole_naturaleza,cole_area_ubicacion,cole_jornada,estu_genero,estu_depto_reside&$where=periodo='20224'&$order=:id&$limit=150000
```

**Licencia:** datos abiertos del Estado colombiano, uso público con cita de la fuente.
