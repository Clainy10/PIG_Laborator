import io
import unittest

from Model.model import PiatraModel


class TestGrafic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from View.grafic import GraficPietre
            from matplotlib.backends.backend_agg import FigureCanvasAgg
        except ImportError as exc:
            raise unittest.SkipTest(f'Dependențe grafice indisponibile: {exc}') from exc
        cls.ClasaGrafic = GraficPietre
        cls.CanvasAgg = FigureCanvasAgg

    def setUp(self):
        self.model = PiatraModel()
        self.grafic = self.ClasaGrafic()

    def test_barele_folosesc_valorile_calculate_de_model(self):
        date = self.model.get_date_grafic()
        self.grafic.afiseaza(date)
        self.assertEqual(len(self.grafic.axa.patches), 3)
        for bara, valoare in zip(self.grafic.axa.patches, date.valori):
            self.assertAlmostEqual(bara.get_height(), valoare)
        self.assertEqual(self.grafic.axa.get_ylabel(), date.eticheta_y)

    def test_schimbarea_indicatorului_reutilizeaza_axa(self):
        axa = self.grafic.axa
        for criteriu in ('duritate', 'densitate', 'numar'):
            self.grafic.afiseaza(self.model.get_date_grafic(criteriu))
            self.assertIs(self.grafic.axa, axa)
            self.assertEqual(len(axa.patches), 3)
            iesire = io.BytesIO()
            self.CanvasAgg(self.grafic.figura).print_png(iesire)
            self.assertGreater(len(iesire.getvalue()), 1000)

    def test_catalog_gol(self):
        self.grafic.afiseaza(PiatraModel([]).get_date_grafic())
        self.assertEqual(len(self.grafic.axa.patches), 0)
        self.assertTrue(any('gol' in text.get_text() for text in self.grafic.axa.texts))

    def test_clasa_goala_nu_afiseaza_medie_zero(self):
        model = PiatraModel([])
        model.adauga_piatra('Pretioasa', 'Rubin', 9, 4, 2)
        self.grafic.afiseaza(model.get_date_grafic())
        self.assertEqual(sum(text.get_text() == 'fără date' for text in self.grafic.axa.texts), 2)

    def test_numar_este_afisat_intreg(self):
        self.grafic.afiseaza(self.model.get_date_grafic('numar'))
        self.assertEqual([text.get_text() for text in self.grafic.axa.texts], ['10', '10', '10'])
