# ============================================================
# indicador_estado.py
# Indicador circular simple para estados visuales
# ============================================================

import customtkinter as ctk

from follow_catapum.gui.estilos import fuente, color_texto


class IndicadorCircular(ctk.CTkFrame):
    """
    Indicador circular basado en un carácter grande '●'.

    Uso:
        indicador.poner_rojo()
        indicador.poner_verde()
        indicador.pulso_azul()
    """

    COLORES = {
        "gris": ("#9CA3AF", "#6B7280"),
        "rojo": ("#DC2626", "#EF4444"),
        "verde": ("#16A34A", "#22C55E"),
        "ambar": ("#D97706", "#F59E0B"),
        "azul": ("#2563EB", "#3B82F6"),
    }

    def __init__(
        self,
        master,
        texto: str = "",
        color_inicial: str = "gris",
        **kwargs
    ):
        super().__init__(
            master,
            fg_color="transparent",
            **kwargs
        )

        self.color_actual = color_inicial
        self._after_pulso = None

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)

        self.label_texto = ctk.CTkLabel(
            self,
            text=texto,
            font=fuente("normal"),
            text_color=color_texto("normal")
        )
        self.label_texto.grid(row=0, column=0, padx=(0, 6), pady=0)

        self.label_circulo = ctk.CTkLabel(
            self,
            text="●",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color=self.COLORES[color_inicial]
        )
        self.label_circulo.grid(row=0, column=1, padx=0, pady=0)

    def poner_color(self, color: str):
        if color not in self.COLORES:
            color = "gris"

        self.color_actual = color
        self.label_circulo.configure(text_color=self.COLORES[color])

    def poner_gris(self):
        self.poner_color("gris")

    def poner_rojo(self):
        self.poner_color("rojo")

    def poner_verde(self):
        self.poner_color("verde")

    def poner_ambar(self):
        self.poner_color("ambar")

    def poner_azul(self):
        self.poner_color("azul")

    def pulso(self, color: str, duracion_ms: int = 150, color_final: str = "gris"):
        """
        Cambia temporalmente de color y después vuelve al color indicado.
        """

        if self._after_pulso is not None:
            try:
                self.after_cancel(self._after_pulso)
            except Exception:
                pass

        self.poner_color(color)

        self._after_pulso = self.after(
            duracion_ms,
            lambda: self.poner_color(color_final)
        )

    def pulso_azul(self, duracion_ms: int = 150):
        self.pulso("azul", duracion_ms, "gris")

    def pulso_rojo(self, duracion_ms: int = 400):
        self.pulso("rojo", duracion_ms, "gris")

    def colocar(self, fila=0, columna=0, padx=10, pady=6, sticky="w", **kwargs):
        self.grid(
            row=fila,
            column=columna,
            padx=padx,
            pady=pady,
            sticky=sticky,
            **kwargs
        )
