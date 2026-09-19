# ============================================================
# CÓMO ACTUALIZAR UN SENSOR DESDE app.py U OTRO FICHERO
# ============================================================
#
# Cada sensor tiene la función:
#
#     sensor.actualizar_valor(nuevo_valor)
#
# Ejemplo:
#
#     self.sensores["sensor_1"].actualizar_valor(23.456)
#     self.sensores["sensor_2"].actualizar_valor(128)
#     self.sensores["sensor_3"].actualizar_valor(255)
#
# Si los sensores están guardados en un diccionario:
#
#     self.sensores = {}
#
# Entonces se pueden actualizar desde cualquier función de app.py:
#
#     def actualizar_sensores(self):
#         self.sensores["sensor_1"].actualizar_valor(12.345)
#         self.sensores["sensor_2"].actualizar_valor(50)
#         self.sensores["sensor_3"].actualizar_valor(1)
#
# También se pueden actualizar desde otro fichero externo pasando
# el diccionario de sensores como entrada:
#
#     def actualizar_desde_fuera(sensores):
#         sensores["sensor_1"].actualizar_valor(98.765)
#         sensores["sensor_2"].actualizar_valor(200)
#         sensores["sensor_3"].actualizar_valor(0)
#
# Importante:
# - Si el sensor es tipo "float", se mostrará con los decimales indicados.
# - Si el sensor es tipo "int", se mostrará como número entero.
# - Si el sensor es tipo "byte", se limitará entre 0 y 255.
# - Si el sensor es tipo "bool", se mostrará como ON/OFF.
# ============================================================

from pathlib import Path

import customtkinter as ctk
from PIL import Image
from follow_catapum.gui.estilos import fuente, color_texto

class Sensor(ctk.CTkFrame):
    """
    Sensor visual minimalista para CustomTkinter.

    Formato:
    [icono.ico]  SENSOR_1 : 000.000
    """

    def __init__(
        self,
        master,
        texto: str,
        ruta_icono,
        tipo_variable: str = "float",
        valor_inicial=0,
        decimales: int = 3,
        ancho_icono: int = 24,
        alto_icono: int = 24,
        width: int = 260,
        height: int = 46,
        **kwargs
    ):
        super().__init__(
            master,
            width=width,
            height=height,
            corner_radius=12,
            fg_color=("#F5F5F5", "#1F1F1F"),
            border_color=("#DDDDDD", "#333333"),
            border_width=1,
            **kwargs
        )

        self.texto = texto
        self.ruta_icono = Path(ruta_icono)
        self.tipo_variable = tipo_variable
        self.decimales = decimales
        self.valor = valor_inicial

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        self.imagen_icono = self._cargar_icono(ancho_icono, alto_icono)

        self.label_icono = ctk.CTkLabel(
            self,
            text="",
            image=self.imagen_icono,
            width=32
        )
        self.label_icono.grid(row=0, column=0, padx=(12, 8), pady=8)

        self.label_texto = ctk.CTkLabel(
            self,
            text=f"{self.texto} :",
            anchor="w",
            font=fuente("sensor_texto"),
            text_color=color_texto("sensor_texto")
        )
        self.label_texto.grid(row=0, column=1, padx=6, pady=8, sticky="ew")

        self.label_valor = ctk.CTkLabel(
            self,
            text=self._formatear_valor(valor_inicial),
            width=90,
            anchor="e",
            font=fuente("sensor_valor"),
            text_color=color_texto("sensor_valor")
        )
        self.label_valor.grid(row=0, column=2, padx=(6, 12), pady=8)

    def _cargar_icono(self, ancho: int, alto: int):
        """
        Carga un archivo .ico como imagen compatible con CustomTkinter.
        """

        if not self.ruta_icono.exists():
            print(f"ERROR: No existe el icono: {self.ruta_icono}")
            return None

        imagen = Image.open(self.ruta_icono)

        return ctk.CTkImage(
            light_image=imagen,
            dark_image=imagen,
            size=(ancho, alto)
        )

    def _formatear_valor(self, valor) -> str:
        """
        Convierte el valor al formato visual según el tipo de variable.
        """

        try:
            if self.tipo_variable == "float":
                return f"{float(valor):.{self.decimales}f}"

            if self.tipo_variable == "int":
                return f"{int(valor)}"

            if self.tipo_variable == "byte":
                valor = int(valor)
                valor = max(0, min(255, valor))
                return f"{valor}"

            if self.tipo_variable == "bool":
                return "ON" if bool(valor) else "OFF"

            if self.tipo_variable == "str":
                return str(valor)

            return str(valor)

        except Exception:
            return "ERROR"

    def actualizar_valor(self, nuevo_valor):
        """
        Actualiza el valor mostrado por el sensor.

        Uso:
            sensor.actualizar_valor(23.456)

        Ejemplo con diccionario:
            self.sensores["sensor_1"].actualizar_valor(23.456)
        """
        self.valor = nuevo_valor
        self.label_valor.configure(text=self._formatear_valor(nuevo_valor))

    def cambiar_texto(self, nuevo_texto: str):
        """
        Cambia el texto fijo del sensor.
        """
        self.texto = nuevo_texto
        self.label_texto.configure(text=f"{self.texto} :")

    def cambiar_icono(self, nueva_ruta_icono, ancho: int = 24, alto: int = 24):
        """
        Cambia el icono del sensor.
        """
        self.ruta_icono = Path(nueva_ruta_icono)
        self.imagen_icono = self._cargar_icono(ancho, alto)
        self.label_icono.configure(image=self.imagen_icono)

    def colocar(self, fila=0, columna=0, padx=10, pady=6, sticky="ew", **kwargs):
        """
        Atajo cómodo para colocar el sensor con grid.
        """
        self.grid(
            row=fila,
            column=columna,
            padx=padx,
            pady=pady,
            sticky=sticky,
            **kwargs
        )