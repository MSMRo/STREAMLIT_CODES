# 🚀 Masterclass de Streamlit con Python y UV

¡Bienvenido al curso interactivo y práctico de **Streamlit**! Este repositorio contiene una colección completa, modular y progresiva de tutoriales diseñados para aprender Streamlit desde los conceptos más básicos hasta el control de hardware y microcontroladores (**Arduino / ESP32**) mediante comunicación serie (PySerial).

Todo el proyecto está gestionado de forma moderna, reproducible y ultrarrápida utilizando [**uv**](https://docs.astral.sh/uv/), el gestor de paquetes y entornos virtuales de Python de nueva generación.

---

## 📋 Tabla de Contenidos

1. [¿Por qué UV y cómo instalarlo?](#-1-instalación-de-uv-y-configuración-del-entorno)
2. [Instalación de Streamlit y Dependencias](#-2-instalación-de-dependencias-del-proyecto)
3. [Estructura del Proyecto y Catálogo de Módulos](#-3-catálogo-completo-de-tutoriales)
4. [Módulo Especial: Arduino y Comunicación Serie](#-4-módulo-especial-arduino-y-comunicación-serie)
5. [Hub Central Interactivo](#-5-hub-central-interactivo)
6. [Hoja de Trucos (Cheat Sheet) de Streamlit](#-6-hoja-de-trucos-de-streamlit)

---

## ⚡ 1. Instalación de UV y Configuración del Entorno

`uv` es un gestor de paquetes de Python desarrollado en Rust que es entre 10 y 100 veces más rápido que `pip`. Con `uv`, no necesitas crear ni activar entornos virtuales manualmente; `uv run` se encarga de todo automáticamente.

### A. Instalación de UV

#### En Windows (PowerShell):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### En macOS / Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Para verificar que esté instalado correctamente:
```bash
uv --version
```

---

## 📦 2. Instalación de Dependencias del Proyecto

Clona o dirígete a esta carpeta en tu terminal:

```bash
cd e:\PROJECTS\STREAMLIT_CODES
```

Para sincronizar e instalar todas las dependencias (Streamlit, Pandas, NumPy, Pillow, Plotly, PySerial) en el entorno virtual administrado por `uv`:

```bash
uv sync --system-certs
```

> **¿Qué hace `uv sync`?**  
> Lee el archivo `pyproject.toml` y `uv.lock`, crea automáticamente el entorno virtual en `.venv` e instala exactamente las versiones requeridas.

---

## 📚 3. Catálogo Completo de Tutoriales

Cada carpeta contiene su propio script funcional (`app.py`) y un archivo `README.md` explicativo:

| Módulo | Carpeta | Descripción | Comando de Ejecución |
| :---: | :--- | :--- | :--- |
| **01** | [`01_fundamentos_y_texto`](01_fundamentos_y_texto/) | Fundamentos de UI, títulos, Markdown con colores, LaTeX, métricas y mensajes de estado. | `uv run streamlit run 01_fundamentos_y_texto/app.py` |
| **02** | [`02_widgets_e_inputs`](02_widgets_e_inputs/) | Botones, sliders, casillas, selectores, entradas de texto, fechas, colores y agrupación con `st.form`. | `uv run streamlit run 02_widgets_e_inputs/app.py` |
| **03** | [`03_estado_y_sesion_state`](03_estado_y_sesion_state/) | Persistencia con `st.session_state`, callbacks `on_click`/`on_change`, ToDo List y Wizards paso a paso. | `uv run streamlit run 03_estado_y_sesion_state/app.py` |
| **04** | [`04_layouts_y_contenedores`](04_layouts_y_contenedores/) | Barra lateral (`st.sidebar`), cuadrículas con `st.columns`, pestañas (`st.tabs`), acordeones y modales `@st.dialog`. | `uv run streamlit run 04_layouts_y_contenedores/app.py` |
| **05** | [`05_multimedia_y_archivos`](05_multimedia_y_archivos/) | Filtros de imagen en vivo con PIL, síntesis de audio senoidal con NumPy, video, cámara web y carga/descarga de archivos. | `uv run streamlit run 05_multimedia_y_archivos/app.py` |
| **06** | [`06_visualizacion_y_datos`](06_visualizacion_y_datos/) | Tablas interactivas con `st.dataframe`, editor en vivo con `st.data_editor`, gráficos nativos y gráficos 3D interactivos con Plotly. | `uv run streamlit run 06_visualizacion_y_datos/app.py` |
| **07** | [`07_rendimiento_y_cache`](07_rendimiento_y_cache/) | Aceleración drástica con `@st.cache_data` (datos/APIs) y `@st.cache_resource` (conexiones de hardware/modelos). | `uv run streamlit run 07_rendimiento_y_cache/app.py` |
| **08** | [`08_arduino_serial_hardware`](08_arduino_serial_hardware/) | Conexión física con Arduino por puerto serie USB (PySerial), control digital y PWM, telemetría y Modo Simulación. | `uv run streamlit run 08_arduino_serial_hardware/app.py` |
| **09** | [`09_aplicacion_multipagina`](09_aplicacion_multipagina/) | Arquitectura multipágina modular con la convención `pages/` y sesión compartida entre vistas. | `uv run streamlit run 09_aplicacion_multipagina/app.py` |

---

## 🔌 4. Módulo Especial: Arduino y Comunicación Serie

El tutorial `08_arduino_serial_hardware` resuelve el problema más habitual al usar hardware en Streamlit:
- **El Problema:** Cada vez que el usuario hace clic en un botón, Streamlit re-ejecuta el script. Si el puerto serie se abre sin caché, la conexión se resetea y el Arduino se reinicia continuamente debido a la señal DTR.
- **La Solución:** Usar `@st.cache_resource` para mantener la instancia de `serial.Serial` viva en memoria compartida.

### Componentes Incluidos:
1. **Firmware C++ de Arduino:** [`08_arduino_serial_hardware/arduino_code/arduino_firmware.ino`](08_arduino_serial_hardware/arduino_code/arduino_firmware.ino). Cárgalo en tu placa usando Arduino IDE.
2. **Modo Simulación Integrado:** Si no tienes una placa Arduino conectada, el sistema activa automáticamente un generador de señales senoidales realistas y responde a los botones de LED y PWM exactamente igual que un hardware real.

---

## 🎛️ 5. Hub Central Interactivo

Puedes navegar por todo el contenido de este repositorio desde una interfaz gráfica interactiva que incluye catálogo de módulos, estado del sistema y visor de código en tiempo real:

```bash
uv run streamlit run dashboard_hub.py
```

---

## 📌 6. Hoja de Trucos de Streamlit

```python
import streamlit as st

# 1. Configuración (¡Primera línea del script!)
st.set_page_config(page_title="Mi App", page_icon="🚀", layout="wide")

# 2. Texto y Notificaciones
st.title("Título")
st.write("Cualquier objeto Python")
st.success("¡Operación exitosa!")

# 3. Widgets
if st.button("Hacer clic"):
    st.balloons()
valor = st.slider("Selecciona:", 0, 100, 50)

# 4. Estado Persistente
if "contador" not in st.session_state:
    st.session_state.contador = 0
st.session_state.contador += 1

# 5. Caché
@st.cache_data
def cargar_datos():
    return pd.read_csv("datos.csv")

@st.cache_resource
def conectar_hardware():
    return serial.Serial("COM3", 9600)
```
