# 🏆 Workflow de Scraping de panamericana con GitHub Actions y Docker

Este proyecto implementa un flujo automatizado de extracción de datos sobre los productos de la pagina web de panamericana, utilizando GitHub Actions para CI/CD, contenerización con Docker y gestión segura de secretos.

---

## ⚙️ Estructura del Flujo de Trabajo

El proceso se gestiona mediante un único workflow en GitHub Actions: `docker.yml`, que realiza los siguientes pasos:

### 1. Preparación del Entorno
- Ejecuta el flujo en un entorno Linux (`ubuntu-latest`).
- Configura Python 3.9 y sus dependencias con `setup.py`.

### 2. Login y Contenerización con Docker
- Inicia sesión en Docker Hub usando los secretos `DOCKER_USERNAME` y `DOCKER_TOKEN`.
- Construye una imagen Docker (`scraper_docker`) que incluye el script de scraping.
- Ejecuta la imagen para generar automáticamente el archivo CSV y la base de datos con los datos extraídos en la pagina.

### 3. Commit Automático
- Si hay cambios generados por el scraping, estos se versionan automáticamente en el repositorio mediante `git-auto-commit-action`.

---

## 🔒 Requisitos para la Configuración

Debes configurar los siguientes **secretos** en GitHub para habilitar el workflow:

- `DOCKER_USERNAME`: Usuario de Docker Hub.
- `DOCKER_TOKEN`: Token de acceso a Docker Hub.

---

## 🗂️ Estructura del Proyecto

```
scraper-panamericana/
├── .github/
│ └── workflows/
│ └── docker.yml
├── build/
│ └── lib/
│ └── edu_pad/
├── dist/
│ └── edu_pad-0.0.1-py3.12.egg
├── src/
│ ├── edu_pad/
│ │ ├── scraper/
│ │ │ ├── storage/
│ │ │ │ ├── db.py
│ │ │ │ └── excel.py
│ │ │ ├── config.py
│ │ │ ├── scraping.py
│ │ │ └── utils.py
│ │ ├── static/
│ │ │ ├── db/
│ │ │ │ └── Productos_Panamericana.db
│ │ │ └── xlsx/
│ │ │ └── Productos_Panamericana.xlsx
│ │ └── main.py # Punto de entrada
│ └── edu_pad.egg-info/
├── .gitignore
├── accionables.yml
├── Dockerfile
└── setup.py
```

---

## 🚀 Instalación y Ejecución

1. Clona este repositorio:  
   `git clone https://github.com/Saimon7741/scraper-panamericana.git`

2. Configura los secretos necesarios en GitHub.

3. El flujo `docker.yml` se ejecutará automáticamente al hacer push al branch `main` o de forma manual desde la interfaz de GitHub Actions.

---

## 🌟 Características Principales

- **Automatizado**: El scraping, versionado y despliegue se ejecutan sin intervención manual.
- **Contenerizado**: El proceso corre dentro de una imagen Docker reproducible.
- **Seguro**: Gestión de credenciales mediante secretos de GitHub.
- **Trazable**: Cada ejecución queda registrada y versionada automáticamente.

---

## 🛠️ Personalización

- Puedes modificar la busqueda desde python `Run python src/edu_pad/main.py --search "su busqueda"` o en docker seria: `docker run --rm scraper_docker --search "su busqueda"`, de momento solo se puede buscar solamente la primera palabra del producto.
- Ajusta el `Dockerfile` si necesitas nuevas dependencias o rutas de ejecución.
- Cambia la frecuencia o condiciones del flujo editando `docker.yml`.
