# Tourism Watcher

Proyecto en Python para monitorizar las viviendas turísticas en Granada, España. Puedes encontrar los datos obtenidos hasta ahora en la carpeta `data.
Los datos recogidos se obtienen de la búsqueda:

 - 15/10/2024 - Actualidad: Destino "Granada, España", "cualquier semana" y Airbnb preselecciona un viaje de 5 noches.

## Roadmap

1. Extracción de datos de Airbnb. ✔️
2. Extracción de datos públicos de las viviendas a partir del permiso turístico.
3. Eliminar programación necesaria para el uso / añadir UI.
4. Creación de análsis de los datos recogidos.
5. Extracción de datos de otros portales.

## Prerrequisitos

- Drivers para el navegador que vas a utilizar. En [esta página](https://www.selenium.dev/downloads/) puedes encontrar los drivers que necesitas.
- Python 3.12
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) (versión probada: 4.12.13)
- [Selenium](https://pypi.org/project/selenium/) (versión probada: 4.25.0)

## Instalación

Para "instalar" el programa, clona el repositorio o, alternativamente, descarga el .zip y extráelo

## Uso

Para utilizar el programa, modifica el archivo `main.py` si deseas cambiar algo. Si no, simplemente ejecútalo.

Este es el archivo `main.py` por defecto.
```python
import logging
from airbnb import AirbnbScrapper

def start_logger(log_file: str = None) ...

if __name__ == "__main__":
    logger = start_logger()
    logger.info("Starting scrapper")

    with AirbnbScrapper("firefox") as scrapper:  # Cambiar por tu navegador
        scrapper.extract()  # Añadir opciones adicionales

    logger.info("Ending scrapper")
```

Los navegadores posibles y las opciones adicionales se pueden encontrar en [`airbnb.py`](airbnb/airbnb.py) y [`types.py`](airbnb/types.py)

## Contribuye

Las pull requests son bienvenidas. Si quieres realizar grandes cambios, por favor abre primero un issue explicando que quieres cambiar y enlázalo con la pull request.
También puedes resolver cualquier issue que no esté asignado, enlazando ese issue en tu pull request.

Por favor prueba que todo funcione antes de mandar la pull request :)
