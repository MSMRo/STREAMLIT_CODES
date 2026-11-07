"""
Tutorial 08: Interconexión de Arduino con Streamlit mediante Puerto Serie (PySerial)
===================================================================================
Aprende a conectar hardware físico (Arduino / ESP32) con una interfaz web en Streamlit.
Incluye un MODO SIMULACIÓN INTEGRADO para que puedas probar la aplicación
incluso si no tienes una placa Arduino conectada en este momento.
"""

import math
import random
import time
from typing import Dict, List, Optional
import pandas as pd
import serial
import serial.tools.list_ports
import streamlit as st

st.set_page_config(
    page_title="Tutorial 08 - Arduino y Serial con Streamlit",
    page_icon="🔌",
    layout="wide"
)

# =====================================================================
# CLASE CONTROLADORA: SOPORTA HARDWARE REAL Y MODO SIMULADO
# =====================================================================
class ArduinoSerialManager:
    """Gestiona la comunicación serie bidireccional de manera persistente."""
    def __init__(self, port: str, baudrate: int = 9600, simulated: bool = False):
        self.port = port
        self.baudrate = baudrate
        self.simulated = simulated
        self.ser: Optional[serial.Serial] = None
        self.connected = False
        self.history_logs: List[str] = []
        
        # Estado interno simulado
        self.sim_led = False
        self.sim_pwm = 0
        self.sim_tick = 0
        
        self.connect()

    def log(self, message: str):
        timestamp = time.strftime("%H:%M:%S")
        self.history_logs.append(f"[{timestamp}] {message}")
        # Mantener solo los últimos 20 logs
        if len(self.history_logs) > 20:
            self.history_logs.pop(0)

    def connect(self) -> bool:
        if self.simulated:
            self.connected = True
            self.log(f"🟢 [SIMULADOR] Conectado a puerto virtual {self.port} a {self.baudrate} baudios.")
            return True
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1.0)
            # Esperar 2 segundos para que el Arduino complete el reinicio por DTR
            time.sleep(2.0)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            self.connected = True
            self.log(f"🟢 Conectado con éxito a puerto físico {self.port} ({self.baudrate} baud).")
            return True
        except Exception as e:
            self.connected = False
            self.log(f"🔴 Error al abrir {self.port}: {e}")
            return False

    def send_command(self, cmd: str) -> Optional[str]:
        if not self.connected:
            self.log("⚠️ Intento de envío sin conexión activa.")
            return None

        cmd_clean = cmd.strip()
        self.log(f"TX ➔ {cmd_clean}")

        if self.simulated:
            return self._handle_simulation_command(cmd_clean)

        try:
            mensaje = (cmd_clean + "\n").encode("utf-8")
            self.ser.write(mensaje)
            self.ser.flush()
            # Leer posible respuesta inmediata
            time.sleep(0.05)
            if self.ser.in_waiting > 0:
                respuesta = self.ser.readline().decode("utf-8", errors="ignore").strip()
                if respuesta:
                    self.log(f"RX ⬅ {respuesta}")
                    return respuesta
            return "ACK:SENT"
        except Exception as e:
            self.log(f"🔴 Error en envío: {e}")
            return None

    def _handle_simulation_command(self, cmd: str) -> str:
        if cmd == "LED:1":
            self.sim_led = True
            resp = "ACK:LED:1"
        elif cmd == "LED:0":
            self.sim_led = False
            resp = "ACK:LED:0"
        elif cmd.startswith("PWM:"):
            try:
                self.sim_pwm = int(cmd.split(":")[1])
                resp = f"ACK:PWM:{self.sim_pwm}"
            except Exception:
                resp = "ERR:INVALID_PWM"
        elif cmd == "READ":
            resp = self._generate_simulated_telemetry()
        else:
            resp = f"ERR:UNKNOWN_CMD:{cmd}"
        
        self.log(f"RX ⬅ [SIM] {resp}")
        return resp

    def _generate_simulated_telemetry(self) -> str:
        self.sim_tick += 1
        # Generar señales realistas: onda senoidal + ruido suave
        pot = int(512 + 400 * math.sin(self.sim_tick * 0.2) + random.uniform(-10, 10))
        pot = max(0, min(1023, pot))
        temp = round(22.0 + (pot / 1023.0) * 12.0 + random.uniform(-0.3, 0.3), 1)
        light = int(300 + 500 * math.cos(self.sim_tick * 0.1) + random.uniform(-15, 15))
        light = max(0, min(1023, light))
        led_val = 1 if self.sim_led else 0
        return f"DATA:POT={pot},TEMP={temp},LIGHT={light},LED={led_val},PWM={self.sim_pwm}"

    def read_telemetry(self) -> Optional[Dict[str, float]]:
        if not self.connected:
            return None

        linea = ""
        if self.simulated:
            linea = self._generate_simulated_telemetry()
        else:
            try:
                # Leer cualquier línea disponible en el buffer serie
                while self.ser and self.ser.in_waiting > 0:
                    raw = self.ser.readline().decode("utf-8", errors="ignore").strip()
                    if raw.startswith("DATA:"):
                        linea = raw
                # Si no llegó en streaming, solicitar lectura explícita
                if not linea:
                    self.ser.write(b"READ\n")
                    time.sleep(0.1)
                    linea = self.ser.readline().decode("utf-8", errors="ignore").strip()
            except Exception as e:
                self.log(f"🔴 Error de lectura: {e}")
                return None

        if linea and linea.startswith("DATA:"):
            self.log(f"RX ⬅ {linea}")
            return self._parse_telemetry_line(linea)
        return None

    def _parse_telemetry_line(self, line: str) -> Dict[str, float]:
        # Formato: DATA:POT=512,TEMP=24.5,LIGHT=620,LED=1,PWM=128
        datos: Dict[str, float] = {}
        payload = line.replace("DATA:", "")
        partes = payload.split(",")
        for parte in partes:
            if "=" in parte:
                k, v = parte.split("=")
                try:
                    datos[k.strip()] = float(v.strip())
                except ValueError:
                    pass
        return datos

    def disconnect(self):
        if self.ser and self.ser.is_open:
            try:
                self.ser.close()
            except Exception:
                pass
        self.connected = False
        self.log("🔌 Conexión cerrada.")


# =====================================================================
# CACHÉ DE RECURSO PERSISTENTE
# =====================================================================
# Es crucial usar @st.cache_resource para que la conexión no se abra
# ni se cierre en cada clic que el usuario hace en un botón o slider.
@st.cache_resource
def get_serial_manager(port: str, baudrate: int, simulated: bool) -> ArduinoSerialManager:
    return ArduinoSerialManager(port=port, baudrate=baudrate, simulated=simulated)


# =====================================================================
# INTERFAZ DE USUARIO STREAMLIT
# =====================================================================
st.title("🔌 Tutorial 08: Interconexión Arduino con Serial en Streamlit")
st.markdown("""
Esta aplicación demuestra cómo interactuar con microcontroladores mediante comunicación serial RS-232 / USB.
Puedes enviar órdenes a los pines digitales y analógicos de Arduino, así como recibir telemetría continua de sensores.
""")

st.divider()

# Detección de puertos COM del sistema
puertos_disponibles = [p.device for p in serial.tools.list_ports.comports()]
if not puertos_disponibles:
    puertos_disponibles = ["COM3 (No detectado)", "COM4 (No detectado)"]

# BARRA LATERAL: Configuración de Conexión
with st.sidebar:
    st.header("⚙️ Configuración del Puerto")
    
    modo_sim = st.toggle("🧪 Activar Modo Simulación", value=(len(serial.tools.list_ports.comports()) == 0),
                         help="Activa este modo si no tienes un Arduino físico conectado para probar todas las funciones inmediatamente.")
    
    if modo_sim:
        st.info("ℹ️ Modo Simulación ACTIVO. Se generarán datos sintéticos realistas.")
        puerto_sel = "VIRTUAL_COM"
    else:
        puerto_sel = st.selectbox("Selecciona Puerto COM:", options=puertos_disponibles)
    
    baud_sel = st.selectbox("Velocidad en Baudios:", options=[9600, 19200, 38400, 57600, 115200], index=0)
    
    col_conn1, col_conn2 = st.sidebar.columns(2)
    with col_conn1:
        conectar_btn = st.button("🔌 Conectar", use_container_width=True, type="primary")
    with col_conn2:
        desconectar_btn = st.button("❌ Desconectar", use_container_width=True)

# Instanciamos el manager con caché persistente
manager = get_serial_manager(puerto_sel, baud_sel, modo_sim)

if desconectar_btn:
    manager.disconnect()
    st.cache_resource.clear()
    st.rerun()

if conectar_btn and not manager.connected:
    manager.connect()
    st.rerun()

# Estado de la conexión
if manager.connected:
    st.success(f"🟢 **Conectado:** {manager.port} @ {manager.baudrate} baud | {'Modo Simulado' if manager.simulated else 'Hardware Físico'}")
else:
    st.warning("🟡 Dispositivo desconectado. Revisa el puerto COM o activa el Modo Simulación en la barra lateral.")

st.divider()

# Inicialización de historial de telemetría en session_state
if "telemetria_historial" not in st.session_state:
    st.session_state.telemetria_historial = []

# =====================================================================
# SECCIÓN 1: PANEL DE CONTROL DE ACTUADORES (TX)
# =====================================================================
st.header("1. Control de Actuadores (Streamlit ➔ Arduino)")
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 1, 1])

with col_ctrl1:
    with st.container(border=True):
        st.subheader("💡 LED Digital (Pin 13)")
        st.write("Envía comandos digitales `LED:1` y `LED:0`:")
        col_on, col_off = st.columns(2)
        with col_on:
            if st.button("🟢 Encender LED", use_container_width=True, disabled=not manager.connected):
                manager.send_command("LED:1")
        with col_off:
            if st.button("🔴 Apagar LED", use_container_width=True, disabled=not manager.connected):
                manager.send_command("LED:0")

with col_ctrl2:
    with st.container(border=True):
        st.subheader("⚡ Salida PWM (Pin 9)")
        st.write("Ajusta el ciclo de trabajo de 0 (0V) a 255 (5V):")
        pwm_val = st.slider("Valor PWM:", min_value=0, max_value=255, value=128, step=5, key="pwm_slider")
        if st.button("Enviar PWM", use_container_width=True, disabled=not manager.connected):
            manager.send_command(f"PWM:{pwm_val}")

with col_ctrl3:
    with st.container(border=True):
        st.subheader("⌨️ Consola de Comandos Directos")
        cmd_manual = st.text_input("Comando personalizado:", value="READ", placeholder="Ej: LED:1, PWM:200, READ")
        if st.button("Enviar Comando TX", use_container_width=True, disabled=not manager.connected):
            if cmd_manual:
                manager.send_command(cmd_manual)

st.divider()

# =====================================================================
# SECCIÓN 2: TELEMETRÍA Y SENSORES EN TIEMPO REAL (RX)
# =====================================================================
st.header("2. Monitoreo de Sensores en Vivo (Arduino ➔ Streamlit)")

col_btn_read, col_clear_hist = st.columns([2, 1])
with col_btn_read:
    leer_ahora = st.button("🔄 Leer Sensores Ahora", type="primary", use_container_width=True, disabled=not manager.connected)
with col_clear_hist:
    if st.button("🗑️ Borrar Historial Gráfico", use_container_width=True):
        st.session_state.telemetria_historial = []
        st.rerun()

# Lectura periódica si se presiona o si hay telemetría
datos_actuales = None
if leer_ahora and manager.connected:
    datos_actuales = manager.read_telemetry()
    if datos_actuales:
        datos_actuales["Timestamp"] = time.strftime("%H:%M:%S")
        st.session_state.telemetria_historial.append(datos_actuales)
        # Mantener últimas 30 lecturas
        if len(st.session_state.telemetria_historial) > 30:
            st.session_state.telemetria_historial.pop(0)

# Mostrar últimas lecturas en métricas
if st.session_state.telemetria_historial:
    ultima = st.session_state.telemetria_historial[-1]
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Potenciómetro (A0)", f"{int(ultima.get('POT', 0))} / 1023")
    with col_m2:
        st.metric("Temperatura Estimada", f"{ultima.get('TEMP', 0.0):.1f} °C")
    with col_m3:
        st.metric("Sensor de Luz LDR (A1)", f"{int(ultima.get('LIGHT', 0))}")
    with col_m4:
        st.metric("Estado Actuadores", f"LED: {'ON' if ultima.get('LED', 0) == 1 else 'OFF'} | PWM: {int(ultima.get('PWM', 0))}")

    # Gráfico interactivo en vivo del historial
    df_hist = pd.DataFrame(st.session_state.telemetria_historial).set_index("Timestamp")
    st.subheader("Evolución Temporal de las Señales")
    st.line_chart(df_hist[["POT", "LIGHT", "TEMP"]])
else:
    st.info("Presiona '🔄 Leer Sensores Ahora' para adquirir los primeros datos de telemetría.")

st.divider()

# =====================================================================
# SECCIÓN 3: TERMINAL DE LOGS SERIE
# =====================================================================
with st.expander("📜 Ver Terminal y Registro de Comunicación Serie (TX/RX)", expanded=True):
    if manager.history_logs:
        st.code("\n".join(manager.history_logs), language="log")
    else:
        st.caption("No hay registros en el buffer aún.")

st.divider()
st.info("💡 Ejecuta este tutorial con: `uv run streamlit run 08_arduino_serial_hardware/app.py`")
