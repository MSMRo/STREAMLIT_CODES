# Tutorial 03: Manejo de Estado con `st.session_state` y Callbacks

Este tutorial aborda uno de los conceptos más importantes y comúnmente incomprendidos en Streamlit: la persistencia del estado entre recargas de página.

---

## 🎯 Objetivos de Aprendizaje
- Comprender por qué las variables locales normales de Python se reinician en cada interacción del usuario.
- Inicializar de forma segura claves en `st.session_state` usando el patrón `if "clave" not in st.session_state:`.
- Usar callbacks (`on_click`, `on_change`) para actualizar datos antes de que se dibuje la interfaz.
- Implementar interfaces dinámicas con estado:
  - Contador interactivo (sumar, restar, resetear).
  - Conversor bidireccional reactivo (°C a °F).
  - Gestor de tareas pendientes (ToDo List con agregar, marcar y eliminar).
  - Asistente de múltiples pasos (Wizard de registro).

---

## 🔄 El Ciclo de Vida de una Interacción

```
[Usuario hace clic en un botón / cambia un valor]
                     │
                     ▼
  [1. Se disparan los callbacks (on_click / on_change)]
                     │
                     ▼
  [2. st.session_state retiene sus valores actualizados]
                     │
                     ▼
  [3. Streamlit re-ejecuta el script desde la línea 1]
                     │
                     ▼
  [4. Se renderiza la nueva interfaz de usuario]
```

---

## 💡 Buenas Prácticas

1. **Siempre inicializa al principio**: Revisa si la clave existe antes de leerla para evitar errores de tipo `AttributeError` o `KeyError`.
2. **Usa `st.rerun()` cuando modifiques listas o estados profundos**: Te asegura que la interfaz refleje inmediatamente los cambios de longitud o eliminación de elementos.
3. **No uses `st.session_state` para caches pesados**: Para datos grandes que no cambian por usuario (como modelos o DataFrames de 100MB), usa `@st.cache_data` o `@st.cache_resource` (Tutorial 07).

---

## 🚀 Cómo Ejecutar

```bash
uv run streamlit run 03_estado_y_sesion_state/app.py
```
