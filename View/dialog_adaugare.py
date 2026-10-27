"""Formular comun de adăugare/editare. View doar colectează și afișează date."""

from typing import Callable

import customtkinter as ctk

from Model.model import DatePiatra


class DialogAdaugarePiatra(ctk.CTkToplevel):
    TIPURI = {"Prețioasă": "Pretioasa", "Magmatică": "Magmatica", "Sedimentară": "Sedimentara"}
    ETICHETE_EXTRA = {
        "Pretioasa": "Carate (ct)",
        "Magmatica": "Temperatura de topire (°C)",
        "Sedimentara": "Porozitate (%)",
    }

    def __init__(
        self, master, on_salveaza: Callable[..., str | None],
        date_existente: DatePiatra | None = None,
    ) -> None:
        super().__init__(master)
        self._on_salveaza = on_salveaza
        self.title("Editează piatra" if date_existente else "Adaugă o piatră")
        self.geometry("470x600")
        self.minsize(440, 590)
        self.configure(fg_color="#171c27")
        self.transient(master)
        self.grid_columnconfigure(0, weight=1)
        self._campuri: dict[str, ctk.CTkEntry] = {}
        self._construieste_interfata()
        if date_existente is not None:
            self._completeaza(date_existente)
        self._actualizeaza_eticheta(self._tip.get())
        self.bind("<Return>", lambda _eveniment: self._salveaza())
        self.bind("<Escape>", lambda _eveniment: self.destroy())
        self.after(80, self._activeaza)

    def _construieste_interfata(self) -> None:
        ctk.CTkLabel(self, text=self.title(), font=("Arial", 23, "bold")).grid(
            row=0, column=0, padx=28, pady=(24, 16), sticky="w",
        )
        ctk.CTkLabel(self, text="Tip de piatră").grid(row=1, column=0, padx=28, sticky="w")
        self._tip = ctk.CTkOptionMenu(
            self, values=list(self.TIPURI), command=self._actualizeaza_eticheta,
        )
        self._tip.grid(row=2, column=0, padx=28, pady=(4, 12), sticky="ew")
        for index, (cheie, text) in enumerate((
            ("nume", "Nume"), ("duritate", "Duritate (Mohs, 1–10)"),
            ("densitate", "Densitate (g/cm³)"), ("extra", ""),
        )):
            eticheta = ctk.CTkLabel(self, text=text)
            eticheta.grid(row=3 + index * 2, column=0, padx=28, sticky="w")
            camp = ctk.CTkEntry(self, height=36)
            camp.grid(row=4 + index * 2, column=0, padx=28, pady=(4, 8), sticky="ew")
            self._campuri[cheie] = camp
            if cheie == "extra":
                self._eticheta_extra = eticheta
        self._eroare = ctk.CTkLabel(self, text="", text_color="#ffb2bc", wraplength=390)
        self._eroare.grid(row=11, column=0, padx=28, sticky="ew")
        actiuni = ctk.CTkFrame(self, fg_color="transparent")
        actiuni.grid(row=12, column=0, padx=28, pady=14, sticky="ew")
        ctk.CTkButton(actiuni, text="Anulează", width=110, command=self.destroy).pack(side="left")
        ctk.CTkButton(
            actiuni, text="Salvează", width=150, fg_color="#6751a7", hover_color="#55418e",
            command=self._salveaza,
        ).pack(side="right")

    def _completeaza(self, date: DatePiatra) -> None:
        self._tip.set(next(text for text, cod in self.TIPURI.items() if cod == date.tip))
        for cheie, camp in self._campuri.items():
            valoare = getattr(date, cheie)
            camp.insert(0, valoare if isinstance(valoare, str) else f"{valoare:g}")

    def _activeaza(self) -> None:
        if self.winfo_exists():
            self.grab_set()
            self._campuri["nume"].focus_set()

    def _actualizeaza_eticheta(self, eticheta_tip: str) -> None:
        self._eticheta_extra.configure(text=self.ETICHETE_EXTRA[self.TIPURI[eticheta_tip]])

    def _salveaza(self) -> None:
        mesaj = self._on_salveaza(
            self.TIPURI[self._tip.get()],
            *(camp.get() for camp in self._campuri.values()),
        )
        if mesaj is None:
            self.destroy()
        else:
            self._eroare.configure(text=mesaj)
