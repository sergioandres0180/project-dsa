"""
AvaluoTuHome API
----------------
API de inferencia para estimar el valor de un inmueble en Bogotá.
Carga el modelo entrenado (Random Forest) y las columnas usadas en el entrenamiento,
preprocesa la solicitud y devuelve el avalúo en COP con un intervalo aproximado.
"""

from __future__ import annotations

from pathlib import Path
from typing import List
import json
import pickle

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "model.pkl"
COLUMNS_PATH = BASE_DIR / "models" / "columnas_modelo.pkl"

app = FastAPI(title="AvaluaTuHome API", version="1.0.0")


class AvaluoRequest(BaseModel):
    localidad: str = Field(..., description="Localidad o barrio en Bogotá")
    tipo_inmueble: str = Field(..., description="Tipo de inmueble (Apartamento, Casa, etc.)")
    area_m2: float = Field(..., gt=0, description="Área cubierta en metros cuadrados")
    cuartos: int = Field(..., ge=0, description="Número de habitaciones")
    banos: int = Field(..., ge=0, description="Número de baños")


def load_artifacts():
    if not MODEL_PATH.exists() or not COLUMNS_PATH.exists():
        raise FileNotFoundError("No se encontraron los artefactos del modelo en la carpeta models/")
    with MODEL_PATH.open("rb") as f:
        model = pickle.load(f)
    with COLUMNS_PATH.open("rb") as f:
        columnas_modelo: List[str] = pickle.load(f)
    return model, columnas_modelo


model, columnas_modelo = load_artifacts()

# Factor para intervalo aproximado (ajustar con MAE real si está disponible)
INTERVAL_FACTOR = 0.05


def preparar_features(payload: AvaluoRequest) -> pd.DataFrame:
    """Genera el vector de características alineado al entrenamiento."""
    df = pd.DataFrame(
        [
            {
                "Habitaciones": payload.cuartos,
                "Baños": payload.banos,
                "log_marea": np.log10(payload.area_m2),
            }
        ]
    )

    for col in columnas_modelo:
        if col not in df.columns:
            df[col] = 0

    tipo_col = f"Tipo_{payload.tipo_inmueble}"
    barrio_col = f"Barrio_{payload.localidad}"
    if tipo_col in df.columns:
        df[tipo_col] = 1
    if barrio_col in df.columns:
        df[barrio_col] = 1

    try:
        df = df[columnas_modelo]
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=f"Columnas faltantes: {exc}")
    return df


@app.get("/health")
def health():
    return {"status": "ok", "model_path": str(MODEL_PATH), "columns": len(columnas_modelo)}


@app.post("/api/v1/avaluo")
def avaluo(payload: AvaluoRequest):
    X = preparar_features(payload)
    log_pred = model.predict(X)[0]
    valor = float(10 ** log_pred)
    intervalo = [valor * (1 - INTERVAL_FACTOR), valor * (1 + INTERVAL_FACTOR)]
    return {
        "avaluo_cop": valor,
        "intervalo_confianza": intervalo,
        "inputs": json.loads(payload.json()),
    }
