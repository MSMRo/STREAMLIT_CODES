"""
Simulador de Placa ESP32 con Cliente MQTT (Paho-MQTT)
=====================================================
Este script emula un microcontrolador ESP32 conectado por WiFi a un Broker MQTT
(Eclipse Mosquitto o EMQX). Publica telemetría periódica en un tópico y escucha
órdenes de control en un tópico de comandos.

Para ejecutar:
    uv run python 11_iot_mqtt_mosquitto_dashboard/simulator_esp32_mqtt.py
"""

import json
import math
import random
import time
import paho.mqtt.client as mqtt

# Configuración del Broker
# Puedes usar 'localhost' si tienes Mosquitto instalado localmente,
# o usar el broker público de pruebas 'broker.emqx.io' o 'test.mosquitto.org'
BROKER = "broker.emqx.io"
PORT = 1883
DEVICE_ID = "ESP32_MQTT_01"

# Tópicos MQTT (Convención jerárquica)
TOPIC_TELEMETRY = f"iot/sensores/{DEVICE_ID}/telemetria"
TOPIC_COMMANDS = f"iot/sensores/{DEVICE_ID}/comandos"

print("=" * 65)
print(f"📡 Iniciando Emulador ESP32 MQTT [{DEVICE_ID}]")
print(f"🌐 Broker: {BROKER}:{PORT}")
print(f"📤 Publicando en: {TOPIC_TELEMETRY}")
print(f"📥 Suscrito a:   {TOPIC_COMMANDS}")
print("Presiona Ctrl+C para detener la simulación.")
print("=" * 65)

estado_rele = False
uptime = 0

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"[{time.strftime('%H:%M:%S')}] 🟢 Conectado exitosamente al Broker MQTT!")
        # Suscribirse al tópico de órdenes
        client.subscribe(TOPIC_COMMANDS, qos=1)
        print(f"[{time.strftime('%H:%M:%S')}] 📥 Escuchando órdenes en: {TOPIC_COMMANDS}")
    else:
        print(f"🔴 Error de conexión con código: {rc}")

def on_message(client, userdata, msg):
    global estado_rele
    try:
        payload_str = msg.payload.decode("utf-8")
        print(f"[{time.strftime('%H:%M:%S')}] 📩 Mensaje recibido en [{msg.topic}]: {payload_str}")
        comando = json.loads(payload_str)
        
        accion = comando.get("action")
        valor = comando.get("value")
        
        if accion == "SET_RELAY":
            estado_rele = bool(valor)
            print(f"      ⚡ [ACTUADOR] Relé físico cambiado a: {'ACTIVADO (ON)' if estado_rele else 'DESACTIVADO (OFF)'}")
        elif accion == "PING":
            print("      🏓 [PONG] Ping recibido desde el Dashboard.")
    except Exception as e:
        print(f"❌ Error al procesar comando MQTT: {e}")

# Inicializar cliente MQTT (usando protocolo moderno CallbackAPIVersion.VERSION2)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"sim_{DEVICE_ID}_{random.randint(100, 999)}")
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER, PORT, keepalive=60)
except Exception as e:
    print(f"🔴 No se pudo conectar al broker {BROKER}: {e}")
    print("Verifica tu conexión a internet o asegúrate de que el broker local Mosquitto esté corriendo.")
    exit(1)

client.loop_start()

step = 0
try:
    while True:
        step += 1
        uptime += 2
        
        # Generar lecturas de sensores
        temp = round(23.5 + 4.5 * math.sin(step * 0.12) + random.uniform(-0.2, 0.2), 2)
        hum = round(55.0 - 10.0 * math.sin(step * 0.12) + random.uniform(-0.5, 0.5), 1)
        rssi = int(-60 + random.uniform(-8, 5))  # Potencia señal WiFi (dBm)
        
        datos = {
            "device_id": DEVICE_ID,
            "temperature": temp,
            "humidity": hum,
            "wifi_rssi_dbm": rssi,
            "relay_active": estado_rele,
            "uptime_seconds": uptime,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        payload_json = json.dumps(datos)
        client.publish(TOPIC_TELEMETRY, payload_json, qos=0)
        print(f"[{time.strftime('%H:%M:%S')}] ⬆️ TX MQTT: Temp={temp}°C | Hum={hum}% | RSSI={rssi}dBm | Relé={estado_rele}")
        
        time.sleep(2.0)
except KeyboardInterrupt:
    print("\nDeteniendo cliente ESP32...")
    client.loop_stop()
    client.disconnect()
    print("Desconectado.")
