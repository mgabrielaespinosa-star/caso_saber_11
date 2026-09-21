# Artefactos del modelo

- `model.pkl` — Pipeline completo de scikit-learn (OneHotEncoder + regresión logística) serializado con joblib. Se genera con `python train.py` desde la raíz del proyecto.
- `metadata.json` — versión de sklearn y Python, lista ordenada de features, métricas en test de ambos candidatos, definición del target y fecha de entrenamiento.
