# ============================================================
# registro_telemetria.py
# Funciones simples para guardar telemetría
# ============================================================

import json
from pathlib import Path
from datetime import datetime

import pandas as pd

from follow_catapum.logica.logger import log


def crear_registro():
    """
    Crea el registro en memoria.
    """

    log("Registro de telemetría creado en memoria.")

    return []


def preparar_muestra(datos: dict) -> dict:
    """
    Prepara una muestra recibida del ESP32.

    Añade timestamp del PC.
    """

    muestra = dict(datos)

    muestra["timestamp_pc"] = datetime.now().isoformat(timespec="milliseconds")

    return muestra


def guardar_muestra_jsonl(ruta_jsonl, muestra: dict):
    """
    Guarda una muestra en formato JSONL.

    Cada línea del archivo es una muestra independiente.
    """

    ruta_jsonl = Path(ruta_jsonl)

    try:
        ruta_jsonl.parent.mkdir(parents=True, exist_ok=True)

        with open(ruta_jsonl, "a", encoding="utf-8") as f:
            f.write(json.dumps(muestra, ensure_ascii=False) + "\n")
            f.flush()

        return True

    except Exception as e:
        log(f"ERROR al guardar muestra en JSONL: {e}")
        return False


def añadir_muestra(registro: list, muestra: dict):
    """
    Añade una muestra al registro en memoria.
    """

    registro.append(muestra)


def crear_dataframe(registro: list) -> pd.DataFrame:
    """
    Convierte el registro en un DataFrame de pandas.
    """

    df = pd.DataFrame(registro)

    log(f"DataFrame creado con {len(df)} muestras.")

    return df


def guardar_dataframe_csv(df: pd.DataFrame, ruta_csv):
    """
    Guarda el DataFrame en CSV.
    """

    ruta_csv = Path(ruta_csv)

    try:
        ruta_csv.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(ruta_csv, index=False)

        return True

    except Exception as e:
        log(f"ERROR al guardar CSV: {e}")
        return False


def guardar_dataframe_excel(df: pd.DataFrame, ruta_excel):
    """
    Guarda el DataFrame en Excel.
    """

    ruta_excel = Path(ruta_excel)

    try:
        ruta_excel.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(ruta_excel, index=False)

        return True

    except Exception as e:
        log(f"ERROR al guardar Excel: {e}")
        return False


def cargar_jsonl_como_dataframe(ruta_jsonl) -> pd.DataFrame:
    """
    Carga un archivo JSONL y lo convierte en DataFrame.

    Útil si la app se cae y quieres recuperar los datos guardados.
    """

    ruta_jsonl = Path(ruta_jsonl)

    muestras = []

    if not ruta_jsonl.exists():
        log(f"No existe el archivo JSONL: {ruta_jsonl}")
        return pd.DataFrame()

    try:
        with open(ruta_jsonl, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()

                if linea:
                    muestras.append(json.loads(linea))

        df = pd.DataFrame(muestras)

        log(f"JSONL recuperado correctamente. Muestras cargadas: {len(df)}")

        return df

    except Exception as e:
        log(f"ERROR al cargar JSONL como DataFrame: {e}")
        return pd.DataFrame()