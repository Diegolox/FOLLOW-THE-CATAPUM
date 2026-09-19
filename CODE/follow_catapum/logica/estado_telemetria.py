# ============================================================
# estado_telemetria.py
# Estado interno de la sesión de telemetría
# ============================================================

from dataclasses import dataclass
from datetime import datetime


@dataclass
class EstadoTelemetria:
    conectado: bool = False
    leyendo: bool = False
    muestras_recibidas: int = 0
    errores_json: int = 0
    ultimo_dato_valido: datetime | None = None
    puerto_actual: str = ""
    baudrate_actual: int | None = None

    def registrar_conexion(self, puerto: str, baudrate: int):
        self.conectado = True
        self.puerto_actual = puerto
        self.baudrate_actual = baudrate

    def registrar_desconexion(self):
        self.conectado = False
        self.leyendo = False
        self.puerto_actual = ""
        self.baudrate_actual = None

    def iniciar_lectura(self):
        self.leyendo = True

    def detener_lectura(self):
        self.leyendo = False

    def registrar_muestra_valida(self):
        self.muestras_recibidas += 1
        self.ultimo_dato_valido = datetime.now()

    def registrar_error_json(self):
        self.errores_json += 1

    def segundos_desde_ultimo_dato(self):
        if self.ultimo_dato_valido is None:
            return None

        return (datetime.now() - self.ultimo_dato_valido).total_seconds()
