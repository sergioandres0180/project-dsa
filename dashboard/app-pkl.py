from __future__ import annotations

import pickle
import numpy as np
import pandas as pd
import streamlit as st
import json


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


# Cargar modelo y columnas
with open("../models/model.pkl", "rb") as f:
    modelo = pickle.load(f)

with open("../models/columnas_modelo.pkl", "rb") as f:
    columnas_modelo = pickle.load(f)


def preparar_features(payload: dict) -> pd.DataFrame:
    X_nuevo = pd.DataFrame([{
        "Habitaciones": payload["cuartos"],
        "Baños": payload["banos"],
        "log_marea": np.log10(payload["area_m2"]),
    }])

    # Inicializar todas las dummies en 0
    for col in columnas_modelo:
        if col not in X_nuevo.columns:
            X_nuevo[col] = 0

    # Activar solo las columnas correspondientes a la entrada
    tipo_col = f"Tipo_{payload['tipo_inmueble']}"
    barrio_col = f"Barrio_{payload['localidad']}"
    if tipo_col in X_nuevo.columns:
        X_nuevo[tipo_col] = 1
    if barrio_col in X_nuevo.columns:
        X_nuevo[barrio_col] = 1

    # Reordenar columnas como en entrenamiento
    X_nuevo = X_nuevo[columnas_modelo]

    return X_nuevo


# Función para predecir
def predecir_valor(payload: dict) -> float:
    X_nuevo = preparar_features(payload)
    log_valor_pred = modelo.predict(X_nuevo)[0]
    valor_pred = 10 ** log_valor_pred
    return valor_pred

def format_cop(value: float) -> str:
    return f"${value:,.0f}".replace(",", ".")


st.title("AvaluaTuHome")
st.caption("Calculadora interactiva para estimar el valor de tu inmueble en Bogotá.")
st.divider()

with st.form("avaluo_form"):
    st.subheader("1. Cuéntanos de tu inmueble")
    col1, col2, col3 = st.columns(3, gap="large")
    localidad = col1.selectbox("Localidad / barrio", BARRIOS)
    tipo = col2.selectbox("Tipo de inmueble", TIPOS_INMUEBLE)
    area = col3.number_input("Área cubierta (m²)", min_value=20, max_value=500, value=65, step=5)
    cuartos = col1.slider("Número de cuartos", 1, 6, 3)
    banos = col2.slider("Número de baños", 1, 4, 2)
    submitted = st.form_submit_button("Calcular avalúo estimado", use_container_width=True)

if submitted:
    payload = {
        "localidad": localidad,
        "tipo_inmueble": tipo,
        "area_m2": area,
        "cuartos": cuartos,
        "banos": banos,
    }
    valor_estimado = predecir_valor(payload)
    intervalo = (valor_estimado * 0.95, valor_estimado * 1.05)  # ±5% ejemplo
    st.session_state["payload"] = payload
    st.session_state["valor_estimado"] = valor_estimado
    st.session_state["intervalo"] = intervalo

if "valor_estimado" in st.session_state:
    payload = st.session_state["payload"]
    valor_estimado = st.session_state["valor_estimado"]
    intervalo = st.session_state["intervalo"]

    col_info, col_viz = st.columns([1.2, 1.8], gap="large")
    with col_info:
        st.subheader("2. Tu avalúo estimado")
        st.metric("Precio estimado (COP)", format_cop(valor_estimado))
        st.caption(f"Intervalo ±5%: {format_cop(intervalo[0])} – {format_cop(intervalo[1])}")

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

    with col_viz:
        st.subheader("3. Contexto del mercado en Bogotá")
        # Mock de dispersión (puedes dejar tu función mock_market_data)
        rng = np.random.default_rng(hash(payload["localidad"] + payload["tipo_inmueble"]) % 1_000_000)
        area_mock = rng.uniform(35, 180, size=60)
        precio_mock = 2.5 + 0.015 * area_mock + rng.normal(0, 0.2, size=area_mock.size)
        df_mock = pd.DataFrame({"Área (m²)": area_mock, "Precio (M COP)": precio_mock})
        st.scatter_chart(df_mock, x="Área (m²)", y="Precio (M COP)")

        st.write("Detalle del payload enviado (para depuración):")
        st.code(json.dumps(payload, indent=2, ensure_ascii=False))

st.divider()
st.caption("Versión con modelo RandomForest y columnas reales cargadas desde .pkl")
