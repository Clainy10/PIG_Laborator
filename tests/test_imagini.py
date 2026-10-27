import unittest
from unittest.mock import patch


class TestImagini(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from View.view import CacheImagini
        except ImportError as exc:
            raise unittest.SkipTest(f'Dependențe grafice indisponibile: {exc}') from exc
        cls.ClasaCache = CacheImagini

    def test_imagini_incarcate_si_reutilizate(self):
        cache = self.ClasaCache()
        self.assertEqual(cache.lipsa, [])
        for tip in ('Pretioasa', 'Magmatica', 'Sedimentara'):
            self.assertIsNotNone(cache.obtine(tip))
            self.assertIs(cache.obtine(tip), cache.obtine(tip))

    def test_imagini_lipsa_nu_blocheaza_aplicatia(self):
        with patch('View.view.Image.open', side_effect=FileNotFoundError('Test')):
            with self.assertLogs('View.view', level='WARNING'):
                cache = self.ClasaCache()
        self.assertEqual(len(cache.lipsa), 3)
        self.assertIsNone(cache.obtine('Pretioasa'))
