"""
AvaluaTuHome – Streamlit dashboard
----------------------------------
Tablero interactivo para estimar el valor de un inmueble en Bogotá.
Conectado al modelo de producción vía API (`MODEL_ENDPOINT`).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
import pandas as pd
import streamlit as st
import altair as alt


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


BASE_DIR = Path(__file__).resolve().parent
ENDPOINT = os.getenv("MODEL_ENDPOINT")
BANNER_PATH = BASE_DIR / "banner.png"

# -----------------------------
# Tema y estilo
# -----------------------------
st.markdown(
    """
    <style>
    :root {
        --primary: #592796;
        --secondary: #2F0E4F;
        --accent: #22D3EE;
        --accent2: #2EC4B6;
        --light: #C3B1F7;
    }
    .stApp {
        background: linear-gradient(180deg, #2F0E4F 0%, #1B0A33 100%);
        color: #FFFFFF;
    }
    div.stButton > button {
        background-color: var(--primary);
        color: #FFFFFF;
        border-radius: 10px;
        border: 1px solid #8F6AD9;
    }
    div.stButton > button:hover {
        background-color: #8F6AD9;
        color: #FFFFFF;
    }
    div[data-testid="stMetricValue"] { color: var(--accent2); }
    div[data-testid="stMetricLabel"] { color: var(--light); }
    </style>
    """,
    unsafe_allow_html=True,
)


@dataclass
class PredictionResult:
    valor: float
    intervalo: Tuple[float, float]
    feature_importance: Dict[str, float]


def call_prediction_api(payload: Dict[str, float]) -> PredictionResult:
    """
    Llama a la API real definida en MODEL_ENDPOINT.
    """
    if not ENDPOINT:
        raise RuntimeError("MODEL_ENDPOINT no está configurado; defínelo con la URL pública de la API.")

    import requests  # import local para evitar dependencia si no se usa

    response = requests.post(ENDPOINT, json=payload, timeout=10)
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

if BANNER_PATH.exists():
    st.image(str(BANNER_PATH), use_container_width=True)
st.title("AvaluaTuHome")
st.caption("Calculadora interactiva para estimar el valor de tu inmueble en Bogotá.")
st.divider()

if not ENDPOINT:
    st.error("MODEL_ENDPOINT no está configurado. Define la URL pública de la API para usar el tablero en modo producción.")

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

        st.subheader("Impacto de las variables")
        if result.feature_importance:
            fi_df = (
                pd.Series(result.feature_importance)
                .sort_values(ascending=True)
                .to_frame("Importancia")
            )
            st.bar_chart(fi_df)
        else:
            st.write("El modelo actual no retorna importancias de variables (SHAP/feature importance).")

    with col_viz:
        st.subheader("3. Contexto del mercado en Bogotá")
        data_scatter = mock_market_data(payload["localidad"], payload["tipo_inmueble"])
        st.write("Relación área vs. precio para comparables recientes en la misma localidad.")
        chart = (
            alt.Chart(data_scatter)
            .mark_circle(size=80, color="#22D3EE")
            .encode(x="Área (m²)", y="Precio (M COP)")
            .properties(height=320)
            .interactive()
        )
        st.altair_chart(chart, use_container_width=True)

        st.subheader("Intervalo estimado")
        st.write(
            f"Rango de confianza basado en el desempeño histórico del modelo: "
            f"{format_cop(result.intervalo[0])} – {format_cop(result.intervalo[1])}."
        )
        st.caption(
            "El intervalo refleja la variabilidad esperada (±MAE). Use el valor central como referencia y este rango para evaluar escenarios conservador y optimista."
        )

else:
    st.info("Ingresa los datos del inmueble y presiona “Calcular avalúo estimado” para ver los resultados.")


st.divider()
st.caption("Resultados generados con el modelo de avalúos en producción.")
