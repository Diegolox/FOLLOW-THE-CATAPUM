# ============================================================
# comunicacion_serial.py
# Comunicación serie con ESP32
# ============================================================

import random

from follow_catapum.logica.logger import log


try:
    import serial
    from serial.tools import list_ports
except Exception:
    serial = None
    list_ports = None


_conexion_serial = None


# ============================================================
# PUERTOS
# ============================================================

def listar_puertos_disponibles():
    """
    Devuelve una lista de puertos serie disponibles.

    Formato:
        [
            {
                "dispositivo": "COM3",
                "descripcion": "USB Serial Device",
                "hwid": "..."
            }
        ]
    """

    if list_ports is None:
        log("ERROR: pyserial no está instalado. Instala pyserial para listar puertos COM.")
        return []

    puertos = []

    for puerto in list_ports.comports():
        puertos.append({
            "dispositivo": puerto.device,
            "descripcion": puerto.description,
            "hwid": puerto.hwid,
        })

    return puertos


# ============================================================
# CONEXIÓN
# ============================================================

def abrir_puerto_serial(puerto: str, baudrate: int, timeout: float = 1.0):
    """
    Abre el puerto serie.
    """

    global _conexion_serial

    if serial is None:
        log("ERROR: pyserial no está instalado. No se puede abrir el puerto serie.")
        return False

    if not puerto:
        log("ERROR: Puerto COM vacío.")
        return False

    try:
        if _conexion_serial is not None and _conexion_serial.is_open:
            log("Ya existe una conexión serial abierta.")
            return True

        _conexion_serial = serial.Serial(
            port=puerto,
            baudrate=int(baudrate),
            timeout=float(timeout)
        )

        log(f"Puerto serie conectado: {puerto} @ {baudrate} baudios")

        return True

    except Exception as e:
        _conexion_serial = None
        log(f"ERROR al abrir puerto serie {puerto}: {e}")
        return False



def cerrar_puerto_serial():
    """
    Cierra el puerto serie si está abierto.
    """

    global _conexion_serial

    try:
        if _conexion_serial is None:
            log("No había conexión serial abierta.")
            return True

        if _conexion_serial.is_open:
            puerto = _conexion_serial.port
            _conexion_serial.close()
            log(f"Puerto serie cerrado: {puerto}")

        _conexion_serial = None

        return True

    except Exception as e:
        log(f"ERROR al cerrar puerto serie: {e}")
        _conexion_serial = None
        return False



def puerto_serial_conectado():
    """
    Devuelve True si hay puerto serie abierto.
    """

    try:
        return _conexion_serial is not None and _conexion_serial.is_open
    except Exception:
        return False


# ============================================================
# LECTURA
# ============================================================

def leer_datos_esp32_serial():
    """
    Lee una línea del puerto serie.

    Formato recomendado enviado por el ESP32:
        acc_x;acc_y;acc_z;pitch;roll;yaw;vel;vel_max;latitud;longitud;altura;altura_max;temperatura;estado;flag\n

    Ejemplo:
        5298.596;146.2;52.896581;0.0;0.0;0.0;12.3;18.5;41.6488;-0.8891;230.4;412.8;28.5;8;3\n

    También se acepta JSON si core.py recibe una línea que empieza por '{'.

    Devuelve:
        - string si ha llegado una línea
        - None si no hay datos disponibles
    """

    if not puerto_serial_conectado():
        return None

    try:
        if _conexion_serial.in_waiting <= 0:
            return None

        linea = _conexion_serial.readline()
        texto = linea.decode("utf-8", errors="ignore").strip()

        if not texto:
            return None

        return texto

    except Exception as e:
        log(f"ERROR leyendo puerto serie: {e}")
        return None



def leer_datos_esp32_prueba():
    """
    Simula una lectura del ESP32.

    Devuelve una línea con los 15 sensores separados por ';'.
    """

    valores = [
        round(random.uniform(-16, 16), 3),       # acc_x [G]
        round(random.uniform(-16, 16), 3),       # acc_y [G]
        round(random.uniform(-16, 16), 3),       # acc_z [G]
        round(random.uniform(-180, 180), 2),     # pitch [°]
        round(random.uniform(-180, 180), 2),     # roll [°]
        round(random.uniform(0, 360), 2),        # yaw [°]
        round(random.uniform(0, 250), 2),        # vel [m/s]
        round(random.uniform(0, 300), 2),        # vel_max [m/s]
        round(random.uniform(-90, 90), 6),       # latitud [°]
        round(random.uniform(-180, 180), 6),     # longitud [°]
        round(random.uniform(0, 3000), 2),       # altura [m]
        round(random.uniform(0, 5000), 2),       # altura_max [m]
        round(random.uniform(-20, 80), 1),       # temperatura [°C]
        random.randint(0, 10),                   # estado
        random.randint(0, 255),                  # flag
    ]

    return ";".join(str(valor) for valor in valores) + "\n"
