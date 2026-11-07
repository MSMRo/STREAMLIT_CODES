"""
Tutorial 06: Visualización de Datos y Tablas Interactivas
========================================================
Aprende a presentar datos tabulares interactivos con st.dataframe y st.data_editor,
utilizar gráficos nativos de Streamlit y construir visualizaciones científicas
y dashboards analíticos con Plotly.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Tutorial 06 - Visualización y Datos",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Tutorial 06: Visualización de Datos y Gráficos Interactivos")
st.write(
    "Streamlit ofrece soporte de primera clase para la exploración de datos. "
    "Puedes desde mostrar tablas estáticas hasta editar DataFrames en vivo en el navegador "
    "e incrustar gráficos vectoriales e interactivos con Plotly."
)

st.divider()

# ==========================================
# 1. TABLAS INTERACTIVAS Y EDITABLES
# ==========================================
st.header("1. Tablas Interactivas y Editables")

# Generar dataset de sensores de laboratorio
np.random.seed(42)
sensores_data = {
    "ID": [f"SN-{100 + i}" for i in range(8)],
    "Ubicación": ["Tanque A", "Tanque B", "Reactor 1", "Reactor 2", "Tubería N", "Tubería S", "Caldera", "Enfriador"],
    "Temperatura (°C)": [24.5, 31.2, 78.4, 82.1, 19.3, 21.0, 115.6, 8.2],
    "Nivel de Carga (%)": [0.65, 0.40, 0.88, 0.92, 0.30, 0.45, 0.99, 0.20],
    "Activo": [True, True, True, True, False, True, True, False],
    "Última Calibración": pd.date_range("2026-10-01", periods=8, freq="4D").strftime("%Y-%m-%d")
}
df_sensores = pd.DataFrame(sensores_data)

col_t1, col_t2 = st.columns(2)

with col_t1:
    st.subheader("DataFrame con Configuración de Columnas (`st.dataframe`)")
    st.write("Soporta búsqueda, ordenación por columnas y formato visual como barras de progreso:")
    st.dataframe(
        df_sensores,
        column_config={
            "Nivel de Carga (%)": st.column_config.ProgressColumn(
                "Carga Actual",
                format="%.0f%%",
                min_value=0,
                max_value=1
            ),
            "Temperatura (°C)": st.column_config.NumberColumn(
                "Temp (°C)",
                format="%.1f °C"
            ),
            "Activo": st.column_config.CheckboxColumn(
                "En Línea",
                help="Indica si el sensor está transmitiendo"
            )
        },
        hide_index=True,
        use_container_width=True
    )

with col_t2:
    st.subheader("Editor de Datos en Vivo (`st.data_editor`)")
    st.write("¡Puedes hacer doble clic en cualquier celda para editarla o añadir nuevas filas!")
    
    # Tabla editable de umbrales de alarma
    df_umbrales = pd.DataFrame({
        "Parámetro": ["Temperatura Máx (°C)", "Presión Máx (PSI)", "Flujo Mín (L/min)"],
        "Umbral": [85.0, 150.0, 12.0],
        "Alerta Sonora": [True, True, False]
    })
    
    df_editado = st.data_editor(
        df_umbrales,
        num_rows="dynamic",
        use_container_width=True,
        key="editor_umbrales"
    )
    st.caption("Valores actualmente en memoria tras edición:")
    st.json(df_editado.to_dict(orient="records"))

st.divider()

# ==========================================
# 2. GRÁFICOS NATIVOS DE STREAMLIT
# ==========================================
st.header("2. Gráficos Nativos Rápidos")
st.write(
    "Para visualizaciones instantáneas sin configurar bibliotecas externas, "
    "Streamlit provee gráficos rápidos optimizados para DataFrames."
)

# Datos de series de tiempo
fechas = pd.date_range("2026-11-01", periods=30, freq="D")
df_series = pd.DataFrame({
    "Fecha": fechas,
    "Sensor_A": np.sin(np.linspace(0, 10, 30)) * 10 + 50 + np.random.normal(0, 1, 30),
    "Sensor_B": np.cos(np.linspace(0, 10, 30)) * 8 + 45 + np.random.normal(0, 1.5, 30),
    "Sensor_C": np.linspace(30, 65, 30) + np.random.normal(0, 2, 30)
}).set_index("Fecha")

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("Gráfico de Líneas (`st.line_chart`)")
    st.line_chart(df_series)

with col_g2:
    st.subheader("Gráfico de Barras (`st.bar_chart`)")
    df_promedios = pd.DataFrame({
        "Sensor": ["Sensor A", "Sensor B", "Sensor C"],
        "Lectura Promedio": [df_series["Sensor_A"].mean(), df_series["Sensor_B"].mean(), df_series["Sensor_C"].mean()]
    }).set_index("Sensor")
    st.bar_chart(df_promedios)

st.divider()

# ==========================================
# 3. VISUALIZACIONES AVANZADAS CON PLOTLY
# ==========================================
st.header("3. Gráficos Interactivos con Plotly (`st.plotly_chart`)")
st.write(
    "Plotly permite hacer zoom, panning, tooltips personalizados y exportar imágenes "
    "directamente desde el navegador."
)

tab_scatter, tab_surface = st.tabs(["🎯 Dispersión y Correlaciones", "🏔️ Superficie 3D"])

with tab_scatter:
    # Generar datos de simulación de motores
    n_puntos = 150
    rpm = np.random.uniform(500, 3500, n_puntos)
    potencia = (rpm / 100) * 2.8 + np.random.normal(0, 8, n_puntos)
    temperatura = 30 + (potencia * 0.45) + np.random.normal(0, 3, n_puntos)
    estado = np.where(temperatura > 75, "Crítico", np.where(temperatura > 55, "Advertencia", "Normal"))
    
    df_motores = pd.DataFrame({
        "RPM": rpm,
        "Potencia_kW": potencia,
        "Temperatura_C": temperatura,
        "Estado": estado
    })
    
    fig_scatter = px.scatter(
        df_motores,
        x="RPM",
        y="Potencia_kW",
        color="Estado",
        size="Temperatura_C",
        hover_data=["Temperatura_C"],
        color_discrete_map={"Normal": "#2ECC71", "Advertencia": "#F39C12", "Crítico": "#E74C3C"},
        title="Rendimiento de Motor: Potencia vs RPM y Temperatura"
    )
    fig_scatter.update_layout(template="plotly_dark", height=450)
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab_surface:
    # Gráfico 3D de distribución de potencial térmico
    x_3d = np.linspace(-5, 5, 40)
    y_3d = np.linspace(-5, 5, 40)
    xx_3d, yy_3d = np.meshgrid(x_3d, y_3d)
    zz_3d = np.sin(np.sqrt(xx_3d**2 + yy_3d**2)) * 10
    
    fig_3d = go.Figure(data=[go.Surface(z=zz_3d, x=xx_3d, y=yy_3d, colorscale="Viridis")])
    fig_3d.update_layout(
        title="Mapa de Calor Térmico 3D",
        scene=dict(
            xaxis_title="Eje X (mm)",
            yaxis_title="Eje Y (mm)",
            zaxis_title="Temperatura (°C)"
        ),
        template="plotly_dark",
        height=500
    )
    st.plotly_chart(fig_3d, use_container_width=True)

st.divider()
st.info("💡 Ejecuta este tutorial con: `uv run streamlit run 06_visualizacion_y_datos/app.py`")
