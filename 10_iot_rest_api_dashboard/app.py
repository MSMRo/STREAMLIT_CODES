"""
Tutorial 10: Dashboard IoT en Streamlit con Comunicación REST (ESP32 y Postman)
================================================================================
Este panel monitorea en tiempo real los datos transmitidos por un microcontrolador
ESP32 (o peticiones enviadas desde Postman) a través de un backend REST API con FastAPI.
"""

from datetime import datetime
import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="Tutorial 10 - Dashboard IoT REST",
    page_icon="🌐",
    layout="wide"
)

API_URL = "http://localhost:8000"

st.title("🌐 Tutorial 10: Dashboard IoT con API REST y Simulación ESP32")
st.write(
    "Aprende la arquitectura estándar en IoT comercial e industrial: el microcontrolador "
    "transmite datos en formato JSON mediante peticiones HTTP POST a un Gateway REST, "
    "y el Dashboard en Streamlit consulta y visualiza la información de forma desacoplada."
)

st.divider()

# Barra Lateral: Configuración de la API y Estado
with st.sidebar:
    st.header("⚙️ Conexión Gateway REST")
    url_servidor = st.text_input("URL de la API:", value=API_URL)
    dispositivo_id = st.text_input("ID del Dispositivo objetivo:", value="ESP32_LAB_01")
    
    # Comprobar salud del servidor FastAPI
    servidor_online = False
    try:
        resp_health = requests.get(f"{url_servidor}/", timeout=1.0)
        if resp_health.status_code == 200:
            servidor_online = True
    except Exception:
        servidor_online = False

    if servidor_online:
        st.success("🟢 Servidor FastAPI Conectado")
    else:
        st.error("🔴 Servidor FastAPI Desconectado")
        st.caption("Inicia el servidor con: `uv run uvicorn 10_iot_rest_api_dashboard.server_api:app --reload --port 8000`")

    st.divider()
    usar_muestra_local = st.toggle("🧪 Usar Datos Simulados Locales", value=not servidor_online,
                                   help="Activa para previsualizar el panel si el servidor FastAPI no está corriendo.")

# Helper functions para comunicarse con la API
def obtener_historial_api(base_url: str, dev_id: str, limit: int = 40):
    try:
        r = requests.get(f"{base_url}/api/telemetry/history?limit={limit}&device_id={dev_id}", timeout=2.0)
        if r.status_code == 200:
            return r.json().get("data", [])
    except Exception:
        pass
    return []

def enviar_comando_api(base_url: str, dev_id: str, cmd: str, param: str):
    try:
        payload = {"device_id": dev_id, "command": cmd, "parameter": param}
        r = requests.post(f"{base_url}/api/commands", json=payload, timeout=2.0)
        return r.status_code == 201
    except Exception as e:
        st.error(f"Error al enviar orden: {e}")
        return False

# Pestañas principales
tab_dashboard, tab_postman, tab_arquitectura = st.tabs([
    "📊 Panel de Telemetría",
    "📬 Pruebas con Postman y cURL",
    "🏗️ Arquitectura del Sistema"
])

# -------------------------------------------------------------
# TAB 1: DASHBOARD DE TELEMETRÍA
# -------------------------------------------------------------
with tab_dashboard:
    col_ref1, col_ref2 = st.columns([3, 1])
    with col_ref1:
        st.subheader(f"Telemetría en Vivo: `{dispositivo_id}`")
    with col_ref2:
        if st.button("🔄 Refrescar Datos", use_container_width=True, type="primary"):
            st.rerun()

    # Obtener lecturas
    registros = []
    if servidor_online and not usar_muestra_local:
        registros = obtener_historial_api(url_servidor, dispositivo_id)
    else:
        # Generar lecturas de muestra sintéticas
        import math, random
        ahora = datetime.now()
        for i in range(25):
            t_hora = ahora.timestamp() - (25 - i) * 3
            ts_str = datetime.fromtimestamp(t_hora).strftime("%H:%M:%S")
            registros.append({
                "device_id": dispositivo_id,
                "temperature": round(25.0 + 3.0 * math.sin(i * 0.3) + random.uniform(-0.2, 0.2), 2),
                "humidity": round(60.0 - 8.0 * math.sin(i * 0.3) + random.uniform(-0.5, 0.5), 1),
                "pressure": round(1013.2 + random.uniform(-0.3, 0.3), 1),
                "battery": max(10, 95 - int(i * 0.4)),
                "timestamp": ts_str
            })

    if registros:
        ultimo = registros[-1]
        
        # Tarjetas de Métricas (KPIs)
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.metric(
                label="🌡️ Temperatura",
                value=f"{ultimo.get('temperature', 0.0):.1f} °C",
                delta=f"{round(ultimo.get('temperature', 0.0) - registros[-2].get('temperature', 0.0), 2)} °C" if len(registros) > 1 else None
            )
        with kpi2:
            st.metric(
                label="💧 Humedad Relativa",
                value=f"{ultimo.get('humidity', 0.0):.1f} %",
                delta=f"{round(ultimo.get('humidity', 0.0) - registros[-2].get('humidity', 0.0), 1)} %" if len(registros) > 1 else None
            )
        with kpi3:
            st.metric(
                label="🧭 Presión Atmosférica",
                value=f"{ultimo.get('pressure', 0.0):.1f} hPa"
            )
        with kpi4:
            bat = int(ultimo.get("battery", 100))
            icono_bat = "🔋" if bat > 30 else "🪫"
            st.metric(label=f"{icono_bat} Nivel de Batería", value=f"{bat}%")

        # Gráficas de Series Temporales
        df_plot = pd.DataFrame(registros)
        df_plot_indexed = df_plot.set_index("timestamp")
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.write("#### Evolución de Temperatura y Humedad")
            st.line_chart(df_plot_indexed[["temperature", "humidity"]])
        with col_g2:
            st.write("#### Presión Barométrica y Batería")
            st.line_chart(df_plot_indexed[["pressure", "battery"]])

        # Tabla de Datos
        with st.expander("📋 Ver últimos registros crudos recibidos", expanded=False):
            st.dataframe(df_plot, use_container_width=True, hide_index=True)
    else:
        st.info("No se han recibido paquetes de telemetría todavía. Inicia el simulador de la ESP32 o envía datos desde Postman.")

    st.divider()

    # Panel de Control de Actuadores (Envío de comandos al microcontrolador)
    st.header("🎛️ Control Remoto de Actuadores (Streamlit ➔ ESP32)")
    st.write("Envía órdenes que quedarán encoladas en el Gateway para ser leídas por la placa en su próximo ciclo de polling:")
    
    col_act1, col_act2, col_act3 = st.columns(3)
    
    with col_act1:
        with st.container(border=True):
            st.subheader("⚡ Relé de Potencia")
            col_ron, col_roff = st.columns(2)
            with col_ron:
                if st.button("🟢 Activar Relé", use_container_width=True):
                    if servidor_online:
                        if enviar_comando_api(url_servidor, dispositivo_id, "SET_RELAY", "ON"):
                            st.success("Comando 'SET_RELAY:ON' encolado.")
                    else:
                        st.info("[Simulado] Relé encendido.")
            with col_roff:
                if st.button("🔴 Desactivar Relé", use_container_width=True):
                    if servidor_online:
                        if enviar_comando_api(url_servidor, dispositivo_id, "SET_RELAY", "OFF"):
                            st.success("Comando 'SET_RELAY:OFF' encolado.")
                    else:
                        st.info("[Simulado] Relé apagado.")

    with col_act2:
        with st.container(border=True):
            st.subheader("🔄 Reinicio Remoto")
            st.write("Solicita un reinicio por software (Watchdog / ESP.restart()):")
            if st.button("⚠️ Reiniciar Placa ESP32", use_container_width=True, type="secondary"):
                if servidor_online:
                    if enviar_comando_api(url_servidor, dispositivo_id, "REBOOT", "FORCE"):
                        st.warning("Comando 'REBOOT' encolado.")
                else:
                    st.warning("[Simulado] Orden de reinicio enviada.")

    with col_act3:
        with st.container(border=True):
            st.subheader("📡 Inyección Manual de Datos")
            st.write("Inyecta una lectura manual a través del endpoint HTTP:")
            temp_man = st.number_input("Temp (°C):", value=28.5, step=0.5)
            hum_man = st.number_input("Humedad (%):", value=55.0, step=1.0)
            if st.button("Enviar HTTP POST Manual"):
                if servidor_online:
                    payload_man = {
                        "device_id": dispositivo_id,
                        "temperature": temp_man,
                        "humidity": hum_man,
                        "pressure": 1013.25,
                        "battery": 99
                    }
                    r_inj = requests.post(f"{url_servidor}/api/telemetry", json=payload_man)
                    if r_inj.status_code == 201:
                        st.success("¡Lectura inyectada con éxito!")
                        st.rerun()

# -------------------------------------------------------------
# TAB 2: POSTMAN Y cURL
# -------------------------------------------------------------
with tab_postman:
    st.header("📬 Pruebas con Postman y Comandos cURL")
    st.markdown("""
    Puedes usar [Postman](https://www.postman.com/) o la terminal de Windows / Linux para simular envíos de telemetría hacia este sistema.
    
    ### 📥 Importar Colección de Postman
    En la carpeta de este tutorial encontrarás el archivo [`postman_collection.json`](file:///e:/PROJECTS/STREAMLIT_CODES/10_iot_rest_api_dashboard/postman_collection.json).
    1. Abre **Postman**.
    2. Haz clic en **Import** (arriba a la izquierda).
    3. Selecciona el archivo `postman_collection.json`.
    4. Tendrás listas todas las peticiones listas para enviar con un solo clic.
    """)
    
    st.subheader("💻 Comandos cURL para probar desde tu Terminal:")
    
    st.write("**1. Simular envío de telemetría de ESP32 (HTTP POST):**")
    st.code("""curl -X POST "http://localhost:8000/api/telemetry" \\
  -H "Content-Type: application/json" \\
  -d '{"device_id": "ESP32_LAB_01", "temperature": 27.4, "humidity": 63.2, "pressure": 1012.8, "battery": 91}'
""", language="bash")
    
    st.write("**2. Consultar la última telemetría recibida (HTTP GET):**")
    st.code("""curl -X GET "http://localhost:8000/api/telemetry/latest?device_id=ESP32_LAB_01"
""", language="bash")
    
    st.write("**3. Enviar orden de encendido de relé desde Postman/cURL:**")
    st.code("""curl -X POST "http://localhost:8000/api/commands" \\
  -H "Content-Type: application/json" \\
  -d '{"device_id": "ESP32_LAB_01", "command": "SET_RELAY", "parameter": "ON"}'
""", language="bash")

# -------------------------------------------------------------
# TAB 3: ARQUITECTURA
# -------------------------------------------------------------
with tab_arquitectura:
    st.header("🏗️ Arquitectura Desacoplada IoT con REST")
    st.markdown("""
    ```
    ┌──────────────────────┐          HTTP POST JSON
    │   ESP32 (Hardware)   │ ───────────────────────────────┐
    │          o           │                                │
    │ Simulador Python     │          HTTP GET Polling      │
    │          o           │ <────────────────────────────┐ │
    │       Postman        │                              │ │
    └──────────────────────┘                              ▼ ▼
                                               ┌──────────────────────┐
                                               │   FastAPI Gateway    │ (Puerto 8000)
                                               │  (Buffer / Memoria)  │
                                               └──────────────────────┘
                                                          ▲
                                                          │ HTTP GET / POST
                                                          ▼
                                               ┌──────────────────────┐
                                               │ Streamlit Dashboard  │ (Puerto 8501)
                                               └──────────────────────┘
    ```
    
    ### ¿Por qué esta arquitectura es superior para REST?
    1. **Desacoplamiento total:** La ESP32 no necesita conocer la existencia de Streamlit ni esperar a que un usuario abra la página web.
    2. **Persistencia temporal:** Si el usuario cierra el navegador, las lecturas de la ESP32 siguen acumulándose en el Gateway.
    3. **Escalabilidad:** Cientos de microcontroladores ESP32 pueden publicar telemetría de forma concurrente hacia la API sin saturar la interfaz de usuario.
    """)

st.divider()
st.info("💡 Ejecuta este tutorial con: `uv run streamlit run 10_iot_rest_api_dashboard/app.py`")
