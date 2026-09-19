import customtkinter as ctk


class CustomScrollableFrame(ctk.CTkScrollableFrame):
    """
    Frame escrollable minimalista reutilizable para CustomTkinter.

    Es equivalente a CustomFrame, pero con scroll vertical.
    Se adapta automáticamente al modo claro/oscuro usando tuplas de color.
    """

    def __init__(
        self,
        master,
        tipo: str = "normal",
        padding: int = 16,
        radius: int = 16,
        scrollbar: str = "normal",
        orientation: str = "vertical",
        **kwargs
    ):
        self.tipo = tipo
        self.padding = padding
        self.scrollbar = scrollbar

        colores = self._obtener_colores(tipo)
        colores_scrollbar = self._obtener_colores_scrollbar(scrollbar)

        super().__init__(
            master,
            fg_color=colores["fg"],
            border_color=colores["border"],
            border_width=colores["border_width"],
            corner_radius=radius,
            scrollbar_fg_color=colores_scrollbar["fg"],
            scrollbar_button_color=colores_scrollbar["button"],
            scrollbar_button_hover_color=colores_scrollbar["button_hover"],
            orientation=orientation,
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
                "fg": ("#F5F5F5", "#1E1E1E"),
                "border": ("#DDDDDD", "#2E2E2E"),
                "border_width": 1,
            },
            "panel": {
                "fg": ("#FFFFFF", "#242424"),
                "border": ("#DADADA", "#333333"),
                "border_width": 1,
            },
            "transparente": {
                "fg": "transparent",
                "border": ("#DDDDDD", "#333333"),
                "border_width": 0,
            },
            "destacado": {
                "fg": ("#EEF3FF", "#1F2937"),
                "border": ("#CBD5E1", "#374151"),
                "border_width": 1,
            },
        }

        return estilos.get(tipo, estilos["normal"])

    def _obtener_colores_scrollbar(self, tipo: str) -> dict:
        """
        Devuelve colores para la barra de scroll.
        """

        estilos = {
            "normal": {
                "fg": ("#F5F5F5", "#1E1E1E"),
                "button": ("#D1D5DB", "#3A3A3A"),
                "button_hover": ("#9CA3AF", "#4B5563"),
            },
            "suave": {
                "fg": ("#FFFFFF", "#242424"),
                "button": ("#E5E7EB", "#2A2A2A"),
                "button_hover": ("#D1D5DB", "#3A3A3A"),
            },
            "azul": {
                "fg": ("#EEF3FF", "#1F2937"),
                "button": ("#93C5FD", "#2563EB"),
                "button_hover": ("#60A5FA", "#1D4ED8"),
            },
        }

        return estilos.get(tipo, estilos["normal"])

    def colocar(self, fila=0, columna=0, padx=10, pady=10, sticky="nsew", **kwargs):
        """
        Atajo cómodo para usar grid.
        """
        self.grid(
            row=fila,
            column=columna,
            padx=padx,
            pady=pady,
            sticky=sticky,
            **kwargs
        )

    def configurar_grid(self, filas=None, columnas=None):
        """
        Permite configurar expansión interna del frame fácilmente.
        """

        if filas is not None:
            for fila in filas:
                self.grid_rowconfigure(fila, weight=1)

        if columnas is not None:
            for columna in columnas:
                self.grid_columnconfigure(columna, weight=1)
