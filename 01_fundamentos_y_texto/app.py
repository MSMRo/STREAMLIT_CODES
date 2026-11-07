"""
Tutorial 01: Fundamentos y Visualización de Texto en Streamlit
==============================================================
En este módulo aprenderás cómo Streamlit renderiza contenido en pantalla,
la sintaxis para títulos, texto enriquecido con Markdown, fórmulas LaTeX,
bloques de código, métricas numéricas y llamadas de estado.
"""

import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="Tutorial 01 - Fundamentos y Texto",
    page_icon="📝",
    layout="centered"
)

# 1. Títulos y Encabezados
st.title("📝 Tutorial 01: Fundamentos y Texto")
st.write(
    "¡Bienvenido a Streamlit! Este framework te permite construir aplicaciones web "
    "interactivas puramente en Python sin necesidad de escribir HTML, CSS o JavaScript."
)

st.divider()

# 2. Jerarquía de Títulos
st.header("1. Jerarquía de Encabezados")
st.write("Streamlit proporciona diferentes niveles para organizar visualmente tu aplicación:")

st.subheader("Este es un Subheader (`st.subheader`)")
st.caption("Esta es una leyenda pequeña (`st.caption`), ideal para notas al pie, fuentes o metadatos.")

# 3. Formato con Markdown y Estilos
st.header("2. Markdown Enriquecido (`st.markdown`)")
st.markdown("""
Puedes escribir Markdown estándar y también usar estilos de color nativos de Streamlit:
- **Texto en negrita** y *texto en cursiva*.
- Listas numeradas y viñetas.
- Texto con color: :blue[azul], :red[rojo], :green[verde], :orange[naranja], :violet[violeta].
- Texto con fondo resaltado: :blue-background[fondo azul], :green-background[fondo verde].
- Enlaces como [Documentación Oficial de Streamlit](https://docs.streamlit.io).
""")

# 4. st.write: La navaja suiza de Streamlit
st.header("3. La función mágica `st.write()`")
st.write(
    "`st.write()` es polimórfica: detecta automáticamente el tipo de dato y lo "
    "renderiza apropiadamente (texto, números, diccionarios, dataframes, gráficos, etc.)."
)

ejemplo_diccionario = {
    "framework": "Streamlit",
    "lenguaje": "Python",
    "gestor_paquetes": "uv",
    "version_estable": True,
    "caracteristicas": ["Rápido", "Reactivo", "Modular"]
}
st.write("Visualizando un diccionario Python directamente con `st.write()`:")
st.write(ejemplo_diccionario)

# 5. Bloques de Código
st.header("4. Bloques de Código con Resaltado de Sintaxis (`st.code`)")
codigo_ejemplo = """def saludar(nombre: str) -> str:
    # Función de saludo simple
    mensaje = f"¡Hola {nombre}, bienvenido al mundo de Streamlit!"
    return mensaje

print(saludar("Desarrollador"))
"""
st.code(codigo_ejemplo, language="python", line_numbers=True)

# 6. Fórmulas Matemáticas con LaTeX
st.header("5. Fórmulas Matemáticas (`st.latex`)")
st.write("Streamlit soporta renderizado de fórmulas matemáticas mediante KaTeX:")
st.latex(r"f(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}")
st.latex(r"E = mc^2 \quad \text{y} \quad \sum_{i=1}^{n} i = \frac{n(n+1)}{2}")

# 7. Métricas y KPIs
st.header("6. Tarjetas de Métricas (`st.metric`)")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Velocidad de Carga", value="120 ms", delta="-15 ms")
with col2:
    st.metric(label="Usuarios Activos", value="1,450", delta="+85")
with col3:
    st.metric(label="Consumo de CPU", value="42%", delta="+5%", delta_color="inverse")

# 8. Mensajes de Estado y Feedback
st.header("7. Mensajes de Estado")
st.success("Operación completada con éxito (`st.success`)")
st.info("Información relevante para el usuario (`st.info`)")
st.warning("Advertencia: Verifica los parámetros antes de continuar (`st.warning`)")
st.error("Error: No se pudo conectar con el servidor remoto (`st.error`)")

st.divider()
st.info("💡 **Consejo:** Para ejecutar este tutorial ejecuta en tu terminal: `uv run streamlit run 01_fundamentos_y_texto/app.py`")
