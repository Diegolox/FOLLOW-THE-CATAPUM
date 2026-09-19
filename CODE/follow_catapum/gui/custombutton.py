import customtkinter as ctk
from follow_catapum.gui.estilos import fuente, color_texto

class CustomButton(ctk.CTkButton):
    """
    Botón minimalista reutilizable para CustomTkinter.
    Se adapta automáticamente al modo claro/oscuro.
    """

    def __init__(
        self,
        master,
        text: str = "Botón",
        tipo: str = "normal",
        width: int = 140,
        height: int = 38,
        radius: int = 12,
        command=None,
        **kwargs
    ):
        colores = self._obtener_colores(tipo)

        super().__init__(
            master,
            text=text,
            width=width,
            height=height,
            corner_radius=radius,
            command=command,
            font=fuente("boton"),
            fg_color=colores["fg"],
            hover_color=colores["hover"],
            text_color=colores["text"],
            border_color=colores["border"],
            border_width=colores["border_width"],
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
                "fg": ("#E5E7EB", "#2A2A2A"),
                "hover": ("#D1D5DB", "#3A3A3A"),
                "text": ("#111827", "#F9FAFB"),
                "border": ("#D1D5DB", "#3F3F46"),
                "border_width": 1,
            },
            "principal": {
                "fg": ("#2563EB", "#3B82F6"),
                "hover": ("#1D4ED8", "#2563EB"),
                "text": "#FFFFFF",
                "border": ("#2563EB", "#3B82F6"),
                "border_width": 0,
            },
            "secundario": {
                "fg": ("#FFFFFF", "#1F1F1F"),
                "hover": ("#F3F4F6", "#2D2D2D"),
                "text": ("#111827", "#F9FAFB"),
                "border": ("#D1D5DB", "#3F3F46"),
                "border_width": 1,
            },
            "peligro": {
                "fg": ("#DC2626", "#EF4444"),
                "hover": ("#B91C1C", "#DC2626"),
                "text": "#FFFFFF",
                "border": ("#DC2626", "#EF4444"),
                "border_width": 0,
            },
            "transparente": {
                "fg": "transparent",
                "hover": ("#E5E7EB", "#2A2A2A"),
                "text": ("#111827", "#F9FAFB"),
                "border": ("#D1D5DB", "#3F3F46"),
                "border_width": 1,
            },
        }

        return estilos.get(tipo, estilos["normal"])

    def colocar(self, fila=0, columna=0, padx=10, pady=10, sticky="ew", **kwargs):
        """
        Atajo cómodo para colocar el botón con grid.
        """
        self.grid(
            row=fila,
            column=columna,
            padx=padx,
            pady=pady,
            sticky=sticky,
            **kwargs
        )