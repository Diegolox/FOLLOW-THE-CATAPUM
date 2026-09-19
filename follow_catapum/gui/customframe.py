import customtkinter as ctk


class CustomFrame(ctk.CTkFrame):
    """
    Frame minimalista reutilizable para CustomTkinter.
    Se adapta automáticamente al modo claro/oscuro usando tuplas de color.
    """

    def __init__(
        self,
        master,
        tipo: str = "normal",
        padding: int = 16,
        radius: int = 16,
        **kwargs
    ):
        self.tipo = tipo
        self.padding = padding

        colores = self._obtener_colores(tipo)

        super().__init__(
            master,
            fg_color=colores["fg"],
            border_color=colores["border"],
            border_width=colores["border_width"],
            corner_radius=radius,
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