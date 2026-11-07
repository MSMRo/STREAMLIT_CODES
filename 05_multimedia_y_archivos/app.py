"""
Tutorial 05: Multimedia y Manejo de Archivos en Streamlit
=========================================================
Aprende a trabajar con imágenes (locales, URLs, PIL, filtros en vivo),
reproducción de video y audio, captura con cámara web (st.camera_input),
subida de archivos (st.file_uploader) y descarga de resultados (st.download_button).
"""

import io
import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter
import streamlit as st

st.set_page_config(
    page_title="Tutorial 05 - Multimedia y Archivos",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Tutorial 05: Multimedia y Manejo de Archivos")
st.write(
    "Streamlit facilita la integración de medios audiovisuales y la manipulación de archivos en memoria. "
    "En esta aplicación exploraremos procesamiento de imágenes en vivo, audio sintetizado, video, captura de cámara y carga/descarga de datos."
)

st.divider()

# ==========================================
# 1. IMÁGENES Y FILTROS EN TIEMPO REAL
# ==========================================
st.header("1. Visualización y Procesamiento de Imágenes")

tab_img_sample, tab_img_upload = st.tabs(["🖼️ Imagen de Muestra con Filtros", "📤 Sube tu Propia Imagen"])

def aplicar_filtros(imagen: Image.Image, brillo: float, contraste: float, escala_grises: bool, filtro_borde: bool) -> Image.Image:
    img = imagen.copy()
    if escala_grises:
        img = img.convert("L")
    else:
        img = img.convert("RGB")
    
    # Ajuste de brillo
    enhancer_b = ImageEnhance.Brightness(img)
    img = enhancer_b.enhance(brillo)
    
    # Ajuste de contraste
    enhancer_c = ImageEnhance.Contrast(img)
    img = enhancer_c.enhance(contraste)
    
    if filtro_borde:
        img = img.filter(ImageFilter.FIND_EDGES)
        
    return img

with tab_img_sample:
    # Generamos una imagen sintética colorida con NumPy para no depender de archivos externos
    x = np.linspace(-3, 3, 300)
    y = np.linspace(-3, 3, 300)
    xx, yy = np.meshgrid(x, y)
    zz = np.sin(xx**2 + yy**2)
    # Normalizar a 0-255 en 3 canales
    img_array = np.uint8((zz - zz.min()) / (zz.max() - zz.min()) * 255)
    img_sample = Image.fromarray(np.stack([img_array, np.roll(img_array, 50, axis=0), 255 - img_array], axis=2))

    col_ctrl, col_orig, col_proc = st.columns([1, 1, 1])
    
    with col_ctrl:
        st.subheader("Controles de Procesamiento")
        brillo = st.slider("Brillo:", 0.2, 2.5, 1.0, 0.1, key="b_sample")
        contraste = st.slider("Contraste:", 0.2, 2.5, 1.0, 0.1, key="c_sample")
        grises = st.checkbox("Convertir a Blanco y Negro", value=False, key="g_sample")
        bordes = st.checkbox("Detección de Bordes (Sobel/Laplace)", value=False, key="e_sample")
    
    with col_orig:
        st.subheader("Original")
        st.image(img_sample, caption="Patrón Sintético (300x300)", use_container_width=True)
    
    with col_proc:
        st.subheader("Procesada")
        img_resultado = aplicar_filtros(img_sample, brillo, contraste, grises, bordes)
        st.image(img_resultado, caption="Imagen con filtros aplicados", use_container_width=True)

with tab_img_upload:
    archivo_subido = st.file_uploader(
        "Arrastra o selecciona una imagen (.png, .jpg, .jpeg, .webp):",
        type=["png", "jpg", "jpeg", "webp"],
        key="uploader_img"
    )
    if archivo_subido is not None:
        img_usuario = Image.open(archivo_subido)
        col_u1, col_u2, col_u3 = st.columns([1, 1, 1])
        with col_u1:
            st.subheader("Filtros")
            b_u = st.slider("Brillo:", 0.2, 2.5, 1.0, 0.1, key="b_user")
            c_u = st.slider("Contraste:", 0.2, 2.5, 1.0, 0.1, key="c_user")
            g_u = st.checkbox("Blanco y Negro", value=False, key="g_user")
            e_u = st.checkbox("Detección de Bordes", value=False, key="e_user")
        with col_u2:
            st.subheader("Imagen Original")
            st.image(img_usuario, caption=archivo_subido.name, use_container_width=True)
        with col_u3:
            st.subheader("Imagen Final")
            img_usuario_proc = aplicar_filtros(img_usuario, b_u, c_u, g_u, e_u)
            st.image(img_usuario_proc, caption="Resultado", use_container_width=True)
            
            # Botón de Descarga de la imagen procesada en formato PNG
            buffer_img = io.BytesIO()
            img_usuario_proc.save(buffer_img, format="PNG")
            st.download_button(
                label="📥 Descargar Imagen Procesada (PNG)",
                data=buffer_img.getvalue(),
                file_name=f"procesada_{archivo_subido.name}.png",
                mime="image/png"
            )
    else:
        st.info("Sube una imagen para probar los filtros y descargar el resultado.")

st.divider()

# ==========================================
# 2. AUDIO Y SÍNTESIS DE SEÑAL
# ==========================================
st.header("2. Reproducción y Generación de Audio (`st.audio`)")
st.write(
    "Además de reproducir archivos WAV o MP3 existentes, puedes generar ondas sonoras matemáticamente en Python:"
)

col_aud1, col_aud2 = st.columns(2)
with col_aud1:
    st.subheader("Sintetizador de Tono Senoidal Puro")
    frecuencia_hz = st.slider("Frecuencia del tono (Hz):", min_value=100, max_value=2000, value=440, step=10, help="440 Hz = Nota La (A4)")
    duracion_seg = st.slider("Duración (segundos):", 1.0, 5.0, 2.0, 0.5)
    
    # Generar audio PCM usando NumPy
    sample_rate = 44100
    t = np.linspace(0, duracion_seg, int(sample_rate * duracion_seg), False)
    tono = np.sin(frecuencia_hz * t * 2 * np.pi)
    # Suavizado de entrada y salida (fade-in / fade-out)
    ventana = np.hamming(len(tono))
    tono_suave = tono * ventana
    # Normalizar a 16-bit PCM
    audio_pcm = np.int16(tono_suave * 32767)
    
    st.audio(audio_pcm, sample_rate=sample_rate)

with col_aud2:
    st.subheader("Audio Remoto por URL")
    st.write("Reproduce podcasts o muestras de sonido desde la web:")
    url_audio = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    st.audio(url_audio)
    st.caption("Muestra libre de regalías de SoundHelix.")

st.divider()

# ==========================================
# 3. REPRODUCCIÓN DE VIDEO (st.video)
# ==========================================
st.header("3. Reproducción de Video (`st.video`)")
st.write("Soporta archivos MP4 locales, enlaces directos a videos y URLs de YouTube o Vimeo.")

col_v1, col_v2 = st.columns([2, 1])
with col_v1:
    url_video = st.text_input(
        "Enlace de Video (YouTube o MP4 directo):",
        value="https://www.youtube.com/watch?v=B2iAODr0fOo"
    )
    if url_video:
        try:
            st.video(url_video)
        except Exception as e:
            st.error(f"Error al cargar video: {e}")

with col_v2:
    st.subheader("Formatos Soportados")
    st.markdown("""
    - **YouTube:** URLs completas o acortadas (`youtu.be`).
    - **Vimeo:** Enlaces directos a videos.
    - **Archivos locales:** `.mp4`, `.webm`, `.ogg`.
    - **Objetos en memoria:** `bytes` o `BytesIO`.
    - **Subtítulos:** Puedes añadir pistas WebVTT mediante el parámetro `subtitles`.
    """)

st.divider()

# ==========================================
# 4. CAPTURA CON CÁMARA WEB (st.camera_input)
# ==========================================
st.header("4. Captura en Vivo con Cámara Web (`st.camera_input`)")
st.write("Permite tomar fotografías directamente desde la cámara del dispositivo del usuario (requiere permiso en el navegador).")

foto = st.camera_input("Haz clic para tomar una fotografía de prueba")
if foto is not None:
    img_foto = Image.open(foto)
    st.success("¡Foto capturada exitosamente!")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.image(img_foto, caption="Foto Capturada", use_container_width=True)
    with col_f2:
        # Convertir a negativo
        img_invertida = Image.fromarray(255 - np.array(img_foto.convert("RGB")))
        st.image(img_invertida, caption="Efecto Negativo Invertido", use_container_width=True)

st.divider()

# ==========================================
# 5. SUBIDA Y DESCARGA DE DATOS (CSV, TXT)
# ==========================================
st.header("5. Subida y Descarga de Archivos de Datos")

col_d1, col_d2 = st.columns(2)

with col_d1:
    st.subheader("Subir y Explorar Archivo CSV")
    csv_file = st.file_uploader("Selecciona un archivo CSV:", type=["csv"], key="csv_uploader")
    if csv_file is not None:
        df_subido = pd.read_csv(csv_file)
        st.write("Vista previa de los primeros 5 registros:")
        st.dataframe(df_subido.head(), use_container_width=True)
        st.write(f"Dimensiones: **{df_subido.shape[0]} filas × {df_subido.shape[1]} columnas**")
    else:
        st.caption("Puedes descargar el archivo de ejemplo de la derecha y subirlo aquí.")

with col_d2:
    st.subheader("Generar y Descargar Reporte CSV")
    # Generamos un DataFrame de ejemplo
    df_ejemplo = pd.DataFrame({
        "Sensor_ID": [f"SENS_{i:03d}" for i in range(1, 11)],
        "Temperatura_C": np.round(np.random.uniform(20.0, 35.0, 10), 1),
        "Humedad_Pct": np.round(np.random.uniform(40.0, 85.0, 10), 1),
        "Estado": ["OK", "OK", "ALERTA", "OK", "OK", "OK", "OK", "ALERTA", "OK", "OK"]
    })
    st.dataframe(df_ejemplo.head(5), use_container_width=True)
    
    csv_data = df_ejemplo.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Descargar Dataset de Sensores (CSV)",
        data=csv_data,
        file_name="telemetria_sensores.csv",
        mime="text/csv",
        type="primary"
    )

st.divider()
st.info("💡 Ejecuta este tutorial con: `uv run streamlit run 05_multimedia_y_archivos/app.py`")
