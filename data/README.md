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



**Diccionario de datos**

| Campo                  | Tipo de dato   | Tipo de variable | Descripción simple                                                    | Qué mide / representa                                                                     |
| ---------------------- | -------------- | ---------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `periodo`              | Entero / texto | Temporal         | Periodo en que el estudiante presentó la prueba Saber 11.             | Identifica el año y semestre de aplicación del examen.                                    |
| `punt_matematicas`     | Numérico       | Cuantitativa     | Puntaje obtenido por el estudiante en Matemáticas.                    | Mide el desempeño del estudiante en el área de Matemáticas en Saber 11.                   |
| `punt_ingles`          | Numérico       | Cuantitativa     | Puntaje obtenido por el estudiante en Inglés.                         | Mide el desempeño del estudiante en la prueba de Inglés.                                  |
| `fami_estratovivienda` | Categórico     | Ordinal          | Estrato socioeconómico de la vivienda del estudiante.                 | Permite aproximarse a las condiciones socioeconómicas del hogar donde vive el estudiante. |
| `fami_educacionmadre`  | Categórico     | Ordinal          | Nivel educativo alcanzado por la madre del estudiante.                | Representa el nivel de formación académica de la madre.                                   |
| `fami_educacionpadre`  | Categórico     | Ordinal          | Nivel educativo alcanzado por el padre del estudiante.                | Representa el nivel de formación académica del padre.                                     |
| `fami_tieneinternet`   | Categórico     | Binaria          | Indica si el hogar del estudiante tiene acceso a Internet.            | Mide la disponibilidad de conexión a Internet en la vivienda.                             |
| `fami_tienecomputador` | Categórico     | Binaria          | Indica si el estudiante dispone de computador en su hogar.            | Mide la disponibilidad de computador en la vivienda.                                      |
| `cole_naturaleza`      | Categórico     | Nominal          | Tipo de establecimiento educativo según su naturaleza administrativa. | Permite diferenciar si el colegio pertenece al sector oficial o no oficial (privado).     |
| `cole_area_ubicacion`  | Categórico     | Nominal          | Área geográfica donde está ubicada la sede educativa.                 | Identifica si el colegio está localizado en una zona urbana o rural.                      |
| `cole_jornada`         | Categórico     | Nominal          | Jornada en la que funciona el establecimiento o sede educativa.       | Identifica el horario o modalidad de jornada en que estudian los estudiantes.             |
| `estu_genero`          | Categórico     | Nominal          | Género reportado del estudiante que presentó la prueba.               | Permite caracterizar a los estudiantes según género.                                      |
| `estu_depto_reside`    | Categórico     | Nominal          | Departamento de residencia del estudiante.                            | Identifica el departamento de Colombia donde declara residir el estudiante.               |

