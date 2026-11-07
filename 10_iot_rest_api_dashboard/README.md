# Tutorial 10: Dashboard IoT en Streamlit con Comunicación REST (ESP32 y Postman)

En este tutorial aprenderás la arquitectura estándar para monitoreo industrial y telemetría IoT basada en **APIs REST**, integrando un microcontrolador **ESP32** (o su emulador en Python), un backend en **FastAPI**, pruebas con **Postman** y visualización interactiva en **Streamlit**.

---

## 🎯 Objetivos de Aprendizaje
- Comprender la arquitectura cliente-servidor desacoplada para dispositivos embebidos.
- Diseñar endpoints REST con FastAPI para recepción de telemetría (`POST /api/telemetry`) y gestión de comandos encolados (`POST /api/commands`, `GET /api/commands/{id}`).
- Simular el ciclo de vida de una placa ESP32 transmitiendo mediciones ambientales y realizando sondeo (*polling*) de actuadores.
- Utilizar **Postman** (o `curl`) para enviar datos manuales y probar los endpoints de la API.
- Diseñar un Dashboard en Streamlit que consuma los endpoints REST y visualice KPIs, gráficos temporales y botones de control remoto.

---

## 🏗️ Arquitectura del Sistema

```
[ ESP32 / Simulador / Postman ]
             │
             │  (HTTP POST /api/telemetry)
             ▼
  [ FastAPI Gateway :8000 ]  <══════>  [ Streamlit Dashboard :8501 ]
             │                                (Consulta y Control)
             │  (HTTP GET /api/commands)
             ▼
    [ ESP32 ejecuta acción ]
```

---

## 🚀 Cómo Ejecutar Este Tutorial Paso a Paso

Para probar el flujo completo necesitarás 3 terminales (o puedes probar solo el Dashboard con datos simulados si prefieres):

### Paso 1: Iniciar el Servidor REST API (Terminal 1)
```bash
uv run uvicorn 10_iot_rest_api_dashboard.server_api:app --reload --port 8000
```
La documentación interactiva Swagger estará disponible en `http://localhost:8000/docs`.

### Paso 2: Iniciar el Simulador de ESP32 (Terminal 2)
```bash
uv run python 10_iot_rest_api_dashboard/simulator_esp32_rest.py
```
Verás cómo el simulador empieza a enviar telemetría (temperatura, humedad, presión, batería) cada 2 segundos.

### Paso 3: Iniciar el Dashboard en Streamlit (Terminal 3)
```bash
uv run streamlit run 10_iot_rest_api_dashboard/app.py
```
Abre tu navegador en `http://localhost:8501`. Verás las gráficas actualizarse en tiempo real con las lecturas transmitidas por el emulador.

---

## 📬 Pruebas con Postman y cURL

### A. Colección de Postman
Importa el archivo [`postman_collection.json`](file:///e:/PROJECTS/STREAMLIT_CODES/10_iot_rest_api_dashboard/postman_collection.json) directamente en Postman para probar:
1. `POST /api/telemetry`: Envío manual de lectura de sensor.
2. `GET /api/telemetry/latest`: Lectura más reciente.
3. `POST /api/commands`: Enviar orden de relé a la ESP32.
4. `GET /api/commands/{id}`: Lectura de comandos encolados.

### B. Probar desde la Terminal con cURL
```bash
curl -X POST "http://localhost:8000/api/telemetry" \
  -H "Content-Type: application/json" \
  -d '{"device_id": "ESP32_LAB_01", "temperature": 29.5, "humidity": 65.0, "pressure": 1012.3, "battery": 90}'
```
Al refrescar Streamlit, verás la nueva lectura inmediatamente reflejada en las métricas y la gráfica.
