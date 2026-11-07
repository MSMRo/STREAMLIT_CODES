# Tutorial 09: Aplicaciones Multipágina y Navegación Modular

En este tutorial aprenderás cómo estructurar aplicaciones grandes y escalables utilizando el sistema nativo de páginas múltiples de Streamlit.

---

## 🎯 Objetivos de Aprendizaje
- Comprender la convención del directorio `pages/`.
- Configurar la nomenclatura de archivos (`1_inicio.py`, `2_analisis.py`) para definir el orden en el menú lateral.
- Compartir datos y estado de usuario de forma transparente entre todas las páginas mediante `st.session_state`.
- Diseñar dashboards industriales organizados por áreas de responsabilidad:
  - Vista general / resumen.
  - Análisis analítico y filtrado de datasets.
  - Monitoreo de hardware e inventario de red.
  - Ajustes de configuración globales.

---

## 📁 Convención de Estructura de Archivos

```
09_aplicacion_multipagina/
├── app.py                      # Página principal (Home / Entrypoint)
├── README.md                   # Documentación del tutorial
└── pages/                      # Directorio especial reconocido por Streamlit
    ├── 1_analisis_datos.py     # Subpágina 1
    ├── 2_dispositivos_iot.py   # Subpágina 2
    └── 3_configuracion.py      # Subpágina 3
```

> **Consejo:** Los prefijos numéricos `1_`, `2_`, etc., determinan el orden exacto de aparición en la barra lateral. Streamlit remueve automáticamente los guiones bajos y los números al renderizar los títulos en la interfaz.

---

## 🚀 Cómo Ejecutar

```bash
uv run streamlit run 09_aplicacion_multipagina/app.py
```
