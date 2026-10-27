import ast
import unittest
from pathlib import Path


class TestArhitectura(unittest.TestCase):
    RADACINA = Path(__file__).resolve().parents[1]
    ORIGINALE = (
        'Model/Interface/interface.py', 'Model/Class/baseclass.py',
        'Model/Class/clase_pietre.py', 'Model/model.py',
        'Presenter/presenter.py', 'View/view.py', 'View/dialog_adaugare.py', 'main.py',
    )

    def test_fisierele_originale_sunt_pastrate(self):
        for nume in self.ORIGINALE:
            self.assertTrue((self.RADACINA / nume).is_file(), nume)

    def test_fara_functii_libere_in_codul_aplicatiei(self):
        fisiere = [self.RADACINA / nume for nume in self.ORIGINALE]
        fisiere.append(self.RADACINA / 'View/grafic.py')
        for fisier in fisiere:
            arbore = ast.parse(fisier.read_text(encoding='utf-8'))
            functii_libere = [nod.name for nod in arbore.body if isinstance(nod, (ast.FunctionDef, ast.AsyncFunctionDef))]
            self.assertEqual(functii_libere, [], str(fisier))
            for nod in arbore.body:
                if isinstance(nod, ast.Expr):
                    self.assertIsInstance(nod.value, ast.Constant, str(fisier))

    def test_model_si_presenter_nu_importa_biblioteci_grafice(self):
        fisiere = list((self.RADACINA / 'Model').rglob('*.py'))
        fisiere += list((self.RADACINA / 'Presenter').rglob('*.py'))
        interzise = {'tkinter', 'customtkinter', 'matplotlib', 'PIL', 'View'}
        for fisier in fisiere:
            arbore = ast.parse(fisier.read_text(encoding='utf-8'))
            for nod in ast.walk(arbore):
                module = []
                if isinstance(nod, ast.Import):
                    module = [alias.name for alias in nod.names]
                elif isinstance(nod, ast.ImportFrom):
                    module = [nod.module or '']
                self.assertFalse(any(modul.split('.')[0] in interzise for modul in module), str(fisier))

    def test_view_nu_instantiaza_model_sau_presenter(self):
        for fisier in (self.RADACINA / 'View').glob('*.py'):
            arbore = ast.parse(fisier.read_text(encoding='utf-8'))
            for nod in ast.walk(arbore):
                if isinstance(nod, ast.Name):
                    self.assertNotIn(nod.id, {'PiatraModel', 'PiatraPresenter'}, str(fisier))

    def test_imaginile_locale_exista(self):
        for tip in ('pretioasa', 'magmatica', 'sedimentara'):
            fisier = self.RADACINA / 'View/imagini' / f'{tip}.png'
            self.assertTrue(fisier.is_file())
            self.assertGreater(fisier.stat().st_size, 1000)
