"""
Tutorial 09: Aplicaciones Multipágina y Navegación Modular en Streamlit
=======================================================================
Página principal / Entrypoint. En Streamlit, cuando creas una carpeta llamada
`pages/` junto al script principal, Streamlit genera automáticamente un menú
de navegación lateral con todas las subpáginas.
"""

import streamlit as st

st.set_page_config(
    page_title="App Multipágina - Inicio",
    page_icon="🧭",
    layout="wide"
)

# Inicializar estado global compartido entre todas las páginas
if "usuario_conectado" not in st.session_state:
    st.session_state.usuario_conectado = "Operador Lab #1"
if "modo_oscuro" not in st.session_state:
    st.session_state.modo_oscuro = True
if "visitas_totales" not in st.session_state:
    st.session_state.visitas_totales = 0

st.session_state.visitas_totales += 1

st.title("🧭 Tutorial 09: Aplicación Multipágina Modular")
st.write(
    "Cuando un proyecto crece, agrupar todo el código en un único archivo se vuelve inmanejable. "
    "Streamlit resuelve esto mediante su arquitectura multipágina: cualquier archivo `.py` ubicado "
    "dentro de la carpeta `pages/` se convierte en una ruta de navegación automática."
)

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Bienvenido al Centro de Control Industrial")
    st.markdown(f"""
    - **Operador actual:** `{st.session_state.usuario_conectado}`
    - **Navegaciones registradas en esta sesión:** `{st.session_state.visitas_totales}`
    
    ### 📂 Estructura de Páginas de este Proyecto:
    1. **🏠 Inicio (`app.py`):** Visión general y estado de la sesión compartida.
    2. **📊 Análisis de Datos (`pages/1_analisis_datos.py`):** Gráficos, métricas y filtros analíticos.
    3. **🔌 Dispositivos IoT (`pages/2_dispositivos_iot.py`):** Monitoreo de placas Arduino y sensores.
    4. **⚙️ Configuración (`pages/3_configuracion.py`):** Preferencias globales del sistema.
    """)
    st.info("👈 Utiliza el menú en la barra lateral para navegar entre las diferentes secciones.")

with col2:
    with st.container(border=True):
        st.subheader("Estado Global del Sistema")
        st.metric("Nodos Conectados", "8 / 8", delta="100% Online")
        st.metric("Latencia de Red", "14 ms", delta="-2 ms")
        st.metric("Temperatura Media", "23.4 °C")

st.divider()
st.info("💡 Ejecuta esta aplicación multipágina con: `uv run streamlit run 09_aplicacion_multipagina/app.py`")
