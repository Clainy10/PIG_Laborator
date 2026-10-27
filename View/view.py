"""Clasele interfeței: imagini locale, carduri, fereastră și callback-uri."""

import logging
from functools import partial
from pathlib import Path
from tkinter import messagebox
from typing import Callable, Sequence

import customtkinter as ctk
from PIL import Image, UnidentifiedImageError

from Model.model import DateGrafic, DatePiatra
from View.dialog_adaugare import DialogAdaugarePiatra
from View.grafic import CadruGrafic


class Stil:
    FUNDAL = "#141923"
    SUPRAFATA = "#202633"
    ACCENT = "#6751a7"
    HOVER = "#55418e"
    TEXT = "#edf1f7"
    SECUNDAR = "#aeb9cc"
    PERICOL = "#713d4c"


class CacheImagini:
    """Încarcă o singură dată cele trei imagini, independent de directorul curent."""

    FISIERE = {
        "Pretioasa": "pretioasa.png",
        "Magmatica": "magmatica.png",
        "Sedimentara": "sedimentara.png",
    }

    def __init__(self) -> None:
        self._imagini: dict[str, ctk.CTkImage | None] = {}
        self.lipsa: list[str] = []
        director = Path(__file__).resolve().parent / "imagini"
        for tip, nume in self.FISIERE.items():
            try:
                with Image.open(director / nume) as sursa:
                    imagine = sursa.convert("RGB")
                self._imagini[tip] = ctk.CTkImage(
                    light_image=imagine, dark_image=imagine, size=(88, 88),
                )
            except (OSError, UnidentifiedImageError) as exc:
                logging.getLogger(__name__).warning("Imagine indisponibilă %s: %s", nume, exc)
                self._imagini[tip] = None
                self.lipsa.append(nume)

    def obtine(self, tip: str) -> ctk.CTkImage | None:
        return self._imagini[tip]


class CadruPiatra(ctk.CTkFrame):
    TIPURI = {"Pretioasa": "Prețioasă", "Magmatica": "Magmatică", "Sedimentara": "Sedimentară"}

    def __init__(
        self, master, id_piatra: str, imagini: CacheImagini,
        editeaza: Callable[[str], None], sterge: Callable[[str], None],
    ) -> None:
        super().__init__(master, fg_color=Stil.SUPRAFATA, corner_radius=12)
        self._imagini = imagini
        self._tip_imagine: str | None = None
        self.grid_columnconfigure(1, weight=1)
        self._imagine = ctk.CTkLabel(self, text="", width=88, height=88)
        self._imagine.grid(row=0, column=0, rowspan=3, padx=(14, 16), pady=14)
        self._titlu = ctk.CTkLabel(self, text="", anchor="w", font=("Arial", 17, "bold"), justify="left")
        self._titlu.grid(row=0, column=1, sticky="ew", pady=(15, 0))
        self._tip = ctk.CTkLabel(self, text="", anchor="w", text_color=Stil.SECUNDAR)
        self._tip.grid(row=1, column=1, sticky="ew")
        self._detalii = ctk.CTkLabel(
            self, text="", anchor="w", justify="left", text_color=Stil.SECUNDAR,
        )
        self._detalii.grid(row=2, column=1, sticky="ew", pady=(0, 15))
        ctk.CTkButton(
            self, text="Editează", width=92, height=32,
            fg_color=Stil.ACCENT, hover_color=Stil.HOVER,
            command=partial(editeaza, id_piatra),
        ).grid(row=0, column=2, rowspan=2, padx=16, pady=(14, 5))
        ctk.CTkButton(
            self, text="Șterge", width=92, height=32, fg_color=Stil.PERICOL,
            hover_color="#8b495b", command=partial(sterge, id_piatra),
        ).grid(row=2, column=2, padx=16, pady=(0, 14))
        self.bind("<Configure>", self._redimensioneaza)

    def _redimensioneaza(self, eveniment) -> None:
        latime = max(180, eveniment.width - 270)
        self._titlu.configure(wraplength=latime)
        self._detalii.configure(wraplength=latime)

    def afiseaza(self, piatra: DatePiatra) -> None:
        imagine = self._imagini.obtine(piatra.tip)
        if imagine is None and self._tip_imagine != piatra.tip:
            # CTkLabel 5.2 nu șterge întotdeauna imaginea precedentă la image=None.
            self._imagine.destroy()
            self._imagine = ctk.CTkLabel(self, text="◇", width=88, height=88)
            self._imagine.grid(row=0, column=0, rowspan=3, padx=(14, 16), pady=14)
        else:
            self._imagine.configure(image=imagine, text="◇" if imagine is None else "")
        self._tip_imagine = piatra.tip
        self._titlu.configure(text=piatra.nume)
        self._tip.configure(text=self.TIPURI[piatra.tip])
        self._detalii.configure(text=(
            f"Duritate: {piatra.duritate:g} Mohs  ·  Densitate: {piatra.densitate:g} g/cm³\n"
            f"{piatra.eticheta_extra}: {piatra.extra:g} {piatra.unitate_extra}"
        ))


class PiatraView(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Laboratorul 5 · Catalog de pietre · MVP")
        self.geometry("1080x800")
        self.minsize(840, 650)
        self.configure(fg_color=Stil.FUNDAL)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._imagini = CacheImagini()
        self._cadre: dict[str, CadruPiatra] = {}
        self._dialog: DialogAdaugarePiatra | None = None
        self._editeaza: Callable[[str], None] | None = None
        self._sterge: Callable[[str], None] | None = None
        self._construieste_layout()

    def _construieste_layout(self) -> None:
        antet = ctk.CTkFrame(self, fg_color="transparent")
        antet.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 8))
        antet.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            antet, text="LABORATORUL 5 / MODEL · VIEW · PRESENTER", text_color=Stil.SECUNDAR,
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(antet, text="Catalog de pietre", font=("Arial", 29, "bold")).grid(
            row=1, column=0, sticky="w", pady=(4, 0),
        )
        self._buton_adauga = ctk.CTkButton(
            antet, text="+ Adaugă piatră", height=38,
            fg_color=Stil.ACCENT, hover_color=Stil.HOVER,
        )
        self._buton_adauga.grid(row=0, column=1, rowspan=2, padx=(20, 0))
        self._taburi = ctk.CTkTabview(
            self, fg_color=Stil.FUNDAL, segmented_button_selected_color=Stil.ACCENT,
            segmented_button_selected_hover_color=Stil.HOVER,
        )
        self._taburi.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 8))
        lista = self._taburi.add("Colecție")
        tab_grafic = self._taburi.add("Grafice")
        lista.grid_columnconfigure(0, weight=1)
        lista.grid_rowconfigure(1, weight=1)
        bara = ctk.CTkFrame(lista, fg_color="transparent")
        bara.grid(row=0, column=0, sticky="ew", padx=8, pady=(4, 10))
        bara.grid_columnconfigure(0, weight=1)
        self._contor = ctk.CTkLabel(bara, text="", text_color=Stil.SECUNDAR)
        self._contor.grid(row=0, column=0, sticky="w")
        self._butoane_sortare: dict[str, ctk.CTkButton] = {}
        for coloana, atribut in enumerate(("nume", "duritate", "densitate"), start=1):
            buton = ctk.CTkButton(bara, text=atribut.capitalize(), width=120, fg_color=Stil.SUPRAFATA)
            buton.grid(row=0, column=coloana, padx=(8, 0))
            self._butoane_sortare[atribut] = buton
        self._lista = ctk.CTkScrollableFrame(lista, fg_color="transparent")
        self._lista.grid(row=1, column=0, sticky="nsew")
        self._lista.grid_columnconfigure(0, weight=1)
        self._mesaj_gol = ctk.CTkLabel(self._lista, text="Catalogul este gol. Adaugă prima piatră.")
        tab_grafic.grid_columnconfigure(0, weight=1)
        tab_grafic.grid_rowconfigure(0, weight=1)
        self._grafic = CadruGrafic(tab_grafic)
        self._grafic.grid(row=0, column=0, sticky="nsew", padx=6, pady=8)
        text = "Date demonstrative în memorie · Imagini reprezentative generate cu AI"
        if self._imagini.lipsa:
            text += " · Unele imagini nu au fost găsite"
        ctk.CTkLabel(self, text=text, text_color=Stil.SECUNDAR).grid(
            row=2, column=0, sticky="ew", padx=24, pady=(0, 12),
        )

    def configureaza_actiuni(self, adauga, editeaza, sterge, sorteaza, schimba_grafic) -> None:
        self._buton_adauga.configure(command=adauga)
        self._editeaza, self._sterge = editeaza, sterge
        for atribut, buton in self._butoane_sortare.items():
            buton.configure(command=partial(sorteaza, atribut))
        self._grafic.seteaza_callback(schimba_grafic)

    def afiseaza_elemente_in_cadre(self, pietre: Sequence[DatePiatra]) -> None:
        identificatori = {piatra.id for piatra in pietre}
        for id_piatra in set(self._cadre) - identificatori:
            self._cadre.pop(id_piatra).destroy()
        self._mesaj_gol.grid_remove()
        if not pietre:
            self._mesaj_gol.grid(row=0, column=0, pady=40)
        for index, piatra in enumerate(pietre):
            if piatra.id not in self._cadre:
                self._cadre[piatra.id] = CadruPiatra(
                    self._lista, piatra.id, self._imagini, self._editeaza, self._sterge,
                )
            cadru = self._cadre[piatra.id]
            cadru.afiseaza(piatra)
            cadru.grid(row=index, column=0, sticky="ew", padx=4, pady=5)
        self._contor.configure(text=f"{len(pietre)} pietre în catalog")

    def actualizeaza_sortare(self, atribut: str | None, descrescator: bool) -> None:
        for cheie, buton in self._butoane_sortare.items():
            activ = cheie == atribut
            simbol = (" ▼" if descrescator else " ▲") if activ else ""
            buton.configure(
                text=cheie.capitalize() + simbol,
                fg_color=Stil.ACCENT if activ else Stil.SUPRAFATA,
            )

    def afiseaza_grafic(self, date: DateGrafic) -> None:
        self._grafic.afiseaza(date)

    def deschide_dialog_adaugare(
        self, on_salveaza: Callable[..., str | None],
        obiect_existent: DatePiatra | None = None,
    ) -> None:
        if self._dialog is not None and self._dialog.winfo_exists():
            self._dialog.lift()
            return
        self._dialog = DialogAdaugarePiatra(self, on_salveaza, obiect_existent)

    def confirma_stergere(self, nume: str) -> bool:
        return messagebox.askyesno("Șterge piatra", f"Ștergi «{nume}»?", parent=self)

    def afiseaza_eroare(self, mesaj: str) -> None:
        messagebox.showerror("Catalog de pietre", mesaj, parent=self)
