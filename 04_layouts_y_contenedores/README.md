# Tutorial 04: Layouts, Contenedores y Estructura Visual

En este tutorial aprenderás a organizar espacialmente los elementos de tu aplicación para obtener una experiencia de usuario limpia, profesional e intuitiva.

---

## 🎯 Objetivos de Aprendizaje
- Configurar el título de pestaña, icono y modo ancho (*wide mode*) con `st.set_page_config`.
- Utilizar la barra lateral (`st.sidebar`) para parámetros globales, navegación y filtros.
- Crear cuadrículas y columnas con anchos proporcionales (`st.columns([2, 1, 1])`).
- Organizar contenido extenso en pestañas limpias (`st.tabs`).
- Añadir secciones colapsables (`st.expander`) para no abrumar al usuario con texto secundario.
- Encapsular tarjetas visuales con bordes redondeados usando `st.container(border=True)`.
- Crear marcadores de posición dinámicos con `st.empty()` para actualizaciones en vivo.
- Implementar diálogos modales flotantes con el decorador `@st.dialog`.

---

## 📌 Guía Rápida de Componentes de Layout

| Componente | Uso Principal |
| :--- | :--- |
| `st.set_page_config` | **Debe ser la 1ª instrucción**. Configura título de ventana, favicon, `layout="wide"` o `"centered"`. |
| `st.sidebar` | Panel lateral retráctil ideal para configuraciones, filtros y controles de sesión. |
| `st.columns(n)` | Distribución horizontal en $n$ columnas. Puede recibir listas de pesos relativos como `[3, 1]`. |
| `st.tabs([...])` | Pestañas superiores para dividir vistas complejas sin cambiar de página. |
| `st.expander("título")` | Acordeón plegable para documentación, FAQs o configuraciones secundarias. |
| `st.empty()` | Reserva un slot en la pantalla para sobreescribir su contenido en bucles o progreso. |
| `@st.dialog("título")` | Abre una ventana modal superpuesta para confirmaciones o formularios críticos. |

---

## 🚀 Cómo Ejecutar

```bash
uv run streamlit run 04_layouts_y_contenedores/app.py
```
