from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
EXIT_DIR = Path(BASE_DIR).resolve().parents[1]

ASSETS_DIR = BASE_DIR / "assets"
CONFIG_DIR = BASE_DIR / "config"
FILES_DIR = BASE_DIR / "files"
OUTPUTS_DIR = FILES_DIR / "outputs"

RUTA_ICONO_APP = ASSETS_DIR / "icono.ico"

RUTA_ICONO_SENSOR_1 = ASSETS_DIR / "sensor_1.ico"
RUTA_ICONO_SENSOR_2 = ASSETS_DIR / "sensor_2.ico"
RUTA_ICONO_SENSOR_3 = ASSETS_DIR / "sensor_3.ico"

RUTA_CONFIG_APP = CONFIG_DIR / "config_app.json"


RUTA_JSONL = OUTPUTS_DIR / "telemetria_vuelo.jsonl"
RUTA_CSV = OUTPUTS_DIR / "telemetria_vuelo.csv"
RUTA_EXCEL = FILES_DIR / "telemetria_vuelo.xlsx"


RUTA_ICONO_ACELERACION = ASSETS_DIR / "ACELERAR.ico"
RUTA_ICONO_ANGULOS = ASSETS_DIR / "GIRAR.ico"
RUTA_ICONO_VELOCIDAD = ASSETS_DIR / "COHETE.ico"
RUTA_ICONO_GPS = ASSETS_DIR / "MAPA.ico"
RUTA_ICONO_ALTURA = ASSETS_DIR / "NUBE.ico"
RUTA_ICONO_TEMPERATURA = ASSETS_DIR / "TEMPERATURA.ico"
RUTA_ICONO_ESTADO = ASSETS_DIR / "PAIS.ico"
RUTA_ICONO_FLAG = ASSETS_DIR / "FLAG.ico"
