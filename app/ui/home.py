import queue

import customtkinter as ctk
from app.core.data import load_monsters
from app.core.images import load_image_async
from .monster import MonsterPage
from .rules import RulesPage
from .styles import TYPE_COLORS


class HomePage(ctk.CTk):
    """Single application window. Pages are frames, never extra windows."""
    def __init__(self):
        super().__init__()
        self.title("MHS3 Companion")
        self.geometry("1000x760")
        self.minsize(720, 600)
        self.monsters = load_monsters()
        self.current_page = None
        self._images = {}
        self._history = []
        self._rules_page = None
        # Worker threads must not touch Tk (the mainloop may not be running yet);
        # they queue UI updates that the main thread drains.
        self._ui_queue = queue.Queue()
        self._drain_ui_queue()
        self._home_page = self._build_home()
        self._show(self._home_page)

    def _drain_ui_queue(self):
        try:
            for _ in range(10):
                self._ui_queue.get_nowait()()
        except queue.Empty:
            pass
        self.after(30, self._drain_ui_queue)

    # --- Navigation -------------------------------------------------------
    def _show(self, page):
        """Pack the new page first, then hide the old one, to avoid a blank flash."""
        old = self.current_page
        page.pack(fill="both", expand=True)
        self.current_page = page
        if old is not None and old is not page:
            old.pack_forget()
            if old not in (self._home_page, self._rules_page):
                old.destroy()

    def navigate(self, page):
        self._history.append(self.current_page)
        self._show(page)

    def back(self):
        if self._history:
            self._show(self._history.pop())

    def show_home(self):
        self._history.clear()
        self._show(self._home_page)

    def show_monster(self, monster):
        self.navigate(MonsterPage(self, monster, self.back))

    def show_rules(self):
        if self._rules_page is None:
            self._rules_page = RulesPage(self, self.back)
        self.navigate(self._rules_page)

    # --- Home page (built once, kept in memory) ----------------------------
    def _build_home(self):
        page = ctk.CTkFrame(self, fg_color="#101216")

        header = ctk.CTkFrame(page, fg_color="transparent")
        header.pack(fill="x", padx=28, pady=(22, 8))
        ctk.CTkLabel(header, text="MHS3", text_color="#2da8ff",
                     font=ctk.CTkFont(size=30, weight="bold")).pack(side="left")
        ctk.CTkLabel(header, text=" Companion", font=ctk.CTkFont(size=30, weight="bold")).pack(side="left")
        ctk.CTkButton(header, text="❓ Counters", width=120, command=self.show_rules).pack(side="right")

        ctk.CTkLabel(page, text="Ton pense-bête de combat", text_color="#9aa3af",
                     font=ctk.CTkFont(size=14)).pack(anchor="w", padx=31, pady=(0, 14))

        search = ctk.CTkEntry(page, placeholder_text="🔎  Rechercher un monstre...", height=46,
                              corner_radius=12)
        search.pack(fill="x", padx=25, pady=(0, 18))

        list_frame = ctk.CTkScrollableFrame(page, label_text=f"Monstres  •  {len(self.monsters)}",
                                            label_font=ctk.CTkFont(size=15, weight="bold"))
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 18))

        rows = []  # (monster, row frame), built once and only shown/hidden when filtering
        empty_label = ctk.CTkLabel(list_frame, text="Aucun monstre trouvé.", text_color="#9aa3af")

        def build_rows(monsters):
            for monster in monsters:
                row = ctk.CTkFrame(list_frame, fg_color="#191c22", corner_radius=14, height=92)
                row.pack(fill="x", padx=5, pady=5)
                rows.append((monster, row))
                row.grid_propagate(False)
                row.grid_columnconfigure(0, weight=0)  # image
                row.grid_columnconfigure(1, weight=1)  # nom + élément
                row.grid_columnconfigure(2, weight=0)  # attaque → contre
                row.grid_columnconfigure(3, weight=0)  # bouton

                image_label = ctk.CTkLabel(row, text="", width=105, height=82)
                image_label.grid(
                    row=0,
                    column=0,
                    rowspan=2,
                    padx=(12, 8),
                    pady=5
                )

                info = ctk.CTkFrame(row, fg_color="transparent")
                info.grid(row=0, column=1, sticky="nsew", padx=(5, 8), pady=(10, 4))
                ctk.CTkLabel(info, text=monster.name,
                             font=ctk.CTkFont(size=17, weight="bold")).pack(anchor="w")
                ctk.CTkLabel(info, text=monster.element, text_color="#9aa3af",
                             font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(1, 3))

                # Quick combat reminder: keep attack → counter together in one block.
                known = next((s for s in monster.states if s.counter), None)
                if known:
                    combat = ctk.CTkFrame(row, fg_color="transparent")
                    combat.grid(
                        row=0,
                        column=2,
                        rowspan=2,
                        padx=(10, 15),
                        pady=10
                    )

                    ctk.CTkLabel(
                        combat,
                        text=known.attack_type.upper(),
                        text_color=TYPE_COLORS.get(known.attack_type, "#9aa3af"),
                        font=ctk.CTkFont(size=11, weight="bold")
                    ).pack(side="left")

                    ctk.CTkLabel(
                        combat,
                        text="→",
                        font=ctk.CTkFont(size=16, weight="bold")
                    ).pack(side="left", padx=8)

                    ctk.CTkLabel(
                        combat,
                        text=known.counter.upper(),
                        text_color=TYPE_COLORS.get(known.counter, "#9aa3af"),
                        font=ctk.CTkFont(size=12, weight="bold")
                    ).pack(side="left")

                # One single Voir button, regardless of whether a counter exists.
                ctk.CTkButton(
                    row,
                    text="Voir",
                    width=84,
                    height=38,
                    command=lambda m=monster: self.show_monster(m)
                ).grid(
                    row=0,
                    column=3,
                    rowspan=2,
                    padx=(4, 14),
                    pady=10
                )

                if monster.image_url:
                    def ready(image, label=image_label, key=monster.name):
                        if image is None:
                            return
                        def update():
                            if not label.winfo_exists():
                                return
                            self._images[key] = ctk.CTkImage(light_image=image, dark_image=image, size=image.size)
                            label.configure(image=self._images[key], text="")
                        self._ui_queue.put(update)
                    load_image_async(monster.image_url, monster.name, (105, 78), ready)

        search_job = None

        def apply_filter():
            q = search.get().strip().lower()
            empty_label.pack_forget()
            for _, row in rows:
                row.pack_forget()
            visible = 0
            for monster, row in rows:
                if q in monster.name.lower():
                    row.pack(fill="x", padx=5, pady=5)
                    visible += 1
            if not visible:
                empty_label.pack(pady=30)

        def on_search(_event=None):
            # Debounce so fast typing does not re-layout the list on every key.
            nonlocal search_job
            if search_job is not None:
                self.after_cancel(search_job)
            search_job = self.after(150, apply_filter)

        search.bind("<KeyRelease>", on_search)
        build_rows(self.monsters)
        return page
