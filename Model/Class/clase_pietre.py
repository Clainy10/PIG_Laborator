"""Cele trei clase derivate din Piatra, păstrate din proiectul inițial."""

from Model.Class.baseclass import Piatra


class PiatraPretioasa(Piatra):
    TIP = "Pretioasa"
    ETICHETA_EXTRA = "Carate"
    UNITATE_EXTRA = "ct"

    def __init__(
        self, nume: str, duritate: float | str, densitate: float | str, carate: float | str,
        *, id_piatra: str | None = None,
    ) -> None:
        super().__init__(nume, duritate, densitate, id_piatra=id_piatra)
        self.carate = carate

    @property
    def carate(self) -> float:
        return self._carate

    @carate.setter
    def carate(self, valoare: float | str) -> None:
        numar = self.valideaza_numar(valoare, "Carate")
        if numar <= 0:
            raise ValueError("Caratele trebuie să fie pozitive.")
        self._carate = numar

    def get_extra(self) -> float:
        return self.carate

    def __str__(self) -> str:
        return f"{super().__str__()} | Carate: {self.carate:g} ct"


class PiatraMagmatica(Piatra):
    TIP = "Magmatica"
    ETICHETA_EXTRA = "Temperatura de topire"
    UNITATE_EXTRA = "°C"

    def __init__(
        self, nume: str, duritate: float | str, densitate: float | str,
        temperatura_topire: float | str, *, id_piatra: str | None = None,
    ) -> None:
        super().__init__(nume, duritate, densitate, id_piatra=id_piatra)
        self.temperatura_topire = temperatura_topire

    @property
    def temperatura_topire(self) -> int:
        return self._temperatura_topire

    @temperatura_topire.setter
    def temperatura_topire(self, valoare: float | str) -> None:
        numar = self.valideaza_numar(valoare, "Temperatura de topire")
        if numar <= 0 or not numar.is_integer():
            raise ValueError("Temperatura de topire trebuie să fie un număr întreg pozitiv.")
        self._temperatura_topire = int(numar)

    def get_extra(self) -> float:
        return self.temperatura_topire

    def __str__(self) -> str:
        return f"{super().__str__()} | Temperatura de topire: {self.temperatura_topire} °C"


class PiatraSedimentara(Piatra):
    TIP = "Sedimentara"
    ETICHETA_EXTRA = "Porozitate"
    UNITATE_EXTRA = "%"

    def __init__(
        self, nume: str, duritate: float | str, densitate: float | str, porozitate: float | str,
        *, id_piatra: str | None = None,
    ) -> None:
        super().__init__(nume, duritate, densitate, id_piatra=id_piatra)
        self.porozitate = porozitate

    @property
    def porozitate(self) -> float:
        return self._porozitate

    @porozitate.setter
    def porozitate(self, valoare: float | str) -> None:
        numar = self.valideaza_numar(valoare, "Porozitate")
        if not 0 <= numar <= 100:
            raise ValueError("Porozitatea trebuie să fie între 0 și 100%.")
        self._porozitate = numar

    def get_extra(self) -> float:
        return self.porozitate

    def __str__(self) -> str:
        return f"{super().__str__()} | Porozitate: {self.porozitate:g}%"
