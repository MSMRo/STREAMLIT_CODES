"""
Subpágina 3: Preferencias y Configuración del Sistema
=====================================================
Modifica variables en st.session_state que afectan a toda la aplicación.
"""

import streamlit as st

st.set_page_config(
    page_title="App Multipágina - Configuración",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Configuración y Preferencias Globales")
st.write("Cualquier cambio guardado aquí persistirá en todas las demás páginas de la aplicación.")

st.divider()

col_cfg1, col_cfg2 = st.columns(2)

with col_cfg1:
    with st.container(border=True):
        st.subheader("Perfil de Usuario")
        nuevo_usuario = st.text_input(
            "Nombre del Operador:",
            value=st.session_state.get("usuario_conectado", "Operador")
        )
        if st.button("Actualizar Nombre de Operador", type="primary"):
            st.session_state.usuario_conectado = nuevo_usuario
            st.success(f"Operador actualizado a: **{nuevo_usuario}**")

with col_cfg2:
    with st.container(border=True):
        st.subheader("Opciones de Notificaciones y Telemetría")
        st.toggle("Habilitar registros detallados (DEBUG)", value=True)
        st.selectbox("Zona Horaria:", ["UTC-5 (Lima / Bogotá)", "UTC-6 (CDMX)", "UTC-3 (Buenos Aires / Santiago)", "UTC+1 (Madrid)"])
        st.slider("Intervalo de refresco de sensores (segundos):", 1, 10, 2)

st.divider()
st.caption(f"Sesión iniciada. Total de navegaciones acumuladas: {st.session_state.get('visitas_totales', 1)}")
