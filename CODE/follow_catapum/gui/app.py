import customtkinter as ctk

from follow_catapum.rutas import (
    RUTA_ICONO_APP,
    RUTA_ICONO_SENSOR_1,
)

from follow_catapum.config_sensores import SENSORES_TELEMETRIA

from follow_catapum.gui.customframe import CustomFrame
from follow_catapum.gui.customscrollableframe import CustomScrollableFrame
from follow_catapum.gui.sensores import Sensor
from follow_catapum.gui.terminal import TerminalFrame
from follow_catapum.gui.estilos import fuente, color_texto
from follow_catapum.gui.panel_serial import PanelSerial

from follow_catapum.logica.logger import log
from follow_catapum.logica.core import iniciar_telemetria


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FOLLOW THE CATAPUM")
        self.geometry("1250x820")
        self.minsize(1050, 720)

        try:
            self.iconbitmap(str(RUTA_ICONO_APP))
        except Exception:
            log("No se pudo cargar el icono de la app")

        self.sensores = {}
        self.registro_telemetria = iniciar_telemetria()

        self.configurar_ventana()
        self.crear_interfaz()

        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)

        log("Aplicación iniciada correctamente")


    ######################
    # CONFIGURACIÓN VENTANA
    ######################

    def configurar_ventana(self):
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=0)  # Panel serial
        self.grid_rowconfigure(1, weight=1)  # Terminal + sensores


    ######################
    # CREAR INTERFAZ
    ######################

    def crear_interfaz(self):
        self.crear_panel_serial()
        self.crear_zona_datos()


    ######################
    # PANEL SERIAL
    ######################

    def crear_panel_serial(self):
        self.panel_serial = PanelSerial(
            self,
            sensores=self.sensores,
            registro=self.registro_telemetria
        )

        self.panel_serial.colocar(
            fila=0,
            columna=0,
            padx=20,
            pady=(20, 10),
            sticky="ew"
        )


    ######################
    # ZONA DATOS
    ######################

    def crear_zona_datos(self):
        """
        Crea la zona inferior de la aplicación.

        Distribución:
            [ Terminal ][ Sensores ]

        La terminal queda más estrecha que el panel de sensores.
        """

        self.zona_datos = CustomFrame(self, tipo="transparente")
        self.zona_datos.colocar(
            fila=1,
            columna=0,
            padx=20,
            pady=(10, 20),
            sticky="nsew"
        )

        self.zona_datos.grid_rowconfigure(0, weight=1)
        self.zona_datos.grid_columnconfigure(0, weight=1)  # Terminal más estrecha
        self.zona_datos.grid_columnconfigure(1, weight=2)  # Sensores más ancho

        self.crear_terminal(
            master=self.zona_datos,
            fila=0,
            columna=0,
            padx=(0, 10),
            pady=0
        )

        self.crear_panel_sensores(
            master=self.zona_datos,
            fila=0,
            columna=1,
            padx=(10, 0),
            pady=0
        )


    ######################
    # SENSORES
    ######################

    def crear_panel_sensores(
        self,
        master,
        fila: int = 0,
        columna: int = 0,
        padx=0,
        pady=0
    ):
        self.panel_sensores = CustomFrame(master, tipo="panel")

        self.panel_sensores.colocar(
            fila=fila,
            columna=columna,
            padx=padx,
            pady=pady,
            sticky="nsew"
        )

        self.panel_sensores.grid_columnconfigure(0, weight=1)
        self.panel_sensores.grid_rowconfigure(1, weight=1)

        titulo = ctk.CTkLabel(
            self.panel_sensores,
            text="Sensores",
            font=fuente("subtitulo"),
            text_color=color_texto("subtitulo")
        )
        titulo.grid(
            row=0,
            column=0,
            padx=20,
            pady=(18, 6),
            sticky="w"
        )

        self.scroll_sensores = CustomScrollableFrame(
            self.panel_sensores,
            tipo="transparente",
            scrollbar="azul"
        )
        self.scroll_sensores.colocar(
            fila=1,
            columna=0,
            padx=10,
            pady=(4, 16),
            sticky="nsew"
        )

        self._crear_sensores_desde_config()


    def _crear_sensores_desde_config(self):
        """
        Crea los sensores visuales a partir de SENSORES_TELEMETRIA.

        Importante:
        - El orden de SENSORES_TELEMETRIA es el orden del mensaje recibido por serial.
        - Cada sensor puede tener su propio icono usando ruta_icono.
        - Cada clave se guarda en self.sensores para poder actualizarla desde core.py.
        """

        numero_columnas = 2

        for columna in range(numero_columnas):
            self.scroll_sensores.grid_columnconfigure(columna, weight=1)

        for indice, config_sensor in enumerate(SENSORES_TELEMETRIA):
            clave = config_sensor["clave"]
            fila = indice // numero_columnas
            columna = indice % numero_columnas

            self.sensores[clave] = Sensor(
                self.scroll_sensores,
                texto=config_sensor["texto"],
                ruta_icono=config_sensor.get("ruta_icono", RUTA_ICONO_SENSOR_1),
                tipo_variable=config_sensor.get("tipo_variable", "float"),
                valor_inicial=config_sensor.get("valor_inicial", 0.0),
                decimales=config_sensor.get("decimales", 3)
            )

            self.sensores[clave].colocar(
                fila=fila,
                columna=columna,
                padx=10,
                pady=8,
                sticky="ew"
            )


    ######################
    # TERMINAL
    ######################

    def crear_terminal(
        self,
        master,
        fila: int = 0,
        columna: int = 0,
        padx=0,
        pady=0
    ):
        self.terminal = TerminalFrame(
            master,
            titulo="Terminal",
            intervalo_ms=100,
            max_lineas=500
        )

        self.terminal.colocar(
            fila=fila,
            columna=columna,
            padx=padx,
            pady=pady,
            sticky="nsew"
        )


    ######################
    # CIERRE
    ######################

    def cerrar_app(self):
        try:
            self.panel_serial.cerrar_recursos()
        except Exception as e:
            log(f"Error al cerrar recursos serial: {e}")

        self.destroy()


######################
# LANZAR APP
######################

def lanzar_app():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()
