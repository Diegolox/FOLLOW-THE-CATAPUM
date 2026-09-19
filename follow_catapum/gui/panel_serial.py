# ============================================================
# panel_serial.py
# Panel de control de comunicación serial y telemetría
# ============================================================

import customtkinter as ctk

from follow_catapum.rutas import RUTA_CONFIG_APP

from follow_catapum.gui.customframe import CustomFrame
from follow_catapum.gui.custombutton import CustomButton
from follow_catapum.gui.customentry import CustomEntry
from follow_catapum.gui.customswitch import CustomSwitch
from follow_catapum.gui.estilos import fuente, color_texto
from follow_catapum.gui.indicador_estado import IndicadorCircular

from follow_catapum.logica.logger import log
from follow_catapum.logica.estado_telemetria import EstadoTelemetria
from follow_catapum.logica.core import (
    listar_puertos_com,
    conectar_serial,
    desconectar_serial,
    serial_esta_conectado,
    leer_y_procesar_datos_esp32,
    finalizar_telemetria,
)


class PanelSerial(CustomFrame):
    """
    Panel de control de la comunicación serial.

    Responsabilidades:
    - Crear entrys y botones relacionados con serial.
    - Llamar al core.
    - Actualizar indicadores y contadores.
    - Cambiar entre modo claro y modo oscuro.
    """

    TIMEOUT_SERIAL = 1.0
    INTERVALO_LECTURA_MS = 100
    MODO_PRUEBA = False

    def __init__(
        self,
        master,
        sensores: dict,
        registro: list,
        **kwargs
    ):
        super().__init__(
            master,
            tipo="panel",
            **kwargs
        )

        self.sensores = sensores
        self.registro = registro
        self.estado = EstadoTelemetria()

        self._after_lectura = None
        self._after_estado = None

        self.crear_widgets()
        self.actualizar_estado_visual()

        self._programar_actualizacion_estado()


    # ========================================================
    # CREACIÓN INTERFAZ
    # ========================================================

    def crear_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)

        titulo = ctk.CTkLabel(
            self,
            text="Comunicación serial",
            font=fuente("titulo"),
            text_color=color_texto("titulo")
        )
        titulo.grid(
            row=0,
            column=0,
            padx=20,
            pady=(18, 8),
            sticky="w"
        )

        self.indicador_conexion = IndicadorCircular(
            self,
            texto="Conexión",
            color_inicial="rojo"
        )
        self.indicador_conexion.grid(
            row=0,
            column=1,
            padx=10,
            pady=(18, 8),
            sticky="e"
        )

        self.indicador_rx = IndicadorCircular(
            self,
            texto="RX",
            color_inicial="gris"
        )
        self.indicador_rx.grid(
            row=0,
            column=2,
            padx=10,
            pady=(18, 8),
            sticky="e"
        )

        self.switch_tema = CustomSwitch(
            self,
            text="Tema claro",
            tipo="normal",
            valor_inicial=False,
            command=self.cambiar_tema
        )
        self.switch_tema.grid(
            row=0,
            column=3,
            padx=(10, 20),
            pady=(18, 8),
            sticky="e"
        )

        self.crear_entrys_y_estado()
        self.crear_botones()


    def crear_entrys_y_estado(self):
        """
        Crea los entrys principales y los indicadores textuales.

        Layout:
            [ Puerto COM ] [ Baudrate ]              [ Estado | Muestras | Errores | Último dato ]
        """

        self.frame_entrys = CustomFrame(self, tipo="transparente")
        self.frame_entrys.grid(
            row=1,
            column=0,
            columnspan=4,
            padx=10,
            pady=4,
            sticky="ew"
        )

        self.frame_entrys.grid_columnconfigure(0, weight=0)
        self.frame_entrys.grid_columnconfigure(1, weight=0)
        self.frame_entrys.grid_columnconfigure(2, weight=1)

        self.entry_com = CustomEntry(
            self.frame_entrys,
            texto="Puerto COM",
            ruta_json=RUTA_CONFIG_APP,
            bloque="PARAMETROS_APP",
            variable="COM",
            tipo_variable="str",
            placeholder="COM3",
            width=410
        )
        self.entry_com.colocar(
            fila=0,
            columna=0,
            padx=(10, 8),
            pady=6,
            sticky="w"
        )

        self.entry_baudrate = CustomEntry(
            self.frame_entrys,
            texto="Baudrate",
            ruta_json=RUTA_CONFIG_APP,
            bloque="PARAMETROS_APP",
            variable="BAUDRATE",
            tipo_variable="int",
            placeholder="115200",
            width=360
        )
        self.entry_baudrate.colocar(
            fila=0,
            columna=1,
            padx=(8, 18),
            pady=6,
            sticky="w"
        )

        self.crear_estado_textual(
            master=self.frame_entrys,
            fila=0,
            columna=2
        )


    def crear_botones(self):
        self.frame_botones = CustomFrame(self, tipo="transparente")
        self.frame_botones.grid(
            row=2,
            column=0,
            columnspan=4,
            padx=10,
            pady=4,
            sticky="ew"
        )

        for columna in range(6):
            self.frame_botones.grid_columnconfigure(columna, weight=1)

        botones = [
            ("Listar puertos", "secundario", self.listar_puertos),
            ("Conectar", "principal", self.conectar),
            ("Desconectar", "secundario", self.desconectar),
            ("Iniciar telemetría", "principal", self.iniciar_lectura),
            ("Detener telemetría", "peligro", self.detener_lectura),
            ("Exportar datos", "secundario", self.exportar_datos),
        ]

        for columna, (texto, tipo, comando) in enumerate(botones):
            boton = CustomButton(
                self.frame_botones,
                text=texto,
                tipo=tipo,
                command=comando
            )
            boton.colocar(
                fila=0,
                columna=columna,
                padx=6,
                pady=8,
                sticky="ew"
            )


    def crear_estado_textual(self, master, fila: int, columna: int):
        """
        Crea los indicadores textuales en una sola fila.
        """

        self.frame_estado = CustomFrame(master, tipo="transparente")
        self.frame_estado.grid(
            row=fila,
            column=columna,
            padx=(20, 10),
            pady=6,
            sticky="e"
        )

        for columna_estado in range(4):
            self.frame_estado.grid_columnconfigure(columna_estado, weight=0)

        self.label_estado = ctk.CTkLabel(
            self.frame_estado,
            text="Estado: desconectado",
            font=fuente("normal"),
            text_color=color_texto("normal"),
            anchor="w"
        )
        self.label_estado.grid(
            row=0,
            column=0,
            padx=(8, 18),
            pady=4,
            sticky="w"
        )

        self.label_muestras = ctk.CTkLabel(
            self.frame_estado,
            text="Muestras: 0",
            font=fuente("normal"),
            text_color=color_texto("normal"),
            anchor="w"
        )
        self.label_muestras.grid(
            row=0,
            column=1,
            padx=(8, 18),
            pady=4,
            sticky="w"
        )

        self.label_errores = ctk.CTkLabel(
            self.frame_estado,
            text="Errores formato: 0",
            font=fuente("normal"),
            text_color=color_texto("normal"),
            anchor="w"
        )
        self.label_errores.grid(
            row=0,
            column=2,
            padx=(8, 18),
            pady=4,
            sticky="w"
        )

        self.label_ultimo_dato = ctk.CTkLabel(
            self.frame_estado,
            text="Último dato: --",
            font=fuente("normal"),
            text_color=color_texto("normal"),
            anchor="w"
        )
        self.label_ultimo_dato.grid(
            row=0,
            column=3,
            padx=(8, 8),
            pady=4,
            sticky="w"
        )


    # ========================================================
    # TEMA CLARO / OSCURO
    # ========================================================

    def cambiar_tema(self):
        """
        Cambia la apariencia global de CustomTkinter.

        Switch apagado  -> modo oscuro.
        Switch encendido -> modo claro.
        """

        if self.switch_tema.esta_activado():
            ctk.set_appearance_mode("light")
            log("Tema cambiado a modo claro.")
        else:
            ctk.set_appearance_mode("dark")
            log("Tema cambiado a modo oscuro.")


    # ========================================================
    # BOTONES
    # ========================================================

    def listar_puertos(self):
        listar_puertos_com()


    def conectar(self):
        puerto = self._leer_puerto()
        baudrate = self._leer_baudrate()
        timeout = self._leer_timeout()

        if puerto is None or baudrate is None or timeout is None:
            return

        ok = conectar_serial(
            puerto=puerto,
            baudrate=baudrate,
            timeout=timeout
        )

        if ok:
            self.estado.registrar_conexion(puerto, baudrate)
        else:
            self.estado.registrar_desconexion()

        self.actualizar_estado_visual()


    def desconectar(self):
        self.detener_lectura(exportar=False)

        desconectar_serial()
        self.estado.registrar_desconexion()

        self.actualizar_estado_visual()


    def leer_una_muestra(self):
        """
        Lee y procesa una única muestra.

        Se mantiene como función auxiliar, aunque ya no hay botón manual.
        """

        if not self._puede_leer():
            return

        resultado = leer_y_procesar_datos_esp32(
            sensores=self.sensores,
            registro=self.registro,
            modo_prueba=self.MODO_PRUEBA
        )

        self._gestionar_resultado_lectura(resultado)


    def iniciar_lectura(self):
        if not self._puede_leer():
            return

        if self.estado.leyendo:
            log("La telemetría ya está en marcha.")
            return

        self.estado.iniciar_lectura()

        log("Lectura de telemetría iniciada.")

        self._ciclo_lectura()
        self.actualizar_estado_visual()


    def detener_lectura(self, exportar: bool = True):
        if self._after_lectura is not None:
            try:
                self.after_cancel(self._after_lectura)
            except Exception:
                pass

            self._after_lectura = None

        if self.estado.leyendo:
            log("Lectura de telemetría detenida.")

        self.estado.detener_lectura()

        if exportar:
            self.exportar_datos()

        self.actualizar_estado_visual()


    def exportar_datos(self):
        finalizar_telemetria(self.registro)


    # ========================================================
    # CICLOS PERIÓDICOS
    # ========================================================

    def _ciclo_lectura(self):
        if not self.estado.leyendo:
            return

        resultado = leer_y_procesar_datos_esp32(
            sensores=self.sensores,
            registro=self.registro,
            modo_prueba=self.MODO_PRUEBA
        )

        self._gestionar_resultado_lectura(resultado)

        intervalo = self._leer_intervalo_ms()

        self._after_lectura = self.after(
            intervalo,
            self._ciclo_lectura
        )


    def _programar_actualizacion_estado(self):
        self.actualizar_estado_visual()

        self._after_estado = self.after(
            500,
            self._programar_actualizacion_estado
        )


    # ========================================================
    # RESULTADOS / ESTADOS
    # ========================================================

    def _gestionar_resultado_lectura(self, resultado: dict):
        if resultado.get("ok"):
            self.estado.registrar_muestra_valida()
            self.indicador_rx.pulso_azul()
            self._log_muestras_periodicamente()
            self.actualizar_estado_visual()
            return

        tipo_error = resultado.get("tipo_error")

        if tipo_error == "sin_datos":
            self.actualizar_estado_visual()
            return

        if tipo_error in ["json", "formato"]:
            self.estado.registrar_error_json()

        self.indicador_rx.pulso_rojo()
        self.actualizar_estado_visual()


    def actualizar_estado_visual(self):
        self.estado.conectado = serial_esta_conectado()

        segundos = self.estado.segundos_desde_ultimo_dato()

        if not self.estado.conectado:
            self.indicador_conexion.poner_rojo()

        elif segundos is not None and segundos < 1.5:
            self.indicador_conexion.poner_verde()

        else:
            self.indicador_conexion.poner_ambar()

        if self.estado.leyendo:
            texto_estado = "Estado: leyendo"
        elif self.estado.conectado:
            texto_estado = "Estado: conectado"
        else:
            texto_estado = "Estado: desconectado"

        self.label_estado.configure(text=texto_estado)
        self.label_muestras.configure(
            text=f"Muestras: {self.estado.muestras_recibidas}"
        )
        self.label_errores.configure(
            text=f"Errores formato: {self.estado.errores_json}"
        )

        if segundos is None:
            self.label_ultimo_dato.configure(text="Último dato: --")
        else:
            self.label_ultimo_dato.configure(
                text=f"Último dato: hace {segundos:.1f} s"
            )


    def _log_muestras_periodicamente(self):
        muestras = self.estado.muestras_recibidas

        if muestras == 1:
            log("Primer dato válido recibido.")
        elif muestras % 100 == 0:
            log(f"{muestras} muestras válidas recibidas.")


    # ========================================================
    # VALIDACIONES / LECTURA ENTRYS
    # ========================================================

    def _puede_leer(self):
        if not self.estado.conectado:
            log("ERROR: No se puede leer. El puerto serie no está conectado.")
            return False

        return True


    def _leer_puerto(self):
        puerto = self.entry_com.obtener_valor()

        if puerto is None or str(puerto).strip() == "":
            log("ERROR: Debes indicar un puerto COM.")
            return None

        return str(puerto).strip()


    def _leer_baudrate(self):
        baudrate = self.entry_baudrate.obtener_valor()

        if baudrate is None:
            log("ERROR: Baudrate no válido.")
            return None

        return int(baudrate)


    def _leer_timeout(self):
        return self.TIMEOUT_SERIAL


    def _leer_intervalo_ms(self):
        return self.INTERVALO_LECTURA_MS


    # ========================================================
    # CIERRE
    # ========================================================

    def cerrar_recursos(self):
        self.detener_lectura(exportar=False)

        if self._after_estado is not None:
            try:
                self.after_cancel(self._after_estado)
            except Exception:
                pass

            self._after_estado = None

        desconectar_serial()
