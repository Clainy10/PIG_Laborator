"""Clasa de bază din LL1: implementare concretă a interfeței IPiatra."""

from math import isfinite
from uuid import uuid4

from Model.Interface.interface import IPiatra


class Piatra(IPiatra):
    def __init__(
        self, nume: str, duritate: float | str, densitate: float | str,
        *, id_piatra: str | None = None,
    ) -> None:
        self._id = id_piatra if id_piatra is not None else uuid4().hex
        self.set_nume(nume)
        self.set_duritate(duritate)
        self.set_densitate(densitate)

    @staticmethod
    def valideaza_numar(valoare: float | str, eticheta: str) -> float:
        if isinstance(valoare, bool):
            raise ValueError(f"{eticheta}: introdu un număr valid.")
        try:
            numar = float(str(valoare).strip().replace(",", "."))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{eticheta}: introdu un număr valid.") from exc
        if not isfinite(numar):
            raise ValueError(f"{eticheta}: numărul trebuie să fie finit.")
        return numar

    def get_id(self) -> str:
        """ID-ul rămâne stabil la sortare și editare."""
        return self._id

    def set_nume(self, nume: str) -> None:
        if not isinstance(nume, str) or not nume.strip():
            raise ValueError("Numele este obligatoriu.")
        if len(nume.strip()) > 100:
            raise ValueError("Numele poate avea cel mult 100 de caractere.")
        self._nume = nume.strip()

    def get_nume(self) -> str:
        return self._nume

    def set_duritate(self, duritate: float | str) -> None:
        valoare = self.valideaza_numar(duritate, "Duritate")
        if not 1 <= valoare <= 10:
            raise ValueError("Duritatea Mohs trebuie să fie între 1 și 10.")
        self._duritate = valoare

    def get_duritate(self) -> float:
        return self._duritate

    def set_densitate(self, densitate: float | str) -> None:
        valoare = self.valideaza_numar(densitate, "Densitate")
        if valoare <= 0:
            raise ValueError("Densitatea trebuie să fie pozitivă.")
        self._densitate = valoare

    def get_densitate(self) -> float:
        return self._densitate

    def __str__(self) -> str:
        return (
            f"Nume: {self.get_nume()} | Duritate: {self.get_duritate():g} Mohs"
            f" | Densitate: {self.get_densitate():g} g/cm³"
        )
