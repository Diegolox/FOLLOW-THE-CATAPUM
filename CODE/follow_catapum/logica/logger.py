from datetime import datetime
from queue import Queue


class Logger:
    """
    Logger global thread-safe.

    Permite llamar a log("texto") desde:
    - app.py
    - cualquier fichero externo
    - hilo principal
    - hilos secundarios

    La interfaz gráfica NO se actualiza directamente desde aquí.
    Solo se mete el mensaje en una cola segura.
    """

    _cola_logs = Queue()

    @classmethod
    def log(cls, mensaje: str):
        hora = datetime.now().strftime("%H:%M:%S")
        texto = f"[{hora}] {mensaje}"
        cls._cola_logs.put(texto)

    @classmethod
    def leer_logs(cls, max_logs: int = 100):
        mensajes = []

        for _ in range(max_logs):
            if cls._cola_logs.empty():
                break

            mensajes.append(cls._cola_logs.get())

        return mensajes


def log(mensaje: str):
    """
    Función cómoda para usar directamente:

        log("Texto para la consola")
    """
    Logger.log(mensaje)