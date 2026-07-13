# 📍 MadTech SmartCity Hub - Panel Operativo Web

¡Bienvenido/a a **SmartCity Hub**! Este es un sistema de gestión crítica a nivel municipal diseñado para reportar, auditar y resolver incidencias urbanas en tiempo real. Este proyecto ha sido desarrollado como una solución integral que demuestra habilidades avanzadas en desarrollo Full-Stack, optimización de interfaces dinámicas y lógica de control de acceso basada en roles.

**Desarrollado por:** Ing. Briggitte Pérez 🚀

---

## 🌐 Demo en Vivo y Despliegue

La aplicación se encuentra desplegada y operativa en la nube. Puedes interactuar con ella directamente en el siguiente enlace:

🔗 **[Ver Aplicación en Vivo (Render)](https://smartcity-hub-panel.onrender.com)**

> ⚠️ **Nota sobre el Servidor de Pruebas (Render Free):**
> Al estar alojado en una instancia gratuita de Render, el servidor entra en "estado de suspensión" tras unos minutos de inactividad. Si al hacer clic en el enlace tarda en cargar o muestra un mensaje de *"Not Found"*, **por favor refresca la página (F5 o Recargar)** para despertar el contenedor. Tardará unos segundos en activarse y luego funcionará con total fluidez.

---

## 💻 Características Principales

* **Gestión de Incidencias en Tiempo Real:** Los usuarios pueden reportar problemas urbanos (averías, limpieza, semáforos) adjuntando descripciones, ubicaciones exactas y evidencias fotográficas.
* **Control de Acceso de Roles Dinámico (RBAC):** * **Ciudadanos / Vecinos:** Vista limpia en modo lectura de las incidencias globales con opción de registrar nuevos reportes.
    * **Operarios (Administradores):** Panel de control avanzado que transforma las celdas en elementos interactivos (`<select>`) para modificar la prioridad y el estado sobre la marcha. Incluye herramientas de eliminación y acceso a bitácoras de seguridad.
* **Buscador Inteligente Multi-Criterio:** Algoritmo desarrollado en JavaScript puro que extrae y mapea dinámicamente celdas de texto plano y valores internos de componentes `<select>`, permitiendo filtrados instantáneos por *descripción*, *ubicación*, *prioridad* o *estado* sin recargar la página.
* **Módulo de Auditoría y Seguridad:** Bitácora persistente que registra cada movimiento crítico realizado por los operarios para garantizar la transparencia en la gestión de datos.
* **Dashboard Estadístico:** Tarjetas dinámicas con contadores automáticos del estado del municipio (Total, Abiertas, En Proceso, Resueltas).

---

## 🛠️ Stack Tecnológico

* **Backend:** Python 3.x / Flask Framework
* **Frontend:** HTML5, CSS3 Avanzado, Bootstrap 5 (UI Responsiva)
* **Iconografía:** FontAwesome 6
* **Lógica del Cliente:** Vanilla JavaScript (ES6+)
* **Base de Datos / Persistencia:** Gestión e inyección dinámica de datos relacionales estructurados (SQLite3).

---

## 🔧 Instrucciones de Configuración Local

Si deseas ejecutar este proyecto en tu entorno local, sigue estos pasos:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/BriggittePerezS/smartcity-hub-panel.git](https://github.com/BriggittePerezS/smartcity-hub-panel.git)
cd smartcity-hub-panel
