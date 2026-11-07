"""
Tutorial 07: Rendimiento y Almacenamiento en Caché en Streamlit
==============================================================
Aprende a acelerar tus aplicaciones drásticamente utilizando los decoradores
@st.cache_data (para datasets, cálculos y APIs) y @st.cache_resource (para conexiones
a bases de datos, microcontroladores y modelos de Machine Learning).
"""

import time
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Tutorial 07 - Rendimiento y Caché",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Tutorial 07: Optimización con @st.cache_data y @st.cache_resource")
st.write(
    "Dado que Streamlit re-ejecuta el script en cada interacción, una función pesada "
    "(como entrenar un modelo, consultar una base de datos remota o procesar 100,000 filas) "
    "haría la aplicación insoportablemente lenta sin una estrategia de almacenamiento en caché."
)

st.divider()

# ===============================================================
# 1. @st.cache_data: DATOS, CÁLCULOS Y TRANSFORMACIONES
# ===============================================================
st.header("1. Almacenamiento en Caché de Datos: `@st.cache_data`")
st.markdown("""
- **¿Qué almacena?** Resultados que pueden serializarse (DataFrames, listas, diccionarios, cadenas, arrays).
- **¿Cómo funciona?** Crea una copia del resultado calculada a partir de los argumentos de entrada.
- Si los argumentos no cambian, devuelve el resultado guardado **al instante** sin ejecutar la función.
""")

def calcular_sin_cache(filas: int) -> pd.DataFrame:
    """Simula una consulta lenta a una base de datos o API remota."""
    time.sleep(2.0)  # Demora deliberada de 2 segundos
    datos = {
        "Sensor": [f"S_{i}" for i in range(filas)],
        "Valor": np.random.normal(50, 10, filas),
        "Fecha": pd.date_range("2026-01-01", periods=filas, freq="h")
    }
    return pd.DataFrame(datos)

@st.cache_data(show_spinner=False, ttl=60)
def calcular_con_cache(filas: int) -> pd.DataFrame:
    """Misma función pero decorada con @st.cache_data y caducidad de 60 segundos."""
    time.sleep(2.0)
    datos = {
        "Sensor": [f"S_{i}" for i in range(filas)],
        "Valor": np.random.normal(50, 10, filas),
        "Fecha": pd.date_range("2026-01-01", periods=filas, freq="h")
    }
    return pd.DataFrame(datos)

col_c1, col_c2 = st.columns(2)

with col_c1:
    st.subheader("❌ Sin Almacenamiento en Caché")
    num_filas = st.slider("Cantidad de registros:", 100, 1000, 500, key="slider_filas")
    
    if st.button("Ejecutar SIN Caché (Siempre 2s)", type="secondary"):
        inicio = time.time()
        with st.spinner("Consultando base de datos lenta..."):
            df_lento = calcular_sin_cache(num_filas)
        fin = time.time()
        duracion = fin - inicio
        st.error(f"⏱️ Tiempo transcurrido: **{duracion:.2f} segundos**")
        st.dataframe(df_lento.head(3), use_container_width=True)

with col_c2:
    st.subheader("✅ Con `@st.cache_data`")
    if st.button("Ejecutar CON Caché (Instantáneo tras la 1ª vez)", type="primary"):
        inicio = time.time()
        with st.spinner("Obteniendo datos..."):
            df_rapido = calcular_con_cache(num_filas)
        fin = time.time()
        duracion = fin - inicio
        if duracion > 1.0:
            st.warning(f"🐢 Primera llamada (cálculo real): **{duracion:.2f} segundos**")
        else:
            st.success(f"🚀 Llamada desde Caché: **{duracion * 1000:.2f} milisegundos!**")
        st.dataframe(df_rapido.head(3), use_container_width=True)

col_clear1, col_clear2 = st.columns(2)
with col_clear2:
    if st.button("🧹 Limpiar Caché de Datos"):
        calcular_con_cache.clear()
        st.info("Caché invalidado. La siguiente llamada volverá a tardar 2 segundos.")

st.divider()

# ===============================================================
# 2. @st.cache_resource: CONEXIONES Y OBJETOS GLOBALES
# ===============================================================
st.header("2. Almacenamiento de Recursos Globales: `@st.cache_resource`")
st.markdown("""
- **¿Qué almacena?** Objetos que **NO** deben clonarse ni serializarse:
  - Clientes de base de datos (`SQLAlchemy`, `pymongo`).
  - Conexiones por hardware (`serial.Serial` con Arduino).
  - Modelos pesados en memoria (`PyTorch`, `TensorFlow`, `scikit-learn`).
- **Comportamiento:** Devuelve exactamente la misma instancia del objeto en memoria para todas las sesiones.
""")

class GestorHardwareSimulado:
    """Clase que simula un hardware o conexión persistente."""
    def __init__(self, puerto: str):
        self.puerto = puerto
        self.tiempo_conexion = time.time()
        self.mensajes_enviados = 0
        # Simular retardo de conexión física
        time.sleep(1.0)
    
    def enviar_comando(self, comando: str) -> str:
        self.mensajes_enviados += 1
        return f"ACK: '{comando}' ejecutado en {self.puerto} (Msg #{self.mensajes_enviados})"

@st.cache_resource
def obtener_conexion_hardware(puerto_com: str) -> GestorHardwareSimulado:
    """
    Gracias a @st.cache_resource, esta conexión SOLO se abre una vez.
    En las siguientes recargas de la página, se reutiliza el mismo objeto sin reconectar el puerto.
    """
    return GestorHardwareSimulado(puerto_com)

col_r1, col_r2 = st.columns(2)
with col_r1:
    puerto_elegido = st.selectbox("Selecciona puerto:", ["COM1", "COM3", "COM4", "/dev/ttyUSB0"])
    conexion = obtener_conexion_hardware(puerto_elegido)
    st.success(f"Dispositivo conectado en `{conexion.puerto}` (Uptime: {int(time.time() - conexion.tiempo_conexion)}s)")

with col_r2:
    cmd = st.text_input("Comando a enviar:", value="PING")
    if st.button("Enviar Comando"):
        respuesta = conexion.enviar_comando(cmd)
        st.write(f"Respuesta del hardware: `{respuesta}`")
        st.caption(f"Total comandos enviados a este canal persistente: {conexion.mensajes_enviados}")

st.divider()
st.info("💡 Ejecuta este tutorial con: `uv run streamlit run 07_rendimiento_y_cache/app.py`")
