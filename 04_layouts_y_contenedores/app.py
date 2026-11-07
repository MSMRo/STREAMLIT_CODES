"""
Tutorial 04: Layouts, Contenedores y Estructura Visual en Streamlit
==================================================================
Aprende a estructurar aplicaciones profesionales usando barras laterales
(st.sidebar), columnas con anchos personalizados, pestañas (st.tabs),
acordeones colapsables (st.expander), contenedores con borde y ventanas
modales (@st.dialog).
"""

import time
import streamlit as st

# 1. Configuración de la página (¡debe ser la primera llamada de Streamlit!)
st.set_page_config(
    page_title="Tutorial 04 - Layouts y Contenedores",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Barra Lateral (st.sidebar)
with st.sidebar:
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=70)
    st.title("Panel de Control")
    st.write("Configuraciones globales de la estación de monitoreo.")
    
    modo_operacion = st.radio("Modo de Operación:", ["Producción", "Calibración", "Mantenimiento"])
    frecuencia_muestreo = st.slider("Frecuencia (Hz):", 1, 100, 10)
    notificaciones = st.toggle("Activar Alertas por Email", value=True)
    
    st.divider()
    st.caption("Versión del Sistema: v2.4.0")

# 3. Título Principal
st.title("📐 Tutorial 04: Diseño de Interfaces y Layouts")
st.write(
    "Una buena disposición visual mejora drásticamente la usabilidad de una aplicación. "
    "Streamlit ofrece herramientas potentes para diseñar paneles limpios y responsivos."
)

st.divider()

# 4. Columnas con Anchos Personalizados (st.columns)
st.header("1. Grillas y Columnas (`st.columns`)")
st.write("Puedes especificar proporciones relativas como `[2, 1, 1]`:")

col_izq, col_centro, col_der = st.columns([2, 1, 1])

with col_izq:
    with st.container(border=True):
        st.subheader("Estado General del Sistema")
        st.write(f"Modo actual seleccionado: **{modo_operacion}**")
        st.write(f"Frecuencia configurada: **{frecuencia_muestreo} Hz**")
        if notificaciones:
            st.success("🟢 Alertas activadas y monitoreando en segundo plano.")
        else:
            st.warning("🟡 Alertas silenciadas.")

with col_centro:
    with st.container(border=True):
        st.metric(label="Presión Hidráulica", value="142.3 bar", delta="+2.1 bar")
        st.metric(label="Temperatura Sensor 1", value="38.5 °C", delta="-0.4 °C")

with col_der:
    with st.container(border=True):
        st.metric(label="Rendimiento Bomba", value="98.7%", delta="+1.2%")
        st.metric(label="Horas de Operación", value="1,240 h")

st.divider()

# 5. Pestañas de Navegación (st.tabs)
st.header("2. Pestañas de Navegación (`st.tabs`)")
tab1, tab2, tab3 = st.tabs(["📊 Gráficos y Telemetría", "⚙️ Parámetros de Calibración", "📜 Registro de Logs"])

with tab1:
    st.subheader("Monitoreo en Tiempo Real")
    st.line_chart([10, 15, 12, 18, 22, 19, 25, 27, 24, 30])
    st.caption("Telemetría de voltaje durante los últimos 10 segundos.")

with tab2:
    st.subheader("Ajuste de Ganancias PID")
    col_p, col_i, col_d = st.columns(3)
    with col_p:
        st.number_input("Ganancia Proporcional (Kp):", value=1.5, step=0.1)
    with col_i:
        st.number_input("Ganancia Integral (Ki):", value=0.05, step=0.01)
    with col_d:
        st.number_input("Ganancia Derivativa (Kd):", value=0.12, step=0.01)

with tab3:
    st.subheader("Eventos Recientes")
    st.code("""[2026-11-06 14:02:11] INFO: Puerto COM3 conectado con éxito a 9600 baudios.
[2026-11-06 14:02:15] DEBUG: Handshake recibido: ARDUINO_READY_OK.
[2026-11-06 14:03:00] INFO: Calibración de offset completada en sensor_01.
[2026-11-06 14:05:22] WARNING: Pico de corriente detectado en canal analógico A0 (4.98V).
""", language="log")

st.divider()

# 6. Acordeones Colapsables (st.expander)
st.header("3. Acordeones Plegables (`st.expander`)")
st.write("Ideales para ocultar detalles técnicos o manuales de ayuda para no saturar la vista:")

with st.expander("📖 Haz clic aquí para ver las instrucciones de calibración del sensor", expanded=False):
    st.markdown("""
    1. Asegúrate de desconectar la carga antes de iniciar la calibración.
    2. Ajusta el potenciómetro de cero hasta que la lectura marque exactamente `0.00 V`.
    3. Aplica la señal de prueba de referencia (5.00 V) y verifica que el valor no se desvíe más de `±0.05 V`.
    4. Guarda los valores presionando el botón de confirmación en la barra lateral.
    """)

# 7. Contenedores Dinámicos con st.empty
st.header("4. Actualizaciones Dinámicas en el Mismo Sitio (`st.empty`)")
st.write(
    "`st.empty()` crea un contenedor de espacio reservado (*placeholder*) cuyo contenido "
    "puede sobreescribirse dinámicamente sin mover el resto de elementos."
)

placeholder = st.empty()
if st.button("Simular Conexión y Progreso Dinámico"):
    for i in range(1, 101, 20):
        with placeholder.container():
            st.info(f"Conectando al microcontrolador... Progreso: {i}%")
            st.progress(i / 100)
        time.sleep(0.3)
    placeholder.success("✅ ¡Dispositivo conectado y sincronizado correctamente!")

st.divider()

# 8. Ventana Modal Emergente (@st.dialog)
st.header("5. Ventanas Modales Emergentes (`@st.dialog`)")
st.write("Permite solicitar confirmaciones críticas o formularios emergentes en un diálogo flotante.")

@st.dialog("Confirmación de Parada de Emergencia")
def modal_parada_emergencia():
    st.error("🚨 ¿Estás seguro de que deseas detener todos los actuadores inmediatamente?")
    st.write("Esta acción cortará la alimentación a los relés y motores del banco de pruebas.")
    
    col_cancel, col_confirm = st.columns(2)
    with col_cancel:
        if st.button("Cancelar", use_container_width=True):
            st.rerun()
    with col_confirm:
        if st.button("¡Confirmar Parada!", type="primary", use_container_width=True):
            st.session_state.parada_activada = True
            st.rerun()

if st.button("🛑 PARADA DE EMERGENCIA", type="primary"):
    modal_parada_emergencia()

if st.session_state.get("parada_activada", False):
    st.error("⚠️ SISTEMA BLOQUEADO: Parada de emergencia ejecutada.")
    if st.button("Reanudar Sistema"):
        st.session_state.parada_activada = False
        st.rerun()

st.divider()
st.info("💡 Ejecuta este tutorial con: `uv run streamlit run 04_layouts_y_contenedores/app.py`")
