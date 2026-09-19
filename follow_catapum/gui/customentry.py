import json
from pathlib import Path

import customtkinter as ctk

from follow_catapum.gui.estilos import fuente, color_texto

class CustomEntry(ctk.CTkFrame):
    """
    Entrada de texto minimalista asociada a una variable de un JSON.

    Formato visual:
        TEXTO: [ entry ]

    Ejemplo de uso:
        entry_com = CustomEntry(
            master=frame,
            texto="Puerto COM",
            ruta_json=RUTA_CONFIG_APP,
            bloque="PARAMETROS_APP",
            variable="COM",
            tipo_variable="str"
        )

    Para guardar:
        entry_com.guardar_en_json()

    También guarda automáticamente al pulsar Enter.
    """

    def __init__(
        self,
        master,
        texto: str,
        ruta_json,
        bloque: str,
        variable: str,
        tipo_variable: str = "str",
        placeholder: str = "",
        width: int = 320,
        height: int = 44,
        radius: int = 12,
        guardar_al_perder_foco: bool = True,
        **kwargs
    ):
        super().__init__(
            master,
            width=width,
            height=height,
            corner_radius=radius,
            fg_color=("#F5F5F5", "#1F1F1F"),
            border_color=("#DDDDDD", "#333333"),
            border_width=1,
            **kwargs
        )

        self.texto = texto
        self.ruta_json = Path(ruta_json)
        self.bloque = bloque
        self.variable = variable
        self.tipo_variable = tipo_variable
        self.guardar_al_perder_foco = guardar_al_perder_foco

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.label = ctk.CTkLabel(
            self,
            text=f"{self.texto}:",
            font=fuente("entry_label"),
            text_color=color_texto("entry_label"),
            anchor="w"
        )
        self.label.grid(
            row=0,
            column=0,
            padx=(14, 8),
            pady=8,
            sticky="w"
        )

        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            fg_color=("#FFFFFF", "#111111"),
            text_color=color_texto("entry_texto"),
            border_color=("#D1D5DB", "#3F3F46"),
            border_width=1,
            corner_radius=8,
            font=fuente("entry_texto")
        )
        self.entry.grid(
            row=0,
            column=1,
            padx=(8, 14),
            pady=8,
            sticky="ew"
        )

        self.cargar_desde_json()

        self.entry.bind("<Return>", self._evento_guardar)
        self.entry.bind("<FocusOut>", self._evento_perder_foco)

    def _leer_json(self) -> dict:
        """
        Lee el JSON completo.
        Si no existe o está vacío, devuelve un diccionario vacío.
        """

        if not self.ruta_json.exists():
            return {}

        try:
            with open(self.ruta_json, "r", encoding="utf-8") as f:
                return json.load(f)

        except json.JSONDecodeError:
            print(f"ERROR: JSON mal formado: {self.ruta_json}")
            return {}

        except Exception as e:
            print(f"ERROR al leer JSON {self.ruta_json}: {e}")
            return {}

    def _guardar_json(self, data: dict):
        """
        Guarda el JSON completo con indentación.
        """

        try:
            self.ruta_json.parent.mkdir(parents=True, exist_ok=True)

            with open(self.ruta_json, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"ERROR al guardar JSON {self.ruta_json}: {e}")

    def _convertir_tipo(self, valor_texto: str):
        """
        Convierte el texto del entry al tipo indicado.
        """

        try:
            if self.tipo_variable == "str":
                return str(valor_texto)

            if self.tipo_variable == "int":
                return int(valor_texto)

            if self.tipo_variable == "float":
                return float(valor_texto)

            if self.tipo_variable == "bool":
                texto = str(valor_texto).strip().lower()

                if texto in ["true", "1", "yes", "si", "sí", "on"]:
                    return True

                if texto in ["false", "0", "no", "off"]:
                    return False

                raise ValueError("Booleano no válido")

            if self.tipo_variable == "byte":
                valor = int(valor_texto)
                return max(0, min(255, valor))

            return valor_texto

        except Exception:
            print(
                f"ERROR: No se pudo convertir '{valor_texto}' "
                f"a tipo '{self.tipo_variable}'"
            )
            return None

    def _formatear_para_entry(self, valor) -> str:
        """
        Convierte el valor leído del JSON a texto para mostrarlo en el entry.
        """

        if valor is None:
            return ""

        if isinstance(valor, bool):
            return "true" if valor else "false"

        return str(valor)

    def cargar_desde_json(self):
        """
        Carga el valor desde el JSON y lo muestra en el entry.
        """

        data = self._leer_json()

        valor = (
            data
            .get(self.bloque, {})
            .get(self.variable, "")
        )

        self.entry.delete(0, "end")
        self.entry.insert(0, self._formatear_para_entry(valor))

    def guardar_en_json(self):
        """
        Guarda el valor actual del entry en el JSON asociado.
        """

        valor_texto = self.entry.get()
        valor_convertido = self._convertir_tipo(valor_texto)

        if valor_convertido is None:
            return False

        data = self._leer_json()

        if self.bloque not in data:
            data[self.bloque] = {}

        data[self.bloque][self.variable] = valor_convertido

        self._guardar_json(data)

        return True

    def obtener_valor(self):
        """
        Devuelve el valor actual del entry convertido al tipo indicado.
        """

        return self._convertir_tipo(self.entry.get())

    def cambiar_valor(self, nuevo_valor, guardar: bool = False):
        """
        Cambia el valor visual del entry.
        Si guardar=True, también lo guarda en el JSON.
        """

        self.entry.delete(0, "end")
        self.entry.insert(0, str(nuevo_valor))

        if guardar:
            self.guardar_en_json()

    def cambiar_texto(self, nuevo_texto: str):
        """
        Cambia el texto fijo de la izquierda.
        """

        self.texto = nuevo_texto
        self.label.configure(text=f"{self.texto}:")

    def _evento_guardar(self, event=None):
        """
        Guarda al pulsar Enter.
        """

        self.guardar_en_json()

    def _evento_perder_foco(self, event=None):
        """
        Guarda al salir del entry si está activado.
        """

        if self.guardar_al_perder_foco:
            self.guardar_en_json()

    def colocar(self, fila=0, columna=0, padx=10, pady=6, sticky="ew", **kwargs):
        """
        Atajo cómodo para colocar el entry con grid.
        """

        self.grid(
            row=fila,
            column=columna,
            padx=padx,
            pady=pady,
            sticky=sticky,
            **kwargs
        )