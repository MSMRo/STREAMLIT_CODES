"""
Dashboard Hub: Navegador Central de Tutoriales de Streamlit
==========================================================
Este panel maestro te permite explorar todo el catálogo de tutoriales,
inspeccionar el código fuente y la documentación de cada módulo, y verificar
el entorno de ejecución (Python, UV, Streamlit y puertos serie).
"""

from pathlib import Path
import sys
import pandas as pd
import serial.tools.list_ports
import streamlit as st

st.set_page_config(
    page_title="Streamlit Masterclass - Hub de Tutoriales",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Streamlit Masterclass: Hub de Tutoriales con Python y UV")
st.markdown("""
¡Bienvenido! Este repositorio contiene una colección completa y modular de tutoriales prácticos diseñados
para dominar **Streamlit** desde cero hasta aplicaciones avanzadas con hardware y comunicación serial.
""")

st.divider()

# Barra lateral con información del sistema
with st.sidebar:
    st.header("🖥️ Estado del Entorno")
    st.write(f"**Python:** `{sys.version.split()[0]}`")
    st.write(f"**Streamlit:** `{st.__version__}`")
    st.write("**Gestor:** `uv`")
    
    puertos = [p.device for p in serial.tools.list_ports.comports()]
    st.write(f"**Puertos COM detectados:** `{len(puertos)}`")
    if puertos:
        for p in puertos:
            st.caption(f"• {p}")
    else:
        st.caption("• Ninguno conectado (Modo Simulación disponible)")
    
    st.divider()
    st.caption("Estructura 100% modular con documentación individual.")

# Directorio base
BASE_DIR = Path(__file__).resolve().parent

# Catálogo de tutoriales
TUTORIALES = [
    {
        "id": "01",
        "folder": "01_fundamentos_y_texto",
        "titulo": "01. Fundamentos y Visualización de Texto",
        "icono": "📝",
        "descripcion": "Modelo reactivo de Streamlit, st.write, markdown con colores, LaTeX, métricas y mensajes de estado.",
        "comando": "uv run streamlit run 01_fundamentos_y_texto/app.py"
    },
    {
        "id": "02",
        "folder": "02_widgets_e_inputs",
        "titulo": "02. Widgets, Entradas y Formularios",
        "icono": "🎛️",
        "descripcion": "Botones, sliders, selectores, inputs de texto, fechas, colores y agrupación con st.form.",
        "comando": "uv run streamlit run 02_widgets_e_inputs/app.py"
    },
    {
        "id": "03",
        "folder": "03_estado_y_sesion_state",
        "titulo": "03. Manejo de Estado (Session State)",
        "icono": "🧠",
        "descripcion": "Persistencia de variables con st.session_state, callbacks on_click/on_change, ToDo list y Wizards.",
        "comando": "uv run streamlit run 03_estado_y_sesion_state/app.py"
    },
    {
        "id": "04",
        "folder": "04_layouts_y_contenedores",
        "titulo": "04. Layouts, Contenedores y Modales",
        "icono": "📐",
        "descripcion": "Barra lateral (sidebar), columnas dinámicas, pestañas (tabs), acordeones (expander) y modales (@st.dialog).",
        "comando": "uv run streamlit run 04_layouts_y_contenedores/app.py"
    },
    {
        "id": "05",
        "folder": "05_multimedia_y_archivos",
        "titulo": "05. Multimedia y Manejo de Archivos",
        "icono": "🎬",
        "descripcion": "Filtros de imagen en vivo con PIL, síntesis de audio senoidal con NumPy, video, cámara web y carga/descarga de datos.",
        "comando": "uv run streamlit run 05_multimedia_y_archivos/app.py"
    },
    {
        "id": "06",
        "folder": "06_visualizacion_y_datos",
        "titulo": "06. Visualización de Datos y Gráficos",
        "icono": "📊",
        "descripcion": "DataFrames formateados, editor de tablas interactivo (st.data_editor), gráficos nativos y gráficos 2D/3D con Plotly.",
        "comando": "uv run streamlit run 06_visualizacion_y_datos/app.py"
    },
    {
        "id": "07",
        "folder": "07_rendimiento_y_cache",
        "titulo": "07. Rendimiento y Caché (@st.cache_*)",
        "icono": "⚡",
        "descripcion": "Aceleración de apps con @st.cache_data (datasets) y @st.cache_resource (conexiones persistentes/hardware).",
        "comando": "uv run streamlit run 07_rendimiento_y_cache/app.py"
    },
    {
        "id": "08",
        "folder": "08_arduino_serial_hardware",
        "titulo": "08. Arduino y Comunicación Serie (PySerial)",
        "icono": "🔌",
        "descripcion": "Conexión con microcontroladores por puerto serie, control de LED/PWM, telemetría de sensores y Modo Simulación integrado.",
        "comando": "uv run streamlit run 08_arduino_serial_hardware/app.py"
    },
    {
        "id": "09",
        "folder": "09_aplicacion_multipagina",
        "titulo": "09. Aplicaciones Multipágina y Modularidad",
        "icono": "🧭",
        "descripcion": "Estructura estándar de proyectos multipágina usando la carpeta pages/ y sesión compartida entre vistas.",
        "comando": "uv run streamlit run 09_aplicacion_multipagina/app.py"
    },
    {
        "id": "10",
        "folder": "10_iot_rest_api_dashboard",
        "titulo": "10. Dashboard IoT REST (ESP32 y Postman)",
        "icono": "🌐",
        "descripcion": "Recepción de telemetría por HTTP POST/GET, simulación de ESP32 con requests, colección para Postman y control de relés.",
        "comando": "uv run streamlit run 10_iot_rest_api_dashboard/app.py"
    },
    {
        "id": "11",
        "folder": "11_iot_mqtt_mosquitto_dashboard",
        "titulo": "11. Dashboard IoT MQTT (Mosquitto y Paho)",
        "icono": "📡",
        "descripcion": "Arquitectura Pub/Sub con paho-mqtt en segundo plano, simulación ESP32 en tiempo real y comandos de actuación.",
        "comando": "uv run streamlit run 11_iot_mqtt_mosquitto_dashboard/app.py"
    },
    {
        "id": "12",
        "folder": "12_bases_de_datos_sqlite_postgresql",
        "titulo": "12. Bases de Datos (SQLite y PostgreSQL)",
        "icono": "🗄️",
        "descripcion": "Persistencia relacional con SQLAlchemy, CRUD completo, filtros de series temporales, consola SQL directa y Docker PostgreSQL.",
        "comando": "uv run streamlit run 12_bases_de_datos_sqlite_postgresql/app.py"
    }
]

# Tabs principales del Hub
tab_catalogo, tab_visor = st.tabs(["📚 Catálogo de Módulos", "🔍 Visor de Código y Documentación"])

with tab_catalogo:
    st.subheader("Selecciona y ejecuta cualquier módulo con UV")
    st.caption("Cada módulo es totalmente autónomo y cuenta con su propio script y README detallado.")
    
    for i in range(0, len(TUTORIALES), 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j
            if idx < len(TUTORIALES):
                tut = TUTORIALES[idx]
                with cols[j]:
                    with st.container(border=True):
                        st.subheader(f"{tut['icono']} {tut['titulo']}")
                        st.write(tut["descripcion"])
                        st.code(tut["comando"], language="bash")

with tab_visor:
    st.subheader("Explorador de Archivos en Tiempo Real")
    opciones_modulos = {tut["titulo"]: tut["folder"] for tut in TUTORIALES}
    seleccionado = st.selectbox("Elige un módulo para inspeccionar:", list(opciones_modulos.keys()))
    
    folder_sel = opciones_modulos[seleccionado]
    dir_path = BASE_DIR / folder_sel
    
    col_v1, col_v2 = st.columns([1, 1])
    
    with col_v1:
        st.subheader("📖 Documentación (`README.md`)")
        readme_path = dir_path / "README.md"
        if readme_path.exists():
            st.markdown(readme_path.read_text(encoding="utf-8"))
        else:
            st.warning("README no encontrado.")
            
    with col_v2:
        st.subheader("💻 Código Fuente (`app.py`)")
        app_path = dir_path / "app.py"
        if app_path.exists():
            st.code(app_path.read_text(encoding="utf-8"), language="python", line_numbers=True)
        else:
            st.warning("app.py no encontrado.")

st.divider()
st.markdown("💡 **Tip:** Para ejecutar este Hub central corre: `uv run streamlit run dashboard_hub.py`")
