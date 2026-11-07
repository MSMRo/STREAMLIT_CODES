# Tutorial 05: Multimedia y Manejo de Archivos

Este módulo enseña cómo integrar medios audiovisuales y trabajar con flujos de archivos tanto de entrada (subidas) como de salida (descargas).

---

## 🎯 Objetivos de Aprendizaje
- **Imágenes**:
  - Renderizar imágenes desde arreglos de NumPy, objetos PIL `Image` o URLs web.
  - Aplicar transformaciones y filtros en tiempo real (brillo, contraste, blanco y negro, detección de bordes).
- **Audio**:
  - Reproducir pistas de audio remotas o locales.
  - Sintetizar tonos senoidales puros en formato PCM de 16 bits usando solo NumPy.
- **Video**:
  - Incrustar videos locales (.mp4) y reproductores de YouTube o Vimeo mediante `st.video`.
- **Cámara Web**:
  - Capturar fotografías instantáneas del usuario en el navegador mediante `st.camera_input`.
- **Gestión de Archivos**:
  - Cargar archivos en memoria con `st.file_uploader` sin guardar en disco si no es necesario.
  - Generar buffers binarios (`io.BytesIO`) y exportar archivos CSV, imágenes o texto con `st.download_button`.

---

## 🛠️ Flujo de Procesamiento en Memoria

Para evitar ensuciar el disco duro con archivos temporales, Streamlit procesa las subidas y descargas como flujos en memoria:

```
[Usuario sube imagen] ──> [UploadedFile (BytesIO)] ──> [PIL Image.open()]
                                                            │
                                                     [Filtros NumPy/PIL]
                                                            │
[st.download_button] <── [BytesIO buffer en memoria] <──────┘
```

---

## 🚀 Cómo Ejecutar

```bash
uv run streamlit run 05_multimedia_y_archivos/app.py
```
