# AvaluaTuHome — Proyecto DSA

Repositorio del proyecto de valoración de inmuebles en Bogotá para la materia **Despliegue de Soluciones Analíticas**. El objetivo es entregar un prototipo funcional que cubra todo el ciclo: preparación de datos, entrenamiento y versionamiento de modelos, API de inferencia y tablero interactivo.

## Estructura general

- `Notebooks/`: exploración, limpieza y experimentos iniciales.
- `data/`: datasets en bruto y procesados (cuando aplica, versionados con DVC).
- `models/`: scripts de entrenamiento (`models-mlflow.py`) y artefactos exportados desde MLflow.
- `dashboard/`: mockup + apps Streamlit (`app.py` y `app-pkl.py`) para consumir el modelo (vía API o `.pkl`).
- `api/`: servicio FastAPI (`api/main.py`) para exponer el modelo como API REST.
- `Entregas/`: reportes y evidencias por semana.

## Componentes principales

1. **Modelado supervisado**  
   - Dataset: `Notebooks/inmuebles_bogota 2.csv` (~9.5k registros).  
   - Features: tipo, habitaciones, baños, log(área) y barrio.  
   - Modelos probados: Regresión Lineal, Ridge, Random Forest, LightGBM.  
   - Tracking: experimento `modelos_inmuebles_bogota` en MLflow (runs incluyen parámetros, métricas y artefactos).

2. **Tablero AvaluaTuHome**  
   - Despliegue local con `streamlit run dashboard/app.py`.  
   - Inputs: localidad/barrio, tipo, área, cuartos y baños.  
   - Outputs: avalúo estimado, intervalo ±MAE, comparables y variables más influyentes.  
   - Integración preparada para consumir la API `POST /api/v1/avaluo` vía `MODEL_ENDPOINT`.

3. **Documentación de entregas**  
   - `Entregas/Entrega_2/Reporte_Entrega2_Sem5.md` resume contexto, modelos, tablero y trabajo en equipo.  
   - Carpeta `Imagenes/` con evidencia visual (tablero, MLflow, VM).

## API de avalúos

Ejecutar localmente (modo desarrollo):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r api/requirements.txt
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Endpoints:
- `GET /health` → estado y metadatos del modelo cargado.
- `POST /api/v1/avaluo` → recibe `localidad`, `tipo_inmueble`, `area_m2`, `cuartos`, `banos` y devuelve `avaluo_cop` e `intervalo_confianza`.

## Cómo correr el tablero

```bash
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
pip install -r dashboard/requirements.txt
cd dashboard
streamlit run app.py
```

Para consumir el modelo real:

```bash
export MODEL_ENDPOINT="https://<host>/api/v1/avaluo"
streamlit run app.py
```

## Próximos hitos

1. Publicar la API de inferencia y conectar el tablero al endpoint real.
2. Incorporar explicaciones del modelo (SHAP/feature importance) desde los artefactos de MLflow.
3. Empaquetar la solución (API + tablero) en contenedores y documentar instalación/despliegue final.
