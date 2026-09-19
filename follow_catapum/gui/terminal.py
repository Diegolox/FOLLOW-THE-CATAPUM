import customtkinter as ctk

from follow_catapum.logica.logger import Logger

from follow_catapum.gui.estilos import fuente, color_texto

class TerminalFrame(ctk.CTkFrame):
    """
    Terminal simple para mostrar mensajes de log en la interfaz.

    Lee mensajes desde Logger usando una cola thread-safe.
    Se actualiza automáticamente con after().
    Compatible con modo claro/oscuro de CustomTkinter.
    """

    def __init__(
        self,
        master,
        titulo: str = "Terminal",
        intervalo_ms: int = 100,
        max_lineas: int = 500,
        **kwargs
    ):
        super().__init__(
            master,
            corner_radius=12,
            fg_color=("#F5F5F5", "#1E1E1E"),
            border_color=("#DDDDDD", "#333333"),
            border_width=1,
            **kwargs
        )

        self.intervalo_ms = intervalo_ms
        self.max_lineas = max_lineas
        self.lineas_actuales = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.label_titulo = ctk.CTkLabel(
            self,
            text=titulo,
            font=fuente("terminal_titulo"),
            text_color=color_texto("terminal_titulo")
        )
        self.label_titulo.grid(
            row=0,
            column=0,
            padx=14,
            pady=(10, 4),
            sticky="w"
        )

        self.textbox = ctk.CTkTextbox(
            self,
            height=180,
            corner_radius=8,
            fg_color=("#FFFFFF", "#111111"),
            text_color=color_texto("terminal"),
            border_color=("#E5E7EB", "#2A2A2A"),
            border_width=1,
            font=fuente("terminal"),
            wrap="word"
        )
        self.textbox.grid(
            row=1,
            column=0,
            padx=12,
            pady=(4, 12),
            sticky="nsew"
        )

        self.textbox.configure(state="disabled")

        self._actualizar_terminal()

    def _actualizar_terminal(self):
        """
        Lee los mensajes pendientes y los muestra en la terminal.
        Esta función se ejecuta siempre en el hilo principal gracias a after().
        """

        mensajes = Logger.leer_logs()

        if mensajes:
            self.textbox.configure(state="normal")

            for mensaje in mensajes:
                self.textbox.insert("end", mensaje + "\n")
                self.lineas_actuales += 1

            self._limitar_lineas()
            self.textbox.see("end")
            self.textbox.configure(state="disabled")

        self.after(self.intervalo_ms, self._actualizar_terminal)

    def _limitar_lineas(self):
        """
        Evita que la terminal crezca infinitamente.
        Borra líneas antiguas si se supera max_lineas.
        """

        if self.lineas_actuales <= self.max_lineas:
            return

        exceso = self.lineas_actuales - self.max_lineas

        for _ in range(exceso):
            self.textbox.delete("1.0", "2.0")
            self.lineas_actuales -= 1

    def limpiar(self):
        """
        Limpia la terminal desde la interfaz.
        """

        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")
        self.lineas_actuales = 0

    def colocar(self, fila=0, columna=0, padx=10, pady=10, sticky="nsew", **kwargs):
        """
        Atajo cómodo para colocar la terminal con grid.
        """

        self.grid(
            row=fila,
            column=columna,
            padx=padx,
            pady=pady,
            sticky=sticky,
            **kwargs
        )