import customtkinter as ctk


######################
# COLORES TEXTO
######################

COLOR_TEXTO = {
    "titulo": ("#111827", "#F9FAFB"),
    "subtitulo": ("#374151", "#E5E7EB"),
    "normal": ("#111827", "#F9FAFB"),
    "secundario": ("#6B7280", "#9CA3AF"),
    "boton": ("#111827", "#F9FAFB"),
    "boton_principal": "#FFFFFF",
    "entry": ("#111827", "#F9FAFB"),
    "sensor_texto": ("#111827", "#F9FAFB"),
    "sensor_valor": ("#111827", "#F9FAFB"),
    "terminal": ("#111827", "#E5E7EB"),
    "error": ("#DC2626", "#F87171"),
    "ok": ("#16A34A", "#22C55E"),
}


######################
# CONFIGURACIÓN TEXTOS
######################

TEXTOS = {
    "titulo": {
        "familia": "Arial",
        "tamano": 22,
        "negrita": True,
        "color": COLOR_TEXTO["titulo"],
    },
    "subtitulo": {
        "familia": "Arial",
        "tamano": 18,
        "negrita": True,
        "color": COLOR_TEXTO["subtitulo"],
    },
    "normal": {
        "familia": "Arial",
        "tamano": 14,
        "negrita": False,
        "color": COLOR_TEXTO["normal"],
    },
    "label": {
        "familia": "Arial",
        "tamano": 14,
        "negrita": True,
        "color": COLOR_TEXTO["normal"],
    },
    "boton": {
        "familia": "Arial",
        "tamano": 14,
        "negrita": True,
        "color": COLOR_TEXTO["boton"],
    },
    "switch": {
        "familia": "Arial",
        "tamano": 14,
        "negrita": False,
        "color": COLOR_TEXTO["normal"],
    },
    "entry_label": {
        "familia": "Arial",
        "tamano": 14,
        "negrita": True,
        "color": COLOR_TEXTO["normal"],
    },
    "entry_texto": {
        "familia": "Arial",
        "tamano": 14,
        "negrita": False,
        "color": COLOR_TEXTO["entry"],
    },
    "sensor_texto": {
        "familia": "Arial",
        "tamano": 14,
        "negrita": True,
        "color": COLOR_TEXTO["sensor_texto"],
    },
    "sensor_valor": {
        "familia": "Consolas",
        "tamano": 14,
        "negrita": False,
        "color": COLOR_TEXTO["sensor_valor"],
    },
    "terminal_titulo": {
        "familia": "Arial",
        "tamano": 15,
        "negrita": True,
        "color": COLOR_TEXTO["normal"],
    },
    "terminal": {
        "familia": "Consolas",
        "tamano": 13,
        "negrita": False,
        "color": COLOR_TEXTO["terminal"],
    },
}


######################
# FUNCIONES ESTILO
######################

def fuente(tipo: str = "normal"):
    estilo = TEXTOS.get(tipo, TEXTOS["normal"])
    peso = "bold" if estilo["negrita"] else "normal"

    return ctk.CTkFont(
        family=estilo["familia"],
        size=estilo["tamano"],
        weight=peso
    )


def color_texto(tipo: str = "normal"):
    estilo = TEXTOS.get(tipo, TEXTOS["normal"])
    return estilo["color"] 