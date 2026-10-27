"""Contractul din LL1 pentru parametrii comuni ai unei pietre."""

from abc import ABC, abstractmethod


class IPiatra(ABC):
    @abstractmethod
    def set_nume(self, nume: str) -> None:
        """Setează numele după validare."""

    @abstractmethod
    def get_nume(self) -> str:
        """Returnează numele."""

    @abstractmethod
    def set_duritate(self, duritate: float) -> None:
        """Setează duritatea pe scara Mohs."""

    @abstractmethod
    def get_duritate(self) -> float:
        """Returnează duritatea."""

    @abstractmethod
    def set_densitate(self, densitate: float) -> None:
        """Setează densitatea în g/cm³."""

    @abstractmethod
    def get_densitate(self) -> float:
        """Returnează densitatea."""
