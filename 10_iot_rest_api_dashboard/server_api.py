"""
Servidor REST API para Telemetría IoT y Comandos (FastAPI)
==========================================================
Este backend recibe datos de telemetría de dispositivos embebidos
(como una placa ESP32 física, el simulador en Python o Postman)
y expone endpoints para ser consumidos por el dashboard en Streamlit.

Para ejecutar este servidor:
    uv run uvicorn 10_iot_rest_api_dashboard.server_api:app --reload --port 8000
"""

from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="IoT ESP32 REST API Gateway",
    description="API para recepción de telemetría de microcontroladores y envío de comandos",
    version="1.0.0"
)

# Permitir CORS para comunicación abierta
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------
# MODELOS DE DATOS (PYDANTIC)
# ---------------------------------------------------------------------
class TelemetryPayload(BaseModel):
    device_id: str = Field(..., example="ESP32_LAB_01")
    temperature: float = Field(..., example=24.8)
    humidity: float = Field(..., example=58.5)
    pressure: float = Field(..., example=1013.2)
    battery: int = Field(..., ge=0, le=100, example=87)
    timestamp: Optional[str] = None

class CommandPayload(BaseModel):
    device_id: str = Field(..., example="ESP32_LAB_01")
    command: str = Field(..., example="SET_RELAY")
    parameter: Optional[str] = Field("ON", example="ON")
    timestamp: Optional[str] = None

# ---------------------------------------------------------------------
# ALMACENAMIENTO EN MEMORIA
# ---------------------------------------------------------------------
telemetry_db: List[Dict] = []
pending_commands: Dict[str, List[Dict]] = {}

# ---------------------------------------------------------------------
# ENDPOINTS DE TELEMETRÍA (ESP32 / POSTMAN ➔ SERVIDOR)
# ---------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "online",
        "service": "IoT REST API Gateway",
        "total_readings": len(telemetry_db),
        "docs_url": "/docs"
    }

@app.post("/api/telemetry", status_code=201)
def receive_telemetry(payload: TelemetryPayload):
    """
    Endpoint invocado por la ESP32 (o Postman) mediante un HTTP POST con cuerpo JSON.
    """
    record = payload.model_dump()
    if not record.get("timestamp"):
        record["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    telemetry_db.append(record)
    # Mantener en memoria los últimos 200 registros
    if len(telemetry_db) > 200:
        telemetry_db.pop(0)

    return {
        "status": "success",
        "message": f"Telemetría registrada para {payload.device_id}",
        "received_at": record["timestamp"]
    }

@app.get("/api/telemetry/latest")
def get_latest_telemetry(device_id: Optional[str] = None):
    """
    Retorna la lectura más reciente para el dashboard en Streamlit.
    """
    if not telemetry_db:
        return {"status": "empty", "data": None}
    
    if device_id:
        for item in reversed(telemetry_db):
            if item["device_id"] == device_id:
                return {"status": "success", "data": item}
        raise HTTPException(status_code=404, detail=f"No hay lecturas para el dispositivo {device_id}")

    return {"status": "success", "data": telemetry_db[-1]}

@app.get("/api/telemetry/history")
def get_telemetry_history(limit: int = 30, device_id: Optional[str] = None):
    """
    Retorna las últimas N lecturas para graficar series de tiempo.
    """
    if device_id:
        filtrados = [d for d in telemetry_db if d["device_id"] == device_id]
        return {"status": "success", "data": filtrados[-limit:]}
    return {"status": "success", "data": telemetry_db[-limit:]}

# ---------------------------------------------------------------------
# ENDPOINTS DE COMANDOS (DASHBOARD ➔ SERVIDOR ➔ ESP32)
# ---------------------------------------------------------------------
@app.post("/api/commands", status_code=201)
def send_command_to_device(cmd: CommandPayload):
    """
    El Dashboard en Streamlit envía un comando hacia la cola de la ESP32.
    """
    data = cmd.model_dump()
    data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if cmd.device_id not in pending_commands:
        pending_commands[cmd.device_id] = []
    
    pending_commands[cmd.device_id].append(data)
    return {"status": "queued", "command": data}

@app.get("/api/commands/{device_id}")
def poll_pending_commands(device_id: str):
    """
    La ESP32 consulta periódicamente este endpoint para saber si hay órdenes pendientes.
    Una vez leídos, los comandos se retiran de la cola.
    """
    cmds = pending_commands.get(device_id, [])
    pending_commands[device_id] = []  # Vaciar cola
    return {"status": "success", "device_id": device_id, "commands": cmds}
