# Tutorial 07: Rendimiento y Almacenamiento en Caché

En este tutorial aprenderás a diseñar aplicaciones rápidas y escalables optimizando el cómputo repetitivo mediante el sistema de almacenamiento en caché de Streamlit.

---

## 🎯 Objetivos de Aprendizaje
- Entender el impacto del re-ejecución del script en funciones de alta latencia (APIs, bases de datos, simulaciones).
- Implementar `@st.cache_data` para almacenar resultados reproducibles (DataFrames, consultas SQL, transformaciones).
- Comprender el ciclo de vida y los parámetros de `@st.cache_data`:
  - `ttl`: tiempo de vida del caché en segundos.
  - `show_spinner`: activar/desactivar el indicador de carga.
  - Invalidación explícita con `funcion.clear()` o `st.cache_data.clear()`.
- Implementar `@st.cache_resource` para objetos no serializables compartidos:
  - Clientes de base de datos.
  - Conexiones de puerto Serial con Arduino.
  - Modelos de Inteligencia Artificial (PyTorch, TensorFlow, Hugging Face).

---

## ⚡ Regla de Oro: `@st.cache_data` vs `@st.cache_resource`

| Decorador | ¿Qué guarda? | ¿Copia el valor? | Ejemplos de uso |
| :--- | :--- | :--- | :--- |
| **`@st.cache_data`** | Datos serializables (números, DataFrames, dicts, arrays) | **Sí**, devuelve una copia nueva para evitar mutaciones accidentales entre usuarios | Descarga de CSV, llamadas a APIs REST, consultas SQL, preprocesamiento de imágenes |
| **`@st.cache_resource`** | Objetos de recursos globales no serializables | **No**, devuelve exactamente la misma referencia en memoria compartida | Conexiones `serial.Serial` con Arduino, sesiones `requests.Session`, modelos de Deep Learning, pools de bases de datos |

---

## 🚀 Cómo Ejecutar

```bash
uv run streamlit run 07_rendimiento_y_cache/app.py
```
