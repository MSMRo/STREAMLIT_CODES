# Tutorial 11: Dashboard IoT en Streamlit con MQTT y Broker Mosquitto

En este tutorial aprenderás a integrar el protocolo **MQTT** (Message Queuing Telemetry Transport) en Streamlit, el estándar de comunicación de baja latencia para sistemas embebidos, robótica y telemetría de campo con placas **ESP32**, **ESP8266** o **Raspberry Pi**.

---

## 🎯 Objetivos de Aprendizaje
- Comprender el modelo de mensajería **Publicador / Suscriptor** (*Pub/Sub*) y la jerarquía de tópicos en MQTT.
- Gestionar un cliente `paho-mqtt` asíncrono con hilos en segundo plano (`loop_start()`) y mantenerlo persistente en Streamlit mediante `@st.cache_resource`.
- Diseñar un emulador de ESP32 que publique mediciones ambientales (temperatura, humedad, RSSI WiFi) y ejecute comandos recibidos remotamente (control de relés).
- Interactuar con Brokers MQTT locales (**Eclipse Mosquitto**) o brokers públicos de prueba en la nube (**EMQX** o **test.mosquitto.org**).
- Probar el sistema mediante herramientas de consola como `mosquitto_pub` y `mosquitto_sub`.

---

## 🏗️ Arquitectura de Mensajería MQTT

```
┌──────────────────────┐          PUBLISH (Telemetría)
│   ESP32 (Hardware)   │ ─────────────────────────────────────────┐
│          o           │                                          │
│  Simulador Python    │          SUBSCRIBE (Comandos)            │
│                      │ <──────────────────────────────────────┐ │
└──────────────────────┘                                        │ │
                                                                ▼ ▼
                                                     ┌──────────────────────┐
                                                     │    BROKER MQTT       │
                                                     │  (Mosquitto / EMQX)  │
                                                     │     Puerto 1883      │
                                                     └──────────────────────┘
                                                                ▲ ▲
                                          SUBSCRIBE (Telemetría)│ │ PUBLISH (Comandos)
                                          ──────────────────────┘ └───────────────────
                                                     ┌──────────────────────┐
                                                     │ Streamlit Dashboard  │
                                                     └──────────────────────┘
```

---

## 🚀 Cómo Ejecutar Este Tutorial

### Paso 1: Iniciar el Simulador de ESP32 (Terminal 1)
```bash
uv run python 11_iot_mqtt_mosquitto_dashboard/simulator_esp32_mqtt.py
```
El simulador se conectará automáticamente al broker `broker.emqx.io` y comenzará a emitir telemetría cada 2 segundos.

### Paso 2: Iniciar el Dashboard en Streamlit (Terminal 2)
```bash
uv run streamlit run 11_iot_mqtt_mosquitto_dashboard/app.py
```
Verás cómo los mensajes MQTT son capturados inmediatamente por la aplicación sin necesidad de refrescar la página manualmente.

---

## 💻 Pruebas desde la Consola con Mosquitto CLI

Si tienes instalado Mosquitto en tu sistema, puedes probar la mensajería directamente desde tu terminal:

**1. Escuchar la telemetría en tiempo real:**
```bash
mosquitto_sub -h broker.emqx.io -t "iot/sensores/ESP32_MQTT_01/telemetria" -v
```

**2. Enviar una orden de encendido de relé a la ESP32:**
```bash
mosquitto_pub -h broker.emqx.io -t "iot/sensores/ESP32_MQTT_01/comandos" -m '{"action":"SET_RELAY","value":true}'
```
Verás cómo el simulador de la ESP32 imprime de inmediato la recepción de la orden y actualiza su estado.
