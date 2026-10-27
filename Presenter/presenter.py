"""Cazurile de utilizare MVP. Nu importă View, Tkinter sau Matplotlib."""

from typing import Callable, Protocol, Sequence

from Model.model import DateGrafic, DatePiatra, PiatraModel


class IPiatraView(Protocol):
    """Contract pasiv: View afișează date și transmite evenimente."""

    def configureaza_actiuni(
        self, adauga: Callable[[], None], editeaza: Callable[[str], None],
        sterge: Callable[[str], None], sorteaza: Callable[[str], None],
        schimba_grafic: Callable[[str], None],
    ) -> None: ...

    def afiseaza_elemente_in_cadre(self, pietre: Sequence[DatePiatra]) -> None: ...
    def actualizeaza_sortare(self, atribut: str | None, descrescator: bool) -> None: ...
    def afiseaza_grafic(self, date: DateGrafic) -> None: ...
    def deschide_dialog_adaugare(
        self, on_salveaza: Callable[..., str | None],
        obiect_existent: DatePiatra | None = None,
    ) -> None: ...
    def confirma_stergere(self, nume: str) -> bool: ...
    def afiseaza_eroare(self, mesaj: str) -> None: ...


class PiatraPresenter:
    def __init__(self, model: PiatraModel, view: IPiatraView) -> None:
        self.model = model
        self.view = view
        self._atribut_sortare: str | None = None
        self._descrescator = False
        self._criteriu_grafic = "duritate"

    def initializeaza(self) -> None:
        self.view.configureaza_actiuni(
            self.deschide_adaugare, self.deschide_editare,
            self.sterge_obiect, self.sorteaza, self.schimba_grafic,
        )
        self.reimprospateaza_ui()

    def reimprospateaza_ui(self) -> None:
        if self._atribut_sortare is not None:
            self.model.sorteaza_dupa(self._atribut_sortare, self._descrescator)
        self.view.afiseaza_elemente_in_cadre(self.model.get_date_lista())
        self.view.actualizeaza_sortare(self._atribut_sortare, self._descrescator)
        self.view.afiseaza_grafic(self.model.get_date_grafic(self._criteriu_grafic))

    def deschide_adaugare(self) -> None:
        self.view.deschide_dialog_adaugare(self.adauga_obiect)

    def deschide_editare(self, id_piatra: str) -> None:
        try:
            piatra = self.model.get_date_piatra(id_piatra)
        except ValueError as exc:
            self.view.afiseaza_eroare(str(exc))
            return
        self.view.deschide_dialog_adaugare(
            lambda *date: self.editeaza_obiect(id_piatra, *date), piatra,
        )

    def _salveaza(
        self, tip: str, nume: str, duritate: str, densitate: str, extra: str,
        *, id_piatra: str | None = None,
    ) -> str | None:
        try:
            if id_piatra is None:
                self.model.adauga_piatra(tip, nume, duritate, densitate, extra)
            else:
                self.model.editeaza_piatra(id_piatra, tip, nume, duritate, densitate, extra)
        except ValueError as exc:
            return str(exc)
        self.reimprospateaza_ui()
        return None

    def adauga_obiect(
        self, tip: str, nume: str, duritate: str, densitate: str, extra: str,
    ) -> str | None:
        return self._salveaza(tip, nume, duritate, densitate, extra)

    def editeaza_obiect(
        self, id_piatra: str, tip: str, nume: str,
        duritate: str, densitate: str, extra: str,
    ) -> str | None:
        return self._salveaza(tip, nume, duritate, densitate, extra, id_piatra=id_piatra)

    def sterge_obiect(self, id_piatra: str) -> None:
        try:
            piatra = self.model.get_date_piatra(id_piatra)
            if self.view.confirma_stergere(piatra.nume):
                self.model.sterge_piatra(id_piatra)
                self.reimprospateaza_ui()
        except ValueError as exc:
            self.view.afiseaza_eroare(str(exc))

    def sorteaza(self, atribut: str) -> None:
        if atribut not in {"nume", "duritate", "densitate"}:
            self.view.afiseaza_eroare("Criteriu de sortare necunoscut.")
            return
        self._descrescator = not self._descrescator if atribut == self._atribut_sortare else False
        self._atribut_sortare = atribut
        self.reimprospateaza_ui()

    def schimba_grafic(self, criteriu: str) -> None:
        try:
            date = self.model.get_date_grafic(criteriu)
        except ValueError as exc:
            self.view.afiseaza_eroare(str(exc))
            return
        self._criteriu_grafic = criteriu
        self.view.afiseaza_grafic(date)
