"""Esquemas Pydantic: el contrato de entrada y salida de la API.

Una observación = el contexto socioeconómico de un estudiante (las mismas 10
variables con las que se entrenó el pipeline; el orden lo maneja el pipeline).
Los campos de baja cardinalidad se restringen a sus valores admitidos con
Literal: un valor fuera de catálogo produce 422 automático. Los campos de alta
cardinalidad (educación de los padres, departamento, jornada) quedan como str:
una categoría nueva no rompe el modelo (OneHotEncoder usa handle_unknown="ignore").
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Estudiante(BaseModel):
    """Contexto socioeconómico de un estudiante (entrada de /predict)."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
        }
    )

    fami_estratovivienda: Literal[
        "Estrato 1", "Estrato 2", "Estrato 3", "Estrato 4",
        "Estrato 5", "Estrato 6", "Sin Estrato", "Sin dato",
    ] = Field(..., description="Estrato socioeconómico de la vivienda")
    fami_educacionmadre: str = Field(..., min_length=1, description="Nivel educativo de la madre")
    fami_educacionpadre: str = Field(..., min_length=1, description="Nivel educativo del padre")
    fami_tieneinternet: Literal["Si", "No", "Sin dato"] = Field(..., description="Internet en el hogar")
    fami_tienecomputador: Literal["Si", "No", "Sin dato"] = Field(..., description="Computador en el hogar")
    cole_naturaleza: Literal["OFICIAL", "NO OFICIAL", "Sin dato"] = Field(..., description="Colegio público u oficial vs. privado")
    cole_area_ubicacion: Literal["URBANO", "RURAL", "Sin dato"] = Field(..., description="Área del colegio")
    cole_jornada: str = Field(..., min_length=1, description="Jornada escolar (COMPLETA, MAÑANA, TARDE, ...)")
    estu_genero: Literal["F", "M", "Sin dato"] = Field(..., description="Género del estudiante")
    estu_depto_reside: str = Field(..., min_length=1, description="Departamento de residencia")


class Prediccion(BaseModel):
    """Salida de /predict."""

    rendimiento_alto: int = Field(description="1 = sobre la mediana nacional de matemáticas, 0 = bajo")
    probabilidad: float = Field(description="P(rendimiento_alto = 1)")
    modelo: str
    version_sklearn: str
    timestamp_utc: str


class LoteEstudiantes(BaseModel):
    """Entrada de /predict-batch."""

    estudiantes: list[Estudiante] = Field(..., min_length=1, max_length=1000)


class PrediccionLote(BaseModel):
    """Salida de /predict-batch (mismo orden que la entrada)."""

    predicciones: list[Prediccion]
    n: int
