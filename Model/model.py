"""Stocare, CRUD, sortare și calcule pentru grafice. Fără importuri grafice."""

from dataclasses import dataclass
from statistics import fmean
from typing import Iterable

from Model.Class.baseclass import Piatra
from Model.Class.clase_pietre import PiatraMagmatica, PiatraPretioasa, PiatraSedimentara


@dataclass(frozen=True)
class DatePiatra:
    """Date simple pentru afișare; View nu primește entități modificabile."""

    id: str
    tip: str
    nume: str
    duritate: float
    densitate: float
    extra: float
    eticheta_extra: str
    unitate_extra: str


@dataclass(frozen=True)
class DateGrafic:
    criteriu: str
    titlu: str
    eticheta_y: str
    categorii: tuple[str, ...]
    valori: tuple[float | None, ...]
    numere: tuple[int, ...]


class PiatraModel:
    CLASE = {
        "Pretioasa": PiatraPretioasa,
        "Magmatica": PiatraMagmatica,
        "Sedimentara": PiatraSedimentara,
    }
    ETICHETE_CLASE = ("Prețioase", "Magmatice", "Sedimentare")
    CRITERII_GRAFIC = {
        "duritate": ("Duritate medie pe clasă", "Duritate medie (Mohs)"),
        "densitate": ("Densitate medie pe clasă", "Densitate medie (g/cm³)"),
        "numar": ("Numărul de pietre pe clasă", "Număr de pietre"),
    }

    def __init__(self, pietre: Iterable[Piatra] | None = None) -> None:
        self._pietre: list[Piatra] = []
        if pietre is None:
            self._genereaza_date()
        else:
            self._pietre.extend(pietre)
            identificatori = [piatra.get_id() for piatra in self._pietre]
            if len(set(identificatori)) != len(identificatori):
                raise ValueError("Colecția conține identificatori duplicați.")
        if any(type(piatra) not in self.CLASE.values() for piatra in self._pietre):
            raise ValueError("Colecția acceptă doar cele trei clase derivate de pietre.")

    def _genereaza_date(self) -> None:
        for i in range(1, 11):
            self._pietre.extend((
                PiatraPretioasa(
                    f"Diamant {i}", round(9.5 - i * 0.1, 2),
                    round(3.5 + i * 0.01, 2), 1 + i * 0.5,
                ),
                PiatraMagmatica(
                    f"Granit {i}", round(6 + i * 0.1, 2),
                    round(2.6 + i * 0.02, 2), 1200 + i * 10,
                ),
                PiatraSedimentara(
                    f"Calcar {i}", round(3 + i * 0.1, 2),
                    round(2.3 + i * 0.01, 2), round(5 + i * 0.8, 2),
                ),
            ))

    def get_toate_pietrele(self) -> list[Piatra]:
        """Returnează o copie a listei, păstrând interfața proiectului inițial."""
        return self._pietre.copy()

    def _gaseste_index(self, id_piatra: str) -> int:
        for index, piatra in enumerate(self._pietre):
            if piatra.get_id() == id_piatra:
                return index
        raise ValueError("Piatra nu mai există în catalog.")

    @staticmethod
    def _date_piatra(piatra: Piatra) -> DatePiatra:
        return DatePiatra(
            id=piatra.get_id(), tip=piatra.TIP, nume=piatra.get_nume(),
            duritate=piatra.get_duritate(), densitate=piatra.get_densitate(),
            extra=piatra.get_extra(), eticheta_extra=piatra.ETICHETA_EXTRA,
            unitate_extra=piatra.UNITATE_EXTRA,
        )

    def get_date_lista(self) -> tuple[DatePiatra, ...]:
        return tuple(self._date_piatra(piatra) for piatra in self._pietre)

    def get_date_piatra(self, id_piatra: str) -> DatePiatra:
        return self._date_piatra(self._pietre[self._gaseste_index(id_piatra)])

    @classmethod
    def _creeaza_piatra(
        cls, tip: str, nume: str, duritate: float | str, densitate: float | str, extra: float | str,
        *, id_piatra: str | None = None,
    ) -> Piatra:
        if tip not in cls.CLASE:
            raise ValueError("Tip de piatră necunoscut.")
        return cls.CLASE[tip](nume, duritate, densitate, extra, id_piatra=id_piatra)

    def adauga_piatra(
        self, tip: str, nume: str, duritate: float | str, densitate: float | str, extra: float | str,
    ) -> None:
        self._pietre.append(self._creeaza_piatra(tip, nume, duritate, densitate, extra))

    def editeaza_piatra(
        self, id_piatra: str, tip: str, nume: str,
        duritate: float | str, densitate: float | str, extra: float | str,
    ) -> None:
        index = self._gaseste_index(id_piatra)
        # Construirea completă precede înlocuirea: datele invalide nu lasă editări parțiale.
        piatra = self._creeaza_piatra(
            tip, nume, duritate, densitate, extra, id_piatra=id_piatra,
        )
        self._pietre[index] = piatra

    def sterge_piatra(self, id_piatra: str) -> None:
        self._pietre.pop(self._gaseste_index(id_piatra))

    def sorteaza_dupa(self, atribut: str, descrescator: bool = False) -> None:
        chei = {
            "nume": lambda piatra: piatra.get_nume().casefold(),
            "duritate": lambda piatra: piatra.get_duritate(),
            "densitate": lambda piatra: piatra.get_densitate(),
        }
        if atribut not in chei:
            raise ValueError("Criteriu de sortare necunoscut.")
        self._pietre.sort(key=chei[atribut], reverse=descrescator)

    def get_date_grafic(self, criteriu: str = "duritate") -> DateGrafic:
        if criteriu not in self.CRITERII_GRAFIC:
            raise ValueError("Criteriu de grafic necunoscut.")
        grupuri: dict[str, list[Piatra]] = {tip: [] for tip in self.CLASE}
        for piatra in self._pietre:
            grupuri[piatra.TIP].append(piatra)
        numere = tuple(len(grup) for grup in grupuri.values())
        if criteriu == "numar":
            valori = tuple(float(numar) for numar in numere)
        else:
            metoda = Piatra.get_duritate if criteriu == "duritate" else Piatra.get_densitate
            # None înseamnă lipsa observațiilor; media unei clase goale nu este zero.
            valori = tuple(
                fmean(metoda(piatra) for piatra in grup) if grup else None
                for grup in grupuri.values()
            )
        titlu, eticheta_y = self.CRITERII_GRAFIC[criteriu]
        return DateGrafic(criteriu, titlu, eticheta_y, self.ETICHETE_CLASE, valori, numere)

    def afiseaza_sortari_terminal(self) -> None:
        """Demonstrația LL1, fără a modifica ordinea curentă a catalogului."""
        copie = self._pietre.copy()
        try:
            for atribut in ("nume", "duritate", "densitate"):
                self.sorteaza_dupa(atribut)
                print(f"\nSortare după {atribut}:")
                for piatra in self._pietre:
                    print(piatra)
        finally:
            self._pietre = copie
