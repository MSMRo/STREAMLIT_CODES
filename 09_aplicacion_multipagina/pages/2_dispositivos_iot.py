"""
Subpágina 2: Monitoreo de Dispositivos IoT
==========================================
Demuestra tablas de estado de hardware, filtrado por estado y telemetría.
"""

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="App Multipágina - Dispositivos IoT",
    page_icon="🔌",
    layout="wide"
)

st.title("🔌 Monitoreo de Nodos y Dispositivos IoT")
st.write("Estado de conexión en tiempo real de los módulos Arduino y sensores de campo.")

st.divider()

dispositivos = [
    {"ID": "ARD_01", "Tipo": "Arduino Uno", "Puerto": "COM3", "Baudios": 9600, "Estado": "En Línea", "Voltaje_V": 4.98},
    {"ID": "ARD_02", "Tipo": "Arduino Mega", "Puerto": "COM4", "Baudios": 115200, "Estado": "En Línea", "Voltaje_V": 5.02},
    {"ID": "ESP_01", "Tipo": "ESP32", "Puerto": "COM7", "Baudios": 115200, "Estado": "En Línea", "Voltaje_V": 3.31},
    {"ID": "ESP_02", "Tipo": "ESP32", "Puerto": "COM8", "Baudios": 115200, "Estado": "Desconectado", "Voltaje_V": 0.00},
    {"ID": "PICO_01", "Tipo": "RPi Pico", "Puerto": "COM9", "Baudios": 9600, "Estado": "En Línea", "Voltaje_V": 3.29},
]

df_iot = pd.DataFrame(dispositivos)

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Listado de Hardware Registrado")
    st.dataframe(
        df_iot,
        column_config={
            "Voltaje_V": st.column_config.NumberColumn("Tensión", format="%.2f V"),
            "Estado": st.column_config.TextColumn("Estado Red")
        },
        hide_index=True,
        use_container_width=True
    )

with col2:
    with st.container(border=True):
        st.subheader("Acción Rápida")
        if st.button("🔄 Escanear Nuevos Puertos COM", use_container_width=True):
            st.toast("Escaneo de puertos completado.")
        if st.button("⚠️ Reiniciar Todos los Nodos", type="secondary", use_container_width=True):
            st.warning("Comando de reinicio transmitido a la red.")
