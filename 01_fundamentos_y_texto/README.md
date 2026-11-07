# Tutorial 01: Fundamentos y Visualización de Texto

Este tutorial cubre los conceptos básicos de presentación visual y el modelo de ejecución reactivo de Streamlit.

---

## 🎯 Objetivos de Aprendizaje
- Comprender el flujo de ejecución de arriba hacia abajo (*top-to-bottom*) de Streamlit.
- Configurar el título y encabezados de página.
- Renderizar texto enriquecido usando Markdown estándar y colores nativos.
- Presentar estructuras de datos con `st.write`.
- Mostrar código fuente con numeración de líneas y fórmulas matemáticas con KaTeX/LaTeX.
- Construir tarjetas de métricas tipo KPI (`st.metric`) con deltas e indicadores.
- Usar bloques de notificación de estado (`st.success`, `st.info`, `st.warning`, `st.error`).

---

## 🧠 Concepto Clave: El Modelo de Ejecución de Streamlit

A diferencia de frameworks tradicionales donde mantienes bucles de eventos complejos o manejadores de DOM:
1. Streamlit ejecuta el script completo de Python **de arriba a abajo** cada vez que la página carga o un usuario interactúa con un widget.
2. No necesitas crear rutas HTTP, plantillas HTML ni serialización JSON manual.
3. El orden de las llamadas a `st.*` en tu código define directamente el orden visual en el navegador.

---

## 🚀 Cómo Ejecutar Este Tutorial

Desde la raíz del proyecto, ejecuta con `uv`:

```bash
uv run streamlit run 01_fundamentos_y_texto/app.py
```

Tu navegador abrirá automáticamente `http://localhost:8501`.
