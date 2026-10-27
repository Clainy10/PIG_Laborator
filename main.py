"""Compune obiectele aplicației. Toată logica executabilă se află în clase."""

from argparse import ArgumentParser

from Model.model import PiatraModel
from Presenter.presenter import PiatraPresenter


class MainApp:
    def __init__(self) -> None:
        self.model = PiatraModel()
        self.view = None
        self.presenter = None

    def run(self) -> None:
        parser = ArgumentParser(description="Catalog MVP de pietre — laboratoarele 1–5")
        parser.add_argument("--terminal", action="store_true", help="Afișează sortările LL1 fără GUI")
        optiuni = parser.parse_args()
        if optiuni.terminal:
            self.model.afiseaza_sortari_terminal()
            return
        self._porneste_interfata()

    def _porneste_interfata(self) -> None:
        import customtkinter as ctk

        from View.view import PiatraView

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        self.view = PiatraView()
        self.presenter = PiatraPresenter(self.model, self.view)
        self.presenter.initializeaza()
        self.view.mainloop()


if __name__ == "__main__":
    MainApp().run()
