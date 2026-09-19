import customtkinter as ctk

from follow_catapum.gui.estilos import fuente, color_texto


class CustomSwitch(ctk.CTkSwitch):
    """
    Switch minimalista reutilizable para CustomTkinter.
    Se adapta automáticamente al modo claro/oscuro.
    """

    def __init__(
        self,
        master,
        text: str = "Switch",
        tipo: str = "normal",
        valor_inicial: bool = False,
        command=None,
        **kwargs
    ):
        self.variable = ctk.BooleanVar(value=valor_inicial)

        colores = self._obtener_colores(tipo)

        super().__init__(
            master,
            text=text,
            variable=self.variable,
            command=command,
            font=fuente("switch"),
            fg_color=colores["fg"],
            progress_color=colores["progress"],
            button_color=colores["button"],
            button_hover_color=colores["button_hover"],
            text_color=color_texto("switch"),
            **kwargs
        )

    def _obtener_colores(self, tipo: str) -> dict:
        """
        Devuelve colores compatibles con modo claro/oscuro.
        Formato:
        ("color claro", "color oscuro")
        """

        estilos = {
            "normal": {
                "fg": ("#D1D5DB", "#3A3A3A"),
                "progress": ("#2563EB", "#3B82F6"),
                "button": ("#FFFFFF", "#F9FAFB"),
                "button_hover": ("#F3F4F6", "#E5E7EB"),
            },
            "suave": {
                "fg": ("#E5E7EB", "#2A2A2A"),
                "progress": ("#93C5FD", "#1D4ED8"),
                "button": ("#FFFFFF", "#F9FAFB"),
                "button_hover": ("#F3F4F6", "#E5E7EB"),
            },
            "verde": {
                "fg": ("#D1D5DB", "#3A3A3A"),
                "progress": ("#16A34A", "#22C55E"),
                "button": ("#FFFFFF", "#F9FAFB"),
                "button_hover": ("#F3F4F6", "#E5E7EB"),
            },
            "peligro": {
                "fg": ("#D1D5DB", "#3A3A3A"),
                "progress": ("#DC2626", "#EF4444"),
                "button": ("#FFFFFF", "#F9FAFB"),
                "button_hover": ("#F3F4F6", "#E5E7EB"),
            },
        }

        return estilos.get(tipo, estilos["normal"])

    def colocar(self, fila=0, columna=0, padx=10, pady=10, sticky="w", **kwargs):
        """
        Atajo cómodo para colocar el switch con grid.
        """
        self.grid(
            row=fila,
            column=columna,
            padx=padx,
            pady=pady,
            sticky=sticky,
            **kwargs
        )

    def esta_activado(self) -> bool:
        """
        Devuelve True si el switch está activado.
        """
        return self.variable.get()

    def activar(self):
        """
        Activa el switch.
        """
        self.select()

    def desactivar(self):
        """
        Desactiva el switch.
        """
        self.deselect()