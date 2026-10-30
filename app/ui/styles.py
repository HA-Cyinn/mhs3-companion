
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#101216"
CARD = "#191c22"
BORDER = "#2b3038"
TEXT_MUTED = "#9aa3af"

TYPE_COLORS = {
    "power": "#ef4444",
    "technical": "#22c55e",
    "speed": "#3b82f6",
}

TYPE_ICONS = {
    "power": "🔴",
    "technical": "🟢",
    "speed": "🔵",
}

CREDIT_TEXT = (
    "Projet de fan non officiel. Données et images : Game8. "
    "Monster Hunter Stories 3 © CAPCOM."
)


def credit_label(parent):
    return ctk.CTkLabel(parent, text=CREDIT_TEXT, text_color=TEXT_MUTED,
                        font=ctk.CTkFont(size=11), wraplength=600)
