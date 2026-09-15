import customtkinter as ctk
from app.core.monster import Monster
from app.core.images import load_image_async
from .styles import TYPE_COLORS, TYPE_ICONS


class TypeBox(ctk.CTkFrame):
    def __init__(self, parent, title, attack_type, highlighted=False):
        super().__init__(
            parent, fg_color="#11161d", border_width=2 if highlighted else 1,
            border_color=TYPE_COLORS.get(attack_type, "#2b3038") if highlighted else "#2b3038",
            corner_radius=12,
        )
        ctk.CTkLabel(self, text=title, text_color="#9aa3af",
                     font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=12, pady=(11, 3))
        label = f"{TYPE_ICONS.get(attack_type, '❔')}  {attack_type.upper()}"
        ctk.CTkLabel(self, text=label, text_color=TYPE_COLORS.get(attack_type, "#9aa3af"),
                     font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=12, pady=(0, 12))


class MonsterPage(ctk.CTkFrame):
    def __init__(self, parent, monster: Monster, on_back):
        super().__init__(parent, fg_color="#101216")
        self.monster = monster
        self._images = {}

        ctk.CTkButton(self, text="←  Retour", width=95, fg_color="transparent",
                      hover_color="#191c22", command=on_back).pack(anchor="w", padx=20, pady=(16, 4))

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=18, pady=(0, 14))

        # Top area: compact monster card on the left, combat information on the right.
        top = ctk.CTkFrame(scroll, fg_color="transparent")
        top.pack(fill="x", padx=4, pady=5)
        top.grid_columnconfigure(0, weight=0)
        top.grid_columnconfigure(1, weight=1)

        monster_card = ctk.CTkFrame(top, fg_color="#151a21", corner_radius=16, width=220)
        monster_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        monster_card.grid_propagate(False)

        image_label = ctk.CTkLabel(monster_card, text="Image du monstre", width=120, height=90)
        image_label.pack(pady=(16, 8))

        ctk.CTkLabel(
            monster_card,
            text=monster.name,
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="center",
        ).pack(fill="x", padx=12, pady=(0, 2))
        ctk.CTkLabel(
            monster_card,
            text=monster.element,
            text_color="#9aa3af",
            font=ctk.CTkFont(size=14),
            anchor="center",
        ).pack(fill="x", padx=12, pady=(0, 16))

        if monster.image_url:
            def ready(image):
                if image is None:
                    return
                def update():
                    if not image_label.winfo_exists():
                        return
                    self._images["hero"] = ctk.CTkImage(
                        light_image=image,
                        dark_image=image,
                        size=(120, 90),
                    )
                    image_label.configure(image=self._images["hero"], text="")
                self.after(0, update)
            load_image_async(monster.image_url, monster.name + "_hero", (120, 90), ready)

        self._build_combat_panel(top, column=1)
        self._build_resistances(scroll)

    def _build_combat_panel(self, parent, column):
        panel = ctk.CTkFrame(parent, fg_color="#151a21", corner_radius=16)
        panel.grid(row=0, column=column, sticky="nsew", padx=(8, 0))

        ctk.CTkLabel(
            panel,
            text="Attaque et contre principal",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(anchor="w", padx=16, pady=(15, 10))

        known = next((s for s in self.monster.states if s.counter), None)
        if known:
            types = ctk.CTkFrame(panel, fg_color="transparent")
            types.pack(fill="x", padx=12, pady=(0, 12))
            TypeBox(types, "TYPE D'ATTAQUE", known.attack_type).pack(
                side="left", fill="x", expand=True, padx=(0, 5)
            )
            ctk.CTkLabel(types, text="→", font=ctk.CTkFont(size=24, weight="bold")).pack(
                side="left", padx=8
            )
            TypeBox(types, "TON CONTRE", known.counter, highlighted=True).pack(
                side="left", fill="x", expand=True, padx=(5, 0)
            )

        ctk.CTkLabel(
            panel,
            text="Tous les états d'attaque",
            text_color="#d1d5db",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(anchor="w", padx=16, pady=(3, 6))

        for state in self.monster.states:
            row = ctk.CTkFrame(panel, fg_color="#1b222b", corner_radius=10)
            row.pack(fill="x", padx=12, pady=3)
            ctk.CTkLabel(
                row,
                text=state.name,
                anchor="w",
            ).pack(side="left", fill="x", expand=True, padx=12, pady=10)
            ctk.CTkLabel(
                row,
                text=state.attack_type.upper(),
                text_color=TYPE_COLORS.get(state.attack_type, "#9aa3af"),
                font=ctk.CTkFont(size=11, weight="bold"),
            ).pack(side="left", padx=8)
            ctk.CTkLabel(
                row,
                text="→",
                font=ctk.CTkFont(size=16, weight="bold"),
            ).pack(side="left", padx=4)
            ctk.CTkLabel(
                row,
                text=(state.counter or "—").upper(),
                text_color=TYPE_COLORS.get(state.counter, "#9aa3af") if state.counter else "#9aa3af",
                font=ctk.CTkFont(size=11, weight="bold"),
            ).pack(side="left", padx=(4, 12))

    def _build_resistances(self, parent):
        section = ctk.CTkFrame(parent, fg_color="#151a21", corner_radius=16)
        section.pack(fill="x", padx=4, pady=8)

        ctk.CTkLabel(
            section,
            text="Résistances",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(anchor="w", padx=16, pady=(15, 10))

        tables = ctk.CTkFrame(section, fg_color="transparent")
        tables.pack(fill="x", padx=12, pady=(0, 14))
        tables.grid_columnconfigure(0, weight=1, uniform="resistance")
        tables.grid_columnconfigure(1, weight=1, uniform="resistance")

        self._build_resistance_table(
            tables,
            column=0,
            title="🧪 Ailment Resistances",
            values=self.monster.resistances.get("ailment", {}),
            labels=[
                ("☠️", "Poison", "poison"),
                ("🔥", "Brûlure", "burn"),
                ("⚡", "Paralysie", "paralysis"),
                ("😴", "Sommeil", "sleep"),
                ("💥", "Fléau explosion", "blastblight"),
                ("🩸", "Saignement", "bleeding"),
                ("👁️", "Cécité", "darkness"),
            ],
        )

        self._build_resistance_table(
            tables,
            column=1,
            title="⚔️ Element Resistances",
            values=self.monster.resistances.get("element", {}),
            labels=[
                ("⚪", "Neutre", "neutral"),
                ("🔥", "Feu", "fire"),
                ("💧", "Eau", "water"),
                ("⚡", "Foudre", "thunder"),
                ("❄️", "Glace", "ice"),
                ("🐉", "Dragon", "dragon"),
            ],
        )

    def _build_resistance_table(self, parent, column, title, values, labels):
        table = ctk.CTkFrame(parent, fg_color="#11161d", corner_radius=12)
        table.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=(0 if column == 0 else 5, 5 if column == 0 else 0),
        )

        # 3 columns keep icons, names and values aligned independently.
        table.grid_columnconfigure(0, weight=0, minsize=28)
        table.grid_columnconfigure(1, weight=1)
        table.grid_columnconfigure(2, weight=0, minsize=110)

        ctk.CTkLabel(
            table,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        ).grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=12,
            pady=(11, 8),
        )

        level_labels = {
            "very_sensitive": "Très sensible",
            "sensitive": "Sensible",
            "normal": "Normal",
            "resistant": "Résistant",
            "very_resistant": "Très résistant",
            "unknown": "Inconnu",
        }

        for row_index, (icon, label, key) in enumerate(labels, start=1):
            value = level_labels.get(values.get(key, "unknown"), "Inconnu")

            ctk.CTkLabel(
                table,
                text=icon,
                anchor="center",
                width=28,
                font=ctk.CTkFont(size=12),
            ).grid(
                row=row_index,
                column=0,
                sticky="w",
                padx=(12, 0),
                pady=3,
            )

            ctk.CTkLabel(
                table,
                text=label,
                anchor="w",
                text_color="#d1d5db",
                font=ctk.CTkFont(size=12),
            ).grid(
                row=row_index,
                column=1,
                sticky="w",
                padx=(2, 8),
                pady=3,
            )

            ctk.CTkLabel(
                table,
                text=value,
                anchor="e",
                text_color="#ffffff" if value != "Inconnu" else "#9aa3af",
                font=ctk.CTkFont(size=12, weight="bold"),
            ).grid(
                row=row_index,
                column=2,
                sticky="e",
                padx=(4, 12),
                pady=3,
            )
