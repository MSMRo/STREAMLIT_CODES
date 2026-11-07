# Tutorial 06: Visualización de Datos y Tablas Interactivas

En este módulo aprenderás a transformar datos crudos en interfaces de usuario analíticas, tablas configurables y gráficos interactivos de alta calidad.

---

## 🎯 Objetivos de Aprendizaje
- **Tablas Avanzadas**:
  - `st.dataframe`: formatear columnas con números decimales, porcentajes, barras de progreso visuales y casillas booleanas.
  - `st.data_editor`: permitir al usuario editar, añadir y eliminar filas directamente en el navegador, obteniendo el DataFrame resultante en Python.
- **Gráficos Nativos**:
  - Crear gráficos rápidos de líneas y barras con `st.line_chart` y `st.bar_chart`.
- **Plotly Express & Graph Objects**:
  - Construir diagramas de dispersión interactivos con codificación de color, tamaño y leyendas dinámicas.
  - Renderizar superficies tridimensionales (3D Surface) con zoom y rotación libre en el navegador.

---

## 📊 Comparativa de Opciones de Visualización

| Herramienta | Ventajas | Casos de Uso Recomendados |
| :--- | :--- | :--- |
| **Gráficos Nativos** (`st.line_chart`, etc.) | Configuración cero, ultrarrápidos, limpios. | Gráficas rápidas de series de tiempo o prototipos inmediatos. |
| **Plotly** (`st.plotly_chart`) | Zoom interactivo, tooltips (hover), 3D, múltiples ejes. | Dashboards analíticos, publicaciones científicas, monitoreo industrial. |
| **Matplotlib / Seaborn** (`st.pyplot`) | Control pixel por pixel, estándar académico. | Gráficos estáticos para reportes imprimibles en PDF o papers. |

---

## 🚀 Cómo Ejecutar

```bash
uv run streamlit run 06_visualizacion_y_datos/app.py
```
