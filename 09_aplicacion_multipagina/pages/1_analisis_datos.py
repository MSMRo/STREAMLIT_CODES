"""
Subpágina 1: Análisis de Datos y Exploración Interactiva
========================================================
Demuestra cómo los datos de st.session_state se conservan al cambiar de página.
"""

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="App Multipágina - Análisis de Datos",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Análisis de Datos y Tendencias")
st.write(f"Sesión activa para: **{st.session_state.get('usuario_conectado', 'Invitado')}**")

st.divider()

# Generar datos de ejemplo
np.random.seed(101)
muestras = 50
df_analisis = pd.DataFrame({
    "Hora": pd.date_range("2026-11-06 00:00", periods=muestras, freq="30min"),
    "Consumo_kW": np.random.normal(12.5, 2.0, muestras) + np.sin(np.linspace(0, 4 * np.pi, muestras)) * 3,
    "Eficiencia": np.clip(np.random.normal(92.0, 3.0, muestras), 80, 100)
}).set_index("Hora")

col_filtro, col_grafico = st.columns([1, 3])

with col_filtro:
    st.subheader("Filtros de Análisis")
    umbral_eficiencia = st.slider("Filtrar Eficiencia Mínima (%):", 80, 95, 88)
    variable_mostrar = st.radio("Señal a graficar:", ["Consumo_kW", "Eficiencia"])
    
    df_filtrado = df_analisis[df_analisis["Eficiencia"] >= umbral_eficiencia]
    st.metric("Puntos Cumplen Umbral", f"{len(df_filtrado)} de {len(df_analisis)}")

with col_grafico:
    st.subheader(f"Evolución de {variable_mostrar}")
    st.line_chart(df_filtrado[[variable_mostrar]])

st.dataframe(df_filtrado.tail(6), use_container_width=True)
