# Tutorial 02: Widgets, Entradas de Usuario y Formularios

En este tutorial exploramos cómo recibir entradas interactivas del usuario y cómo optimizar la experiencia evitando re-ejecuciones innecesarias usando `st.form`.

---

## 🎯 Objetivos de Aprendizaje
- Dominar los widgets fundamentales:
  - Botones (`st.button`) y casillas (`st.checkbox`).
  - Opciones únicas (`st.radio`, `st.selectbox`).
  - Opciones múltiples (`st.multiselect`).
  - Deslizadores numéricos simples y de intervalo (`st.slider`, `st.select_slider`).
  - Entradas de texto estándar y contraseñas ocultas (`st.text_input`, `st.text_area`).
  - Números, fechas, horas y selector de color (`st.number_input`, `st.date_input`, `st.time_input`, `st.color_picker`).
- Entender el ciclo de vida de los widgets: por qué devuelven su valor actual en cada ejecución.
- Usar `st.form` y `st.form_submit_button` para agrupar múltiples campos y retrasar la ejecución hasta que el usuario termine de rellenar el formulario.

---

## 💡 Cuándo usar `st.form` vs Widgets Directos

| Tipo de Interacción | Recomendación | Motivo |
| :--- | :--- | :--- |
| **Filtro dinámico de una gráfica** | Widget directo (`st.slider`, `st.selectbox`) | El usuario espera ver el gráfico cambiar de inmediato al deslizar o seleccionar. |
| **Formulario con muchos campos** (ej. registro, login, configuración) | `st.form` | Evita re-ejecutar el script 10 veces mientras el usuario llena 10 campos secuencialmente. |
| **Acciones pesadas o destructivas** | `st.form` con botón primario | Da control explícito de confirmación antes de disparar el procesamiento. |

---

## 🚀 Cómo Ejecutar

```bash
uv run streamlit run 02_widgets_e_inputs/app.py
```
