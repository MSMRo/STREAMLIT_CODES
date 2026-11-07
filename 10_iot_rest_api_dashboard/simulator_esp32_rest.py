"""
Simulador de Placa ESP32 con Conectividad WiFi y Cliente REST
=============================================================
Este script emula el comportamiento de un microcontrolador ESP32
enviando lecturas periódicas de sensores mediante peticiones HTTP POST
y consultando comandos pendientes mediante HTTP GET.

Para ejecutar:
    uv run python 10_iot_rest_api_dashboard/simulator_esp32_rest.py
"""

import math
import random
import time
import requests

API_BASE_URL = "http://localhost:8000"
DEVICE_ID = "ESP32_LAB_01"

print("=" * 60)
print(f"📡 Iniciando Emulador de ESP32 WiFi [{DEVICE_ID}]")
print(f"🎯 Servidor Destino: {API_BASE_URL}")
print("Presiona Ctrl+C para detener la simulación.")
print("=" * 60)

step = 0
bateria_pct = 95
estado_rele = "OFF"

while True:
    step += 1
    
    # 1. Generación de telemetría física realista
    # Temperatura: Onda senoidal entre 21°C y 29°C con algo de ruido
    temperatura = round(25.0 + 4.0 * math.sin(step * 0.15) + random.uniform(-0.3, 0.3), 2)
    # Humedad: Correlación inversa con temperatura
    humedad = round(60.0 - 10.0 * math.sin(step * 0.15) + random.uniform(-1.0, 1.0), 1)
    # Presión barométrica estándar en hPa (1010 - 1016 hPa)
    presion = round(1013.25 + 2.0 * math.cos(step * 0.08) + random.uniform(-0.2, 0.2), 1)
    # Batería se va descargando muy lentamente
    if step % 20 == 0 and bateria_pct > 10:
        bateria_pct -= 1

    payload = {
        "device_id": DEVICE_ID,
        "temperature": temperatura,
        "humidity": humedad,
        "pressure": presion,
        "battery": bateria_pct
    }

    # 2. Transmisión HTTP POST hacia el servidor
    try:
        resp_post = requests.post(f"{API_BASE_URL}/api/telemetry", json=payload, timeout=2.0)
        if resp_post.status_code == 201:
            print(f"[{time.strftime('%H:%M:%S')}] ⬆️ POST Telemetría: Temp={temperatura}°C | Hum={humedad}% | Pres={presion}hPa | Bat={bateria_pct}% [OK]")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] ⚠️ Respuesta del servidor: {resp_post.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"[{time.strftime('%H:%M:%S')}] 🔴 Servidor no disponible en {API_BASE_URL}. Asegúrate de iniciar FastAPI primero:")
        print("     uv run uvicorn 10_iot_rest_api_dashboard.server_api:app --reload --port 8000")
        time.sleep(3.0)
        continue
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] ❌ Error de red: {e}")

    # 3. Sondeo periódico de comandos entrantes (Polling GET)
    try:
        resp_cmd = requests.get(f"{API_BASE_URL}/api/commands/{DEVICE_ID}", timeout=2.0)
        if resp_cmd.status_code == 200:
            comandos = resp_cmd.json().get("commands", [])
            for c in comandos:
                accion = c.get("command")
                param = c.get("parameter")
                print(f"[{time.strftime('%H:%M:%S')}] ⬇️ ¡Comando recibido del Dashboard! Acción='{accion}' Parámetro='{param}'")
                if accion == "SET_RELAY":
                    estado_rele = param
                    print(f"        ⚡ [ACTUADOR] Relé físico cambiado a: {estado_rele}")
                elif accion == "REBOOT":
                    print("        🔄 [SISTEMA] Reiniciando microcontrolador ESP32...")
                    time.sleep(1.0)
                    print("        ✅ [SISTEMA] ESP32 reiniciado y reconectado al WiFi.")
    except Exception:
        pass

    time.sleep(2.0)
