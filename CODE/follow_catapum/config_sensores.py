# ============================================================
# config_sensores.py
# Configuración ordenada de sensores de telemetría
# ============================================================

"""
Orden esperado del mensaje enviado por el ESP32:

    acc_x;acc_y;acc_z;pitch;roll;yaw;vel;vel_max;latitud;longitud;altura;altura_max;temperatura;estado;flag\n
Ejemplo:

    5298.596;146.2;52.896581;0.0;0.0;0.0;12.3;18.5;41.6488;-0.8891;230.4;412.8;28.5;8;3\n
Cada entrada de SENSORES_TELEMETRIA representa un sensor visual único.
El orden de esta lista es el mismo que el orden de los campos recibidos por serial.
"""

from follow_catapum.rutas import (
    RUTA_ICONO_ACELERACION,
    RUTA_ICONO_ANGULOS,
    RUTA_ICONO_VELOCIDAD,
    RUTA_ICONO_GPS,
    RUTA_ICONO_ALTURA,
    RUTA_ICONO_TEMPERATURA,
    RUTA_ICONO_ESTADO,
    RUTA_ICONO_FLAG,
)


SENSORES_TELEMETRIA = [
    {
        "clave": "acc_x",
        "texto": "ACC X [G]",
        "ruta_icono": RUTA_ICONO_ACELERACION,
        "tipo_variable": "float",
        "valor_inicial": 0.0,
        "decimales": 3,
    },
    {
        "clave": "acc_y",
        "texto": "ACC Y [G]",
        "ruta_icono": RUTA_ICONO_ACELERACION,
        "tipo_variable": "float",
        "valor_inicial": 0.0,
        "decimales": 3,
    },
    {
        "clave": "acc_z",
        "texto": "ACC Z [G]",
        "ruta_icono": RUTA_ICONO_ACELERACION,
        "tipo_variable": "float",
        "valor_inicial": 0.0,
        "decimales": 3,
    },
    {
        "clave": "pitch",
        "texto": "PITCH [°]",
        "ruta_icono": RUTA_ICONO_ANGULOS,
        "tipo_variable": "float",
        "valor_inicial": 0.0,
        "decimales": 2,
    },
    {
        "clave": "roll",
        "texto": "ROLL [°]",
        "ruta_icono": RUTA_ICONO_ANGULOS,
        "tipo_variable": "float",
        "valor_inicial": 0.0,
        "decimales": 2,
    },
    {
        "clave": "yaw",
        "texto": "YAW [°]",
        "ruta_icono": RUTA_ICONO_ANGULOS,
        "tipo_variable": "float",
        "valor_inicial": 0.0,
        "decimales": 2,
    },
    {
        "clave": "vel",
        "texto": "VEL [m/s]",
        "ruta_icono": RUTA_ICONO_VELOCIDAD,
        "tipo_variable": "float",
        "valor_inicial": 0.0,
        "decimales": 2,
    },
    {
        "clave": "vel_max",
        "texto": "VEL MAX [m/s]",
        "ruta_icono": RUTA_ICONO_VELOCIDAD,
        "tipo_variable": "float",
        "valor_inicial": 0.0,
        "decimales": 2,
    },
    {
        "clave": "latitud",
        "texto": "LAT [°]",
        "ruta_icono": RUTA_ICONO_GPS,
        "tipo_variable": "float",
        "valor_inicial": 0.0,
        "decimales": 6,
    },
    {
        "clave": "longitud",
        "texto": "LON [°]",
        "ruta_icono": RUTA_ICONO_GPS,
        "tipo_variable": "float",
        "valor_inicial": 0.0,
        "decimales": 6,
    },
    {
        "clave": "altura",
        "texto": "ALTURA [m]",
        "ruta_icono": RUTA_ICONO_ALTURA,
        "tipo_variable": "float",
        "valor_inicial": 0.0,
        "decimales": 2,
    },
    {
        "clave": "altura_max",
        "texto": "ALTURA MAX [m]",
        "ruta_icono": RUTA_ICONO_ALTURA,
        "tipo_variable": "float",
        "valor_inicial": 0.0,
        "decimales": 2,
    },
    {
        "clave": "temperatura",
        "texto": "TEMP [°C]",
        "ruta_icono": RUTA_ICONO_TEMPERATURA,
        "tipo_variable": "float",
        "valor_inicial": 0.0,
        "decimales": 1,
    },
    {
        "clave": "estado",
        "texto": "ESTADO",
        "ruta_icono": RUTA_ICONO_ESTADO,
        "tipo_variable": "int",
        "valor_inicial": 0,
        "decimales": 0,
    },
    {
        "clave": "flag",
        "texto": "FLAG",
        "ruta_icono": RUTA_ICONO_FLAG,
        "tipo_variable": "int",
        "valor_inicial": 0,
        "decimales": 0,
    },
]


CLAVES_SENSORES_TELEMETRIA = [sensor["clave"] for sensor in SENSORES_TELEMETRIA]
