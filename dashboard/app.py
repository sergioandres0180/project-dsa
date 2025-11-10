"""
AvaluaTuHome – Streamlit dashboard
----------------------------------
Tablero interactivo para estimar el valor de un inmueble en Bogotá.
Mientras el modelo/API real se integra, la aplicación usa datos y lógica mock
para evidenciar el flujo completo y permitir pruebas locales.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
import pandas as pd
import streamlit as st


# -----------------------------
# Configuración e utilidades
# -----------------------------

st.set_page_config(
    page_title="AvaluaTuHome",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BARRIOS = [
    "Usaquén",
    "Chapinero",
    "Suba",
    "Kennedy",
    "Barrios Unidos",
    "Bosa",
    "Engativá",
    "Teusaquillo",
    "Fontibón",
]

TIPOS_INMUEBLE = ["Apartamento", "Casa", "Studio", "Oficina"]


@dataclass
class PredictionResult:
    valor: float
    intervalo: Tuple[float, float]
    feature_importance: Dict[str, float]


def simulate_prediction(payload: Dict[str, float]) -> PredictionResult:
    """Genera una predicción mock basándose en reglas simples."""
    base_price = 2_500_000 * payload["area_m2"]
    tipo_factor = {
        "Apartamento": 1.0,
        "Casa": 1.15,
        "Studio": 0.85,
        "Oficina": 1.1,
    }.get(payload["tipo_inmueble"], 1.0)
    barrio_factor = 1 + (BARRIOS.index(payload["localidad"]) / len(BARRIOS)) * 0.15
    habitaciones_factor = 1 + (payload["cuartos"] - 2) * 0.05
    banos_factor = 1 + (payload["banos"] - 1) * 0.04

    valor = base_price * tipo_factor * barrio_factor * habitaciones_factor * banos_factor
    ruido = np.random.normal(0, 5_000_000)
    valor += ruido
    intervalo = (valor - 25_000_000, valor + 25_000_000)

    importancias = {
        "Localidad / barrio": 0.40,
        "Área (m²)": 0.30,
        "Tipo de inmueble": 0.15,
        "Cuartos": 0.10,
        "Baños": 0.05,
    }
    return PredictionResult(valor=valor, intervalo=intervalo, feature_importance=importancias)


def call_prediction_api(payload: Dict[str, float]) -> PredictionResult:
    """
    Si existe la variable de entorno MODEL_ENDPOINT, intenta llamar a la API real.
    En caso contrario, usa la simulación local.
    """
    endpoint = os.getenv("MODEL_ENDPOINT")
    if not endpoint:
        return simulate_prediction(payload)

    import requests  # import local para evitar dependencia si no se usa

    response = requests.post(endpoint, json=payload, timeout=10)
    response.raise_for_status()
    data = response.json()
    return PredictionResult(
        valor=data["avaluo_cop"],
        intervalo=tuple(data.get("intervalo_confianza", [data["avaluo_cop"], data["avaluo_cop"]])),
        feature_importance=data.get("feature_importance", {}),
    )


@st.cache_data
def mock_market_data(localidad: str, tipo: str) -> pd.DataFrame:
    """Genera datos de dispersión área vs precio para la visualización de contexto."""
    rng = np.random.default_rng(hash(localidad + tipo) % 1_000_000)
    area = rng.uniform(35, 180, size=60)
    base = 2.4 + (BARRIOS.index(localidad) / len(BARRIOS)) * 0.8
    precio_millones = base + 0.015 * area + rng.normal(0, 0.2, size=area.size)
    return pd.DataFrame({"Área (m²)": area, "Precio (M COP)": precio_millones})


def format_cop(value: float) -> str:
    return f"${value:,.0f}".replace(",", ".")


# -----------------------------
# Layout
# -----------------------------

st.title("AvaluaTuHome")
st.caption("Calculadora interactiva para estimar el valor de tu inmueble en Bogotá.")
st.divider()


with st.form("avaluo_form"):
    st.subheader("1. Cuéntanos de tu inmueble")
    st.write("Completa los campos para personalizar la consulta. Estos datos se enviarán al modelo.")
    col1, col2, col3 = st.columns(3, gap="large")
    localidad = col1.selectbox("Localidad / barrio", BARRIOS, help="Usamos la localidad para contextualizar comparables.")
    tipo = col2.selectbox("Tipo de inmueble", TIPOS_INMUEBLE)
    area = col3.number_input("Área cubierta (m²)", min_value=20, max_value=500, value=65, step=5)
    cuartos = col1.slider("Número de cuartos", 1, 6, 3)
    banos = col2.slider("Número de baños", 1, 4, 2)
    submitted = st.form_submit_button("Calcular avalúo estimado", use_container_width=True)

if submitted:
    with st.spinner("Consultando modelo..."):
        payload = {
            "localidad": localidad,
            "tipo_inmueble": tipo,
            "area_m2": area,
            "cuartos": cuartos,
            "banos": banos,
        }
        result = call_prediction_api(payload)
        st.session_state["payload"] = payload
        st.session_state["result"] = result


if "result" in st.session_state:
    payload = st.session_state["payload"]
    result = st.session_state["result"]
    col_info, col_viz = st.columns([1.2, 1.8], gap="large")

    with col_info:
        st.subheader("2. Tu avalúo estimado")
        st.metric("Precio estimado (COP)", format_cop(result.valor))
        st.caption(
            f"Intervalo ±MAE: {format_cop(result.intervalo[0])} – {format_cop(result.intervalo[1])}"
        )
        st.write("**Características evaluadas**")
        st.write(
            f"""
- Localidad/barrio: **{payload['localidad']}**
- Tipo: **{payload['tipo_inmueble']}**
- Área cubierta: **{payload['area_m2']} m²**
- Cuartos: **{payload['cuartos']}**
- Baños: **{payload['banos']}**
"""
        )
        st.info(
            "Cuando la API esté disponible, este valor se actualizará automáticamente manteniendo el mismo flujo."
        )

        st.subheader("Impacto de las variables")
        if result.feature_importance:
            fi_df = (
                pd.Series(result.feature_importance)
                .sort_values(ascending=True)
                .to_frame("Importancia")
            )
            st.bar_chart(fi_df)
        else:
            st.write("Pendiente de conectar las importancias del modelo (SHAP o feature importance).")

    with col_viz:
        st.subheader("3. Contexto del mercado en Bogotá")
        data_scatter = mock_market_data(payload["localidad"], payload["tipo_inmueble"])
        st.write("Relación área vs. precio para comparables recientes en la misma localidad.")
        st.scatter_chart(data_scatter, x="Área (m²)", y="Precio (M COP)")

        st.write("Detalle del payload enviado (para depuración):")
        st.code(json.dumps(payload, indent=2, ensure_ascii=False))

else:
    st.info("Ingresa los datos del inmueble y presiona “Calcular avalúo estimado” para ver los resultados.")


st.divider()
st.caption(
    "Versión mock (Semana 5). Integraremos la API de inferencia y métricas de MLflow en las próximas iteraciones."
)
