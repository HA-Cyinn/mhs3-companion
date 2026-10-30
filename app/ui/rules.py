import customtkinter as ctk
from .styles import TYPE_COLORS, TYPE_ICONS, credit_label


class RulesPage(ctk.CTkFrame):
    def __init__(self, parent, on_back):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkButton(self, text="← Retour", width=90, command=on_back).pack(
            anchor="w", padx=20, pady=(18, 8)
        )
        ctk.CTkLabel(
            self, text="Mécanique des counters",
            font=ctk.CTkFont(size=26, weight="bold"),
        ).pack(anchor="w", padx=25, pady=(10, 20))

        rules = [("power", "speed"), ("speed", "technical"), ("technical", "power")]
        for source, counter in rules:
            frame = ctk.CTkFrame(self, fg_color="#191c22", corner_radius=12)
            frame.pack(fill="x", padx=25, pady=7)
            ctk.CTkLabel(
                frame, text=f"{TYPE_ICONS[source]}  {source.upper()}",
                text_color=TYPE_COLORS[source],
                font=ctk.CTkFont(size=17, weight="bold"),
            ).pack(side="left", padx=18, pady=15)
            ctk.CTkLabel(frame, text="→ contre →", text_color="#9aa3af").pack(side="left")
            ctk.CTkLabel(
                frame, text=f"{TYPE_ICONS[counter]}  {counter.upper()}",
                text_color=TYPE_COLORS[counter],
                font=ctk.CTkFont(size=17, weight="bold"),
            ).pack(side="left", padx=18)

        credit_label(self).pack(pady=(18, 10))
