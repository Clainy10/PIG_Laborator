"""LL5: clase exclusiv grafice; toate statisticile sunt primite din Presenter."""

from typing import Callable

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

from Model.model import DateGrafic


class GraficPietre:
    """Desenează o figură reutilizabilă; poate fi verificată și cu backend-ul Agg."""

    FUNDAL = "#202633"
    TEXT = "#edf1f7"
    SECUNDAR = "#aeb9cc"
    CULORI = ("#9d8fdf", "#52b5ad", "#d9ad6c")

    def __init__(self) -> None:
        self.figura = Figure(figsize=(8, 4.8), dpi=100, layout="constrained")
        self.figura.set_facecolor(self.FUNDAL)
        self.axa = self.figura.add_subplot(111)

    def afiseaza(self, date: DateGrafic) -> None:
        axa = self.axa
        axa.clear()
        axa.set_facecolor(self.FUNDAL)
        axa.set_title(date.titlu, color=self.TEXT, fontsize=15, pad=20)
        axa.set_xlabel("Clasă de pietre", color=self.SECUNDAR, labelpad=12)
        axa.set_ylabel(date.eticheta_y, color=self.SECUNDAR, labelpad=12)
        axa.tick_params(colors=self.SECUNDAR, labelsize=11)
        for latura in ("top", "right"):
            axa.spines[latura].set_visible(False)
        for latura in ("bottom", "left"):
            axa.spines[latura].set_color("#475165")
        if not any(date.numere):
            axa.set_xticks([])
            axa.set_yticks([])
            axa.text(
                0.5, 0.5, "Catalogul este gol. Adaugă o piatră.",
                transform=axa.transAxes, ha="center", va="center", color=self.TEXT,
            )
            return
        pozitii = tuple(range(len(date.categorii)))
        inaltimi = tuple(valoare if valoare is not None else 0 for valoare in date.valori)
        bare = axa.bar(pozitii, inaltimi, color=self.CULORI, width=0.55)
        axa.set_xticks(pozitii, date.categorii)
        if date.criteriu == "duritate":
            axa.set_ylim(0, 10.8)
        else:
            axa.set_ylim(0, max(inaltimi, default=1) * 1.25 or 1)
        axa.set_axisbelow(True)
        axa.yaxis.grid(True, color="#475165", linewidth=0.6, alpha=0.5)
        if date.criteriu == "numar":
            axa.yaxis.set_major_locator(MaxNLocator(integer=True))
        for bara, valoare, numar in zip(bare, date.valori, date.numere):
            text = "fără date" if valoare is None else (
                f"{int(valoare)}" if date.criteriu == "numar" else f"{valoare:.2f}"
            )
            if date.criteriu != "numar" and valoare is not None:
                text += f"\nn = {numar}"
            axa.annotate(
                text, (bara.get_x() + bara.get_width() / 2, bara.get_height()),
                xytext=(0, 7), textcoords="offset points", ha="center", va="bottom",
                color=self.TEXT, fontsize=11,
            )


class CadruGrafic(ctk.CTkFrame):
    OPTIUNI = {
        "Duritate medie": "duritate",
        "Densitate medie": "densitate",
        "Număr de pietre": "numar",
    }

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, fg_color=GraficPietre.FUNDAL, **kwargs)
        self._callback: Callable[[str], None] | None = None
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        antet = ctk.CTkFrame(self, fg_color="transparent")
        antet.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 4))
        ctk.CTkLabel(antet, text="Compară clasele", font=("Arial", 20, "bold")).pack(side="left")
        self.selector = ctk.CTkOptionMenu(
            antet, values=list(self.OPTIUNI), command=self._schimba_criteriul, width=190,
        )
        self.selector.pack(side="right", padx=(16, 0))
        self.grafic = GraficPietre()
        self.canvas = FigureCanvasTkAgg(self.grafic.figura, master=self)
        self.canvas.get_tk_widget().configure(highlightthickness=0)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=16, pady=12)
        self.rezumat = ctk.CTkLabel(self, text="", text_color=GraficPietre.SECUNDAR, wraplength=700)
        self.rezumat.grid(row=2, column=0, sticky="ew", padx=24, pady=(0, 16))

    def seteaza_callback(self, callback: Callable[[str], None]) -> None:
        self._callback = callback

    def _schimba_criteriul(self, eticheta: str) -> None:
        if self._callback is not None:
            self._callback(self.OPTIUNI[eticheta])

    def afiseaza(self, date: DateGrafic) -> None:
        self.selector.set(next(text for text, cheie in self.OPTIUNI.items() if cheie == date.criteriu))
        self.grafic.afiseaza(date)
        self.canvas.draw_idle()
        self.rezumat.configure(text=" · ".join(
            f"{categorie}: {numar}" for categorie, numar in zip(date.categorii, date.numere)
        ))
