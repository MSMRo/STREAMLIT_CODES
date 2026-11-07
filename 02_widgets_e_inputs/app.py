"""
Tutorial 02: Widgets, Entradas de Usuario y Formularios en Streamlit
===================================================================
Aprende a capturar interacciones del usuario con botones, selectores,
deslizadores, entradas de texto, fechas, colores y agrupación con st.form.
"""

from datetime import date, time
import streamlit as st

st.set_page_config(
    page_title="Tutorial 02 - Widgets e Inputs",
    page_icon="🎛️",
    layout="wide"
)

st.title("🎛️ Tutorial 02: Widgets, Entradas y Formularios")
st.write(
    "Los widgets son los componentes que permiten al usuario interactuar con tu aplicación. "
    "Cada vez que un usuario interactúa con un widget, Streamlit vuelve a ejecutar el script "
    "con el nuevo valor asignado a la variable."
)

st.divider()

# Sección 1: Botones y Opciones Booleanas
st.header("1. Botones y Casillas de Verificación")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Botón de Acción (`st.button`)")
    st.write("Un botón devuelve `True` únicamente en la ejecución en que fue presionado.")
    if st.button("¡Presióname!", type="primary"):
        st.balloons()
        st.success("¡Hiciste clic en el botón primario!")
    else:
        st.info("El botón está en reposo.")

with col2:
    st.subheader("Casilla de Selección (`st.checkbox`)")
    mostrar_detalles = st.checkbox("Mostrar opciones avanzadas", value=False)
    if mostrar_detalles:
        st.warning("⚠️ Opciones avanzadas activadas: ten cuidado con los cambios.")
    else:
        st.caption("Marca la casilla para ver más detalles.")

st.divider()

# Sección 2: Selectores y Listas
st.header("2. Selectores y Opciones")
col_sel1, col_sel2, col_sel3 = st.columns(3)

with col_sel1:
    lenguaje = st.radio(
        "Lenguaje favorito:",
        options=["Python", "C++ (Arduino)", "Rust", "JavaScript"],
        index=0,
        help="Selecciona una única opción entre las disponibles"
    )
    st.write(f"Seleccionaste: **{lenguaje}**")

with col_sel2:
    nivel = st.selectbox(
        "Nivel de experiencia con Streamlit:",
        options=["Principiante", "Intermedio", "Avanzado", "Experto"],
        index=0
    )
    st.write(f"Nivel elegido: **{nivel}**")

with col_sel3:
    modulos = st.multiselect(
        "Temas que te interesan aprender:",
        options=["Widgets", "Multimedia", "Serial / Arduino", "Visualización", "APIs"],
        default=["Widgets", "Serial / Arduino"]
    )
    st.write(f"Seleccionados ({len(modulos)}): {', '.join(modulos)}")

st.divider()

# Sección 3: Deslizadores Numéricos y Rangos
st.header("3. Deslizadores (`st.slider` y `st.select_slider`)")
col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    volumen = st.slider("Nivel de Volumen (0 a 100):", min_value=0, max_value=100, value=70, step=5)
    st.write(f"Volumen: **{volumen}%**")

with col_s2:
    rango_edad = st.slider(
        "Rango de Edades objetivo:",
        min_value=18,
        max_value=80,
        value=(25, 45),
        help="Arrastra ambos extremos para seleccionar un intervalo"
    )
    st.write(f"Rango seleccionado: **{rango_edad[0]} - {rango_edad[1]} años**")

with col_s3:
    talla = st.select_slider(
        "Talla de camiseta:",
        options=["XS", "S", "M", "L", "XL", "XXL"],
        value="L"
    )
    st.write(f"Talla: **{talla}**")

st.divider()

# Sección 4: Entradas de Texto, Números, Fechas y Color
st.header("4. Entradas de Texto, Números, Fechas y Color")
col_in1, col_in2, col_in3 = st.columns(3)

with col_in1:
    nombre = st.text_input("Nombre de usuario:", placeholder="Ej: dev_python")
    password = st.text_input("Contraseña:", type="password", placeholder="••••••••")
    st.write(f"Usuario ingresado: `{nombre or '(vacío)'}`")

with col_in2:
    edad = st.number_input("Edad:", min_value=1, max_value=120, value=25, step=1)
    fecha_nac = st.date_input("Fecha de nacimiento:", value=date(2000, 1, 1))
    st.write(f"Edad: **{edad}**, Fecha: **{fecha_nac}**")

with col_in3:
    hora_alarma = st.time_input("Hora de alarma:", value=time(8, 30))
    color_favorito = st.color_picker("Elige un color para el tema:", value="#00A65A")
    st.write(f"Hora: **{hora_alarma}**")
    st.markdown(
        f'<div style="background-color:{color_favorito}; padding:10px; border-radius:8px; color:white; text-align:center;">'
        f'Color hexadecimal: {color_favorito}</div>',
        unsafe_allow_html=True
    )

st.divider()

# Sección 5: Formularios (st.form) - Agrupación de Entradas
st.header("5. Agrupación y Envío por Lotes con Formularios (`st.form`)")
st.markdown("""
> **¿Por qué usar formularios?**  
> Normalmente, cada vez que un usuario escribe una letra o mueve un slider, Streamlit recarga la página.
> Con `st.form`, los valores solo se envían al hacer clic en el botón `st.form_submit_button`.
""")

with st.form("formulario_registro"):
    st.subheader("Formulario de Registro de Dispositivo IoT")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        dev_id = st.text_input("ID del Dispositivo:", value="ESP32_NODE_01")
        dev_tipo = st.selectbox("Tipo de Placa:", ["Arduino Uno", "Arduino Nano", "ESP32", "Raspberry Pi Pico"])
    with col_f2:
        dev_baud = st.selectbox("Velocidad de Baudios:", [9600, 19200, 38400, 57600, 115200], index=0)
        dev_auto_reconnect = st.checkbox("Reconexión automática", value=True)
    
    dev_desc = st.text_area("Descripción de la estación de trabajo:", placeholder="Ubicado en el laboratorio...")
    
    # Botón obligatorio de envío del formulario
    enviado = st.form_submit_button("Guardar Configuración", type="primary")

if enviado:
    st.success("✅ ¡Datos del formulario recibidos correctamente!")
    st.json({
        "device_id": dev_id,
        "board_type": dev_tipo,
        "baud_rate": dev_baud,
        "auto_reconnect": dev_auto_reconnect,
        "description": dev_desc
    })

st.divider()
st.info("💡 Ejecuta este tutorial con: `uv run streamlit run 02_widgets_e_inputs/app.py`")
