# Verificación de reproducibilidad

## Entorno utilizado

* Sistema operativo: Windows
* Python: 3.14.7
* Terminal: PowerShell
* Editor: Visual Studio Code

## Pasos realizados

Se clonó el repositorio mediante:

```bash
git clone https://github.com/mgabrielaespinosa-star/caso_saber_11.git
cd caso_saber_11
```

Se creó el entorno virtual:

```bash
python -m venv .venv
```

Al intentar activarlo inicialmente con:

```powershell
.venv\Scripts\Activate.ps1
```

PowerShell bloqueó la ejecución debido a la política de ejecución de scripts de Windows.

El problema se resolvió temporalmente para la sesión actual utilizando:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Posteriormente, el entorno virtual se activó correctamente.

Se instalaron las dependencias:

```bash
pip install -r requirements.txt
```

La instalación finalizó sin errores.

## Verificación de la API

Se inició la API con Uvicorn y se comprobó que la documentación estuviera disponible en:

```text
http://localhost:8000/docs

(evidencias_reproducibilidad/jairo-uvicorn.png)

```

El endpoint `/health` respondió correctamente:

```text
StatusCode : 200
Content : {"status":"ok","model_loaded":true}
```

También se probó el endpoint `POST /predict` desde Swagger UI, obteniendo una respuesta:

```text
200 OK
```

## Pruebas automatizadas

Se ejecutaron las pruebas mediante:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Resultado final:

```text
7 passed
```

## Conclusión

El proyecto pudo reproducirse correctamente en un segundo computador con Windows. 
La única dificultad encontrada fue la política de ejecución de scripts de PowerShell al activar el entorno virtual, 
la cual se resolvió habilitando temporalmente la ejecución de scripts para la sesión actual.
