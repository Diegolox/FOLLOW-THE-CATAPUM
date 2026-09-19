# ============================================================
# core.py
# Lógica principal de telemetría ESP32 → interfaz + registro
# ============================================================

import json

from follow_catapum.config_sensores import (
    SENSORES_TELEMETRIA,
    CLAVES_SENSORES_TELEMETRIA,
)

from follow_catapum.logica.logger import log

from follow_catapum.logica.registro_telemetria import (
    crear_registro,
    preparar_muestra,
    guardar_muestra_jsonl,
    añadir_muestra,
    crear_dataframe,
    guardar_dataframe_csv,
    guardar_dataframe_excel,
)

from follow_catapum.logica.comunicacion_serial import (
    listar_puertos_disponibles,
    abrir_puerto_serial,
    cerrar_puerto_serial,
    puerto_serial_conectado,
    leer_datos_esp32_serial,
    leer_datos_esp32_prueba,
)

from follow_catapum.rutas import RUTA_JSONL, RUTA_CSV, RUTA_EXCEL


# ============================================================
# FORMATO ESPERADO DESDE EL ESP32
# ============================================================
#
# Formato recomendado actual:
#     acc_x;acc_y;acc_z;pitch;roll;yaw;vel;vel_max;latitud;longitud;altura;altura_max;temperatura;estado;flag\n
#
# Ejemplo:
#     5298.596;146.2;52.896581;0.0;0.0;0.0;12.3;18.5;41.6488;-0.8891;230.4;412.8;28.5;8;3\n
#
# También se acepta JSON por compatibilidad, con estas claves:
#     {
#         "acc_x": 5298.596,
#         "acc_y": 146.2,
#         "acc_z": 52.896581,
#         "pitch": 0.0,
#         "roll": 0.0,
#         "yaw": 0.0,
#         "vel": 12.3,
#         "vel_max": 18.5,
#         "latitud": 41.6488,
#         "longitud": -0.8891,
#         "altura": 230.4,
#         "altura_max": 412.8,
#         "temperatura": 28.5,
#         "estado": 8,
#         "flag": 3
#     }
#
# En ambos casos, el orden y los tipos se definen en config_sensores.py.
# ============================================================


# ============================================================
# CONEXIÓN SERIAL
# ============================================================

def listar_puertos_com():
    """
    Lista los puertos COM disponibles usando comunicacion_serial.py.
    También los escribe en el log.
    """

    puertos = listar_puertos_disponibles()

    if not puertos:
        log("No se han encontrado puertos COM disponibles.")
        return []

    log("Puertos COM disponibles:")

    for puerto in puertos:
        dispositivo = puerto.get("dispositivo", "")
        descripcion = puerto.get("descripcion", "")
        log(f"  - {dispositivo} | {descripcion}")

    return puertos



def conectar_serial(puerto: str, baudrate: int, timeout: float = 1.0):
    """
    Abre la conexión serial.
    """

    return abrir_puerto_serial(
        puerto=puerto,
        baudrate=baudrate,
        timeout=timeout
    )



def desconectar_serial():
    """
    Cierra la conexión serial.
    """

    return cerrar_puerto_serial()



def serial_esta_conectado():
    """
    Devuelve True si el puerto serie está abierto.
    """

    return puerto_serial_conectado()


# ============================================================
# INICIO / FIN TELEMETRÍA
# ============================================================

def iniciar_telemetria():
    """
    Inicializa el registro de telemetría.
    """

    registro = crear_registro()

    log("Telemetría iniciada.")
    log(f"Archivo de respaldo JSONL: {RUTA_JSONL}")

    return registro



def finalizar_telemetria(registro):
    """
    Finaliza la telemetría.

    Convierte el registro en DataFrame y lo guarda en CSV y Excel.
    """

    log("Finalizando telemetría...")

    df = crear_dataframe(registro)

    csv_ok = guardar_dataframe_csv(df, RUTA_CSV)
    excel_ok = guardar_dataframe_excel(df, RUTA_EXCEL)

    if csv_ok:
        log(f"CSV guardado: {RUTA_CSV}")

    if excel_ok:
        log(f"Excel guardado: {RUTA_EXCEL}")

    log(f"Muestras registradas: {len(df)}")

    return df


# ============================================================
# LECTURA Y PROCESADO DE DATOS
# ============================================================

def leer_y_procesar_datos_esp32(
    sensores,
    registro,
    modo_prueba: bool = False
):
    """
    Función de alto nivel.

    Pide un dato a comunicacion_serial.py y lo procesa:
    - convierte el mensaje recibido a diccionario
    - guarda muestra en JSONL
    - añade muestra al registro
    - actualiza sensores de la interfaz

    Formato recomendado:
        acc_x;acc_y;acc_z;pitch;roll;yaw;vel;vel_max;latitud;longitud;altura;altura_max;temperatura;estado;flag\n

    También acepta JSON tipo diccionario con las mismas claves.

    Devuelve:
        {
            "ok": True/False,
            "tipo_error": None / "sin_datos" / "formato" / "guardado",
            "muestra": dict | None
        }
    """

    if modo_prueba:
        mensaje_esp32 = leer_datos_esp32_prueba()
    else:
        mensaje_esp32 = leer_datos_esp32_serial()

    if not mensaje_esp32:
        return {
            "ok": False,
            "tipo_error": "sin_datos",
            "muestra": None
        }

    return procesar_mensaje_esp32(
        mensaje_esp32=mensaje_esp32,
        sensores=sensores,
        registro=registro
    )


# ============================================================
# PROCESADO DE MENSAJES
# ============================================================

def procesar_mensaje_esp32(mensaje_esp32, sensores, registro):
    """
    Procesa un mensaje recibido desde el ESP32.

    Hace:
    1. Convertir el mensaje a diccionario.
    2. Añadir timestamp del PC.
    3. Guardar la muestra en JSONL.
    4. Añadir la muestra al registro en memoria.
    5. Actualizar sensores de la interfaz.
    """

    datos = convertir_mensaje_a_dict(mensaje_esp32)

    if datos is None:
        return {
            "ok": False,
            "tipo_error": "formato",
            "muestra": None
        }

    muestra = preparar_muestra(datos)

    guardado_ok = guardar_muestra_jsonl(RUTA_JSONL, muestra)

    if not guardado_ok:
        log("ERROR: La muestra no se ha podido guardar en JSONL.")
        return {
            "ok": False,
            "tipo_error": "guardado",
            "muestra": muestra
        }

    añadir_muestra(registro, muestra)

    actualizar_interfaz_sensores(sensores, muestra)

    return {
        "ok": True,
        "tipo_error": None,
        "muestra": muestra
    }


# ============================================================
# PARSEO DE MENSAJES
# ============================================================

def convertir_mensaje_a_dict(mensaje_esp32):
    """
    Convierte el mensaje recibido en un diccionario.

    Formato principal esperado:
        valor_1;valor_2;valor_3;...;estado;flag\n

    También acepta JSON tipo diccionario:
        {"acc_x": 1.0, "acc_y": 2.0, ...}
    """

    texto = str(mensaje_esp32).strip()

    if not texto:
        log("ERROR: Mensaje vacío recibido desde ESP32.")
        return None

    if texto.startswith("{"):
        return convertir_json_a_dict(texto)

    return convertir_linea_separada_por_punto_y_coma(texto)



def convertir_linea_separada_por_punto_y_coma(texto: str):
    """
    Convierte una línea separada por ';' al diccionario de sensores.

    El orden de los valores debe coincidir con SENSORES_TELEMETRIA.
    """

    partes = [parte.strip() for parte in texto.split(";")]

    if partes and partes[-1] == "":
        partes = partes[:-1]

    numero_esperado = len(SENSORES_TELEMETRIA)

    if len(partes) != numero_esperado:
        log(
            "ERROR: Número de campos incorrecto. "
            f"Recibidos: {len(partes)} | Esperados: {numero_esperado}"
        )
        return None

    datos = {}

    for indice, config_sensor in enumerate(SENSORES_TELEMETRIA):
        clave = config_sensor["clave"]
        tipo_variable = config_sensor.get("tipo_variable", "float")
        valor_texto = partes[indice]

        valor = convertir_valor_sensor(
            valor_texto=valor_texto,
            tipo_variable=tipo_variable,
            clave=clave
        )

        if valor is None:
            return None

        datos[clave] = valor

    return datos



def convertir_json_a_dict(mensaje_json):
    """
    Convierte un JSON recibido desde el ESP32 en un diccionario normalizado.

    El JSON debe tener, como mínimo, todas las claves de CLAVES_SENSORES_TELEMETRIA.
    Si trae claves extra, se ignoran para mantener una tabla de salida limpia.
    """

    try:
        datos_json = json.loads(mensaje_json)

        if not isinstance(datos_json, dict):
            log("ERROR: El JSON recibido no es un diccionario.")
            return None

        return normalizar_diccionario_sensores(datos_json)

    except json.JSONDecodeError:
        log("ERROR: JSON mal formado recibido desde ESP32.")
        return None

    except Exception as e:
        log(f"ERROR al convertir JSON recibido: {e}")
        return None



def normalizar_diccionario_sensores(datos_json: dict):
    """
    Valida y convierte un diccionario con claves de sensores.
    """

    claves_recibidas = set(datos_json.keys())
    claves_esperadas = set(CLAVES_SENSORES_TELEMETRIA)
    claves_faltantes = claves_esperadas - claves_recibidas

    if claves_faltantes:
        log(
            "ERROR: JSON incompleto. Faltan claves: "
            + ", ".join(sorted(claves_faltantes))
        )
        return None

    datos = {}

    for config_sensor in SENSORES_TELEMETRIA:
        clave = config_sensor["clave"]
        tipo_variable = config_sensor.get("tipo_variable", "float")

        valor = convertir_valor_sensor(
            valor_texto=datos_json[clave],
            tipo_variable=tipo_variable,
            clave=clave
        )

        if valor is None:
            return None

        datos[clave] = valor

    return datos



def convertir_valor_sensor(valor_texto, tipo_variable: str, clave: str):
    """
    Convierte un campo del mensaje al tipo indicado por la configuración.
    """

    try:
        texto = str(valor_texto).strip().replace(",", ".")

        if tipo_variable == "int":
            return int(float(texto))

        if tipo_variable == "byte":
            valor = int(float(texto))
            return max(0, min(255, valor))

        if tipo_variable == "bool":
            return bool(int(float(texto)))

        if tipo_variable == "str":
            return str(valor_texto)

        return float(texto)

    except Exception:
        log(
            f"ERROR: No se pudo convertir el campo '{clave}' "
            f"con valor '{valor_texto}' a tipo '{tipo_variable}'."
        )
        return None


# ============================================================
# INTERFAZ
# ============================================================

def actualizar_interfaz_sensores(sensores, muestra):
    """
    Actualiza los sensores visuales de la interfaz.

    sensores debe ser un diccionario con claves como:
        acc_x, acc_y, acc_z, pitch, roll, yaw, vel, vel_max,
        latitud, longitud, altura, altura_max, temperatura, estado, flag

    Si una variable recibida no existe como sensor visual, se ignora.
    """

    for nombre_variable, valor in muestra.items():

        if nombre_variable in sensores:
            sensores[nombre_variable].actualizar_valor(valor)
