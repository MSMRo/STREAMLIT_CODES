# Tutorial 12: Integración de Bases de Datos Relacionales (SQLite y PostgreSQL)

En este tutorial aprenderás a conectar tus aplicaciones de Streamlit con bases de datos relacionales para persistir, consultar, filtrar y analizar históricos de mediciones de sensores y dispositivos IoT.

---

## 🎯 Objetivos de Aprendizaje
- Comprender la diferencia entre persistencia en memoria (`st.session_state`) vs persistencia física en bases de datos relacionales (RDBMS).
- Trabajar con **SQLite**: Base de datos ligera, local, embebida y sin configuración (archivo `.db`).
- Conectar con **PostgreSQL**: Servidor de base de datos industrial de alto rendimiento apto para producción masiva.
- Utilizar **SQLAlchemy** y el motor de consultas para parametrizar sentencias SQL de forma segura contra inyecciones SQL.
- Implementar operaciones **CRUD** completas:
  - **Create**: Formularios de inserción y generador masivo de series de tiempo.
  - **Read**: Consultas con filtros de rango, límites, agregaciones (`AVG`, `MIN`, `MAX`) y visualización en DataFrames.
  - **Delete**: Vaciado y mantenimiento de tablas.
- Ejecutar consultas SQL personalizadas en una consola interactiva integrada.
- Exportar reportes filtrados a archivos CSV con `st.download_button`.

---

## ⚖️ Comparativa: SQLite vs PostgreSQL

| Característica | SQLite | PostgreSQL |
| :--- | :--- | :--- |
| **Tipo** | Embebida en un solo archivo local (`.db`) | Servidor cliente/servidor independiente |
| **Instalación** | Cero configuración (incluido en Python) | Requiere servidor local, Docker o servicio Cloud |
| **Escrituras Concurrentes** | Bloqueo a nivel de archivo (limitado a 1 escritor) | Bloqueo por fila de alta concurrencia |
| **Ideal para** | Prototipos, pruebas locales, dashboards individuales, Raspberry Pi | Producción, múltiples usuarios concurrentes, Big Data, TimescaleDB |

---

## 🐘 Cómo Levantar PostgreSQL en 5 Segundos con Docker

Si deseas probar el modo PostgreSQL sin instalar el servidor completo en Windows:

```bash
docker run -d --name pg-iot -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=iot_db postgres:alpine
```

Luego, en la barra lateral del tutorial, cambia a **PostgreSQL (Servidor)** con las credenciales por defecto (`localhost:5432`, user: `postgres`, pass: `postgres`, db: `iot_db`).

---

## 🚀 Cómo Ejecutar Este Tutorial

```bash
uv run streamlit run 12_bases_de_datos_sqlite_postgresql/app.py
```
*(Por defecto se iniciará en modo SQLite local de forma totalmente automática sin requerir ninguna configuración externa).*
