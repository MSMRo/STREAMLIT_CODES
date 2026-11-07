"""
Tutorial 03: Manejo de Estado con st.session_state y Callbacks
=============================================================
Aprende a mantener variables en memoria entre ejecuciones, usar callbacks
(on_click, on_change) y construir aplicaciones con estado como contadores,
listas de tareas dinámicas y asistentes paso a paso (wizards).
"""

import streamlit as st

st.set_page_config(
    page_title="Tutorial 03 - Session State y Callbacks",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Tutorial 03: Manejo de Estado (`st.session_state`)")
st.write(
    "Debido a que Streamlit re-ejecuta todo el código en cada clic, cualquier variable normal de Python "
    "se reinicia a su valor inicial. `st.session_state` es un diccionario persistente que vive "
    "durante toda la sesión del usuario en el navegador."
)

st.divider()

# ==========================================
# 1. EL PROBLEMA vs LA SOLUCIÓN: CONTADOR
# ==========================================
st.header("1. El Problema de las Variables Locales vs `st.session_state`")

col_bad, col_good = st.columns(2)

with col_bad:
    st.subheader("❌ Variable Normal (Sin Estado)")
    st.caption("Esta variable se reinicia a 0 cada vez que se presiona el botón.")
    
    variable_normal = 0
    if st.button("Sumar a variable local", key="btn_local"):
        variable_normal += 1
    st.write(f"Valor de `variable_normal`: **{variable_normal}** (¡Nunca pasa de 1!)")

with col_good:
    st.subheader("✅ Con `st.session_state` (Persistente)")
    st.caption("El valor se preserva entre ejecuciones.")
    
    # Patrón seguro de inicialización
    if "contador_persistente" not in st.session_state:
        st.session_state.contador_persistente = 0

    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button("➕ Sumar 1", key="btn_add"):
            st.session_state.contador_persistente += 1
    with col_btn2:
        if st.button("➖ Restar 1", key="btn_sub"):
            st.session_state.contador_persistente -= 1
    with col_btn3:
        if st.button("🔄 Reiniciar", key="btn_reset"):
            st.session_state.contador_persistente = 0

    st.write(f"Valor en `st.session_state.contador_persistente`: **{st.session_state.contador_persistente}**")

st.divider()

# ==========================================
# 2. CALLBACKS (on_click y on_change)
# ==========================================
st.header("2. Callbacks con `on_click` y `on_change`")
st.write(
    "Un callback es una función de Python que se ejecuta **antes** de que el resto del script "
    "vuelva a correr, asegurando que el estado esté actualizado antes de renderizar la pantalla."
)

if "temperatura_celsius" not in st.session_state:
    st.session_state.temperatura_celsius = 25.0
if "temperatura_fahrenheit" not in st.session_state:
    st.session_state.temperatura_fahrenheit = 77.0

def celsius_a_fahrenheit():
    st.session_state.temperatura_fahrenheit = round(
        (st.session_state.celsius_input * 9 / 5) + 32, 2
    )

def fahrenheit_a_celsius():
    st.session_state.temperatura_celsius = round(
        (st.session_state.fahrenheit_input - 32) * 5 / 9, 2
    )

col_temp1, col_temp2 = st.columns(2)
with col_temp1:
    st.number_input(
        "Grados Celsius (°C):",
        value=st.session_state.temperatura_celsius,
        key="celsius_input",
        on_change=celsius_a_fahrenheit
    )
with col_temp2:
    st.number_input(
        "Grados Fahrenheit (°F):",
        value=st.session_state.temperatura_fahrenheit,
        key="fahrenheit_input",
        on_change=fahrenheit_a_celsius
    )

st.caption("Cambia cualquiera de las dos cajas y verás cómo la otra se actualiza inmediatamente vía callback.")

st.divider()

# ==========================================
# 3. EJEMPLO PRÁCTICO: LISTA DE TAREAS (TODO LIST)
# ==========================================
st.header("3. Caso Práctico: Lista de Tareas Dinámica")

if "tareas" not in st.session_state:
    st.session_state.tareas = [
        {"texto": "Instalar UV y Streamlit", "completada": True},
        {"texto": "Aprender widgets e inputs", "completada": True},
        {"texto": "Conectar Arduino por puerto Serial", "completada": False},
    ]

# Función para agregar tarea
def agregar_tarea():
    nueva = st.session_state.input_nueva_tarea.strip()
    if nueva:
        st.session_state.tareas.append({"texto": nueva, "completada": False})
        st.session_state.input_nueva_tarea = ""

# Formulario simple para nueva tarea
col_t1, col_t2 = st.columns([4, 1])
with col_t1:
    st.text_input("Escribe una nueva tarea:", key="input_nueva_tarea", placeholder="Ej: Crear gráfico interactivo...")
with col_t2:
    st.button("Agregar Tarea", on_click=agregar_tarea, use_container_width=True)

# Listado de tareas
st.write("### Tus Tareas Actuales:")
for idx, tarea in enumerate(st.session_state.tareas):
    col_check, col_del = st.columns([8, 2])
    with col_check:
        completada = st.checkbox(
            tarea["texto"],
            value=tarea["completada"],
            key=f"tarea_{idx}"
        )
        st.session_state.tareas[idx]["completada"] = completada
    with col_del:
        if st.button("🗑️ Eliminar", key=f"del_{idx}"):
            st.session_state.tareas.pop(idx)
            st.rerun()

st.divider()

# ==========================================
# 4. ASISTENTE PASO A PASO (WIZARD)
# ==========================================
st.header("4. Asistente Paso a Paso (Multi-step Wizard)")

if "paso_wizard" not in st.session_state:
    st.session_state.paso_wizard = 1
if "datos_wizard" not in st.session_state:
    st.session_state.datos_wizard = {}

# Barra de progreso visual
progreso = (st.session_state.paso_wizard - 1) / 2
st.progress(progreso, text=f"Paso {st.session_state.paso_wizard} de 3")

if st.session_state.paso_wizard == 1:
    st.subheader("Paso 1: Información Personal")
    nombre_w = st.text_input("Nombre completo:", value=st.session_state.datos_wizard.get("nombre", ""))
    email_w = st.text_input("Correo electrónico:", value=st.session_state.datos_wizard.get("email", ""))
    
    if st.button("Siguiente ➡️", key="w_siguiente_1"):
        if nombre_w and email_w:
            st.session_state.datos_wizard["nombre"] = nombre_w
            st.session_state.datos_wizard["email"] = email_w
            st.session_state.paso_wizard = 2
            st.rerun()
        else:
            st.error("Por favor completa todos los campos requeridos.")

elif st.session_state.paso_wizard == 2:
    st.subheader("Paso 2: Preferencias Técnicas")
    hardware_w = st.multiselect(
        "¿Qué hardware utilizas?",
        options=["Arduino Uno", "ESP32", "Raspberry Pi", "Sensores I2C", "Motores Paso a Paso"],
        default=st.session_state.datos_wizard.get("hardware", [])
    )
    
    col_w_prev, col_w_next = st.columns(2)
    with col_w_prev:
        if st.button("⬅️ Anterior", key="w_ant_2"):
            st.session_state.paso_wizard = 1
            st.rerun()
    with col_w_next:
        if st.button("Siguiente ➡️", key="w_siguiente_2"):
            st.session_state.datos_wizard["hardware"] = hardware_w
            st.session_state.paso_wizard = 3
            st.rerun()

elif st.session_state.paso_wizard == 3:
    st.subheader("Paso 3: Confirmación y Resumen")
    st.json(st.session_state.datos_wizard)
    
    col_w_prev3, col_w_finish = st.columns(2)
    with col_w_prev3:
        if st.button("⬅️ Anterior", key="w_ant_3"):
            st.session_state.paso_wizard = 2
            st.rerun()
    with col_w_finish:
        if st.button("🎉 Finalizar Registro", type="primary", key="w_finish"):
            st.success("¡Registro completado exitosamente!")
            # Reiniciar wizard
            st.session_state.paso_wizard = 1
            st.session_state.datos_wizard = {}

st.divider()
st.info("💡 Ejecuta este tutorial con: `uv run streamlit run 03_estado_y_sesion_state/app.py`")
