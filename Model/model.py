"""Stocare, CRUD, sortare și calcule folosind exclusiv DBManager ca intermediar."""

from dataclasses import dataclass
from statistics import fmean

from Model.Class.baseclass import Piatra
from Model.Class.clase_pietre import PiatraMagmatica, PiatraPretioasa, PiatraSedimentara
from Model.DBManager import DatabaseManager


@dataclass(frozen=True)
class DatePiatra:
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

    def __init__(self) -> None:
        self.db = DatabaseManager()
        if not self.db.obtine_toate():
            self._genereaza_date_initiale()

    def _genereaza_date_initiale(self) -> None:
        date_initiale = [
            ("Pretioasa", "Diamant 1", 9.4, 3.51, 1.5),
            ("Pretioasa", "Rubin 1", 9.0, 4.02, 2.0),
            ("Magmatica", "Granit 1", 6.1, 2.65, 1210.0),
            ("Magmatica", "Bazalt 1", 6.5, 2.90, 1150.0),
            ("Sedimentara", "Calcar 1", 3.1, 2.31, 5.8),
            ("Sedimentara", "Gresie 1", 6.0, 2.25, 7.2),
        ]
        for tip, nume, duritate, densitate, extra in date_initiale:
            self.db.insereaza(tip, nume, duritate, densitate, extra)

    def _instantiaza_obiect(self, r: dict) -> Piatra:
        tip = r["tip"]
        if tip not in self.CLASE:
            raise ValueError(f"Tip de piatră necunoscut în baza de date: {tip}")
        cls_piatra = self.CLASE[tip]
        
        # Apelăm constructorul trimițând valorile pozițional, exact cum sunt definite în clasele tale
        return cls_piatra(
            r["nume"],
            r["duritate"],
            r["densitate"],
            r["extra"],
            id_piatra=str(r["id"])
        )

    def get_toate_pietrele(self) -> list[Piatra]:
        randuri = self.db.obtine_toate()
        return [self._instantiaza_obiect(r) for r in randuri]

    @staticmethod
    def _date_piatra(piatra: Piatra) -> DatePiatra:
        return DatePiatra(
            id=piatra.get_id(),
            tip=piatra.TIP,
            nume=piatra.get_nume(),
            duritate=piatra.get_duritate(),
            densitate=piatra.get_densitate(),
            extra=piatra.get_extra(),
            eticheta_extra=piatra.ETICHETA_EXTRA,
            unitate_extra=piatra.UNITATE_EXTRA,
        )

    def get_date_lista(self) -> tuple[DatePiatra, ...]:
        pietre = self.get_toate_pietrele()
        return tuple(self._date_piatra(p) for p in pietre)

    def get_date_piatra(self, id_piatra: str) -> DatePiatra:
        pietre = self.get_toate_pietrele()
        for p in pietre:
            if p.get_id() == id_piatra:
                return self._date_piatra(p)
        raise ValueError("Piatra nu există în baza de date.")

    def adauga_piatra(
        self, tip: str, nume: str, duritate: float | str, densitate: float | str, extra: float | str,
    ) -> None:
        if tip not in self.CLASE:
            raise ValueError("Tip de piatră necunoscut.")
        self.db.insereaza(tip, nume, float(duritate), float(densitate), float(extra))

    def editeaza_piatra(
        self, id_piatra: str, tip: str, nume: str,
        duritate: float | str, densitate: float | str, extra: float | str,
    ) -> None:
        if tip not in self.CLASE:
            raise ValueError("Tip de piatră necunoscut.")
        self.db.actualizeaza(id_piatra, tip, nume, float(duritate), float(densitate), float(extra))

    def sterge_piatra(self, id_piatra: str) -> None:
        self.db.sterge(id_piatra)

    def sorteaza_dupa(self, atribut: str, descrescator: bool = False) -> list[Piatra]:
        pietre = self.get_toate_pietrele()
        chei = {
            "nume": lambda piatra: piatra.get_nume().casefold(),
            "duritate": lambda piatra: piatra.get_duritate(),
            "densitate": lambda piatra: piatra.get_densitate(),
        }
        if atribut not in chei:
            raise ValueError("Criteriu de sortare necunoscut.")
        pietre.sort(key=chei[atribut], reverse=descrescator)
        return pietre

    def get_date_grafic(self, criteriu: str = "duritate") -> DateGrafic:
        if criteriu not in self.CRITERII_GRAFIC:
            raise ValueError("Criteriu de grafic necunoscut.")
        
        pietre = self.get_toate_pietrele()
        grupuri: dict[str, list[Piatra]] = {tip: [] for tip in self.CLASE}
        for piatra in pietre:
            grupuri[piatra.TIP].append(piatra)
            
        numere = tuple(len(grup) for grup in grupuri.values())
        if criteriu == "numar":
            valori = tuple(float(numar) for numar in numere)
        else:
            metoda = Piatra.get_duritate if criteriu == "duritate" else Piatra.get_densitate
            valori = tuple(
                fmean(metoda(piatra) for piatra in grup) if grup else None
                for grup in grupuri.values()
            )
        titlu, eticheta_y = self.CRITERII_GRAFIC[criteriu]
        return DateGrafic(criteriu, titlu, eticheta_y, self.ETICHETE_CLASE, valori, numere)

    def afiseaza_sortari_terminal(self) -> None:
        """Demonstrația LL1, fără a modifica ordinea curentă a catalogului."""
        pietre = self.get_toate_pietrele()
        copie = pietre.copy()
        try:
            for atribut in ("nume", "duritate", "densitate"):
                pietre_sortate = self.sorteaza_dupa(atribut)
                print(f"\nSortare după {atribut}:")
                for piatra in pietre_sortate:
                    print(piatra)
        finally:
            pass