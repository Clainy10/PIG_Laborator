import io
import unittest
from contextlib import redirect_stdout
from dataclasses import FrozenInstanceError

from Model.Class.baseclass import Piatra
from Model.Class.clase_pietre import PiatraMagmatica, PiatraPretioasa, PiatraSedimentara
from Model.Interface.interface import IPiatra
from Model.model import PiatraModel


class TestModel(unittest.TestCase):
    def setUp(self):
        self.model = PiatraModel()

    def test_interfata_si_mostenire(self):
        self.assertIsInstance(Piatra('Bază', 5, 3), IPiatra)
        for clasa in (PiatraPretioasa, PiatraMagmatica, PiatraSedimentara):
            self.assertTrue(issubclass(clasa, Piatra))
        with self.assertRaises(TypeError):
            IPiatra()

    def test_getteri_si_setteri_ll1(self):
        piatra = Piatra('Test', 5, 3)
        piatra.set_nume(' Nume nou ')
        piatra.set_duritate(7)
        piatra.set_densitate(2.5)
        self.assertEqual((piatra.get_nume(), piatra.get_duritate(), piatra.get_densitate()),
                         ('Nume nou', 7, 2.5))
        with self.assertRaises(ValueError):
            piatra.set_duritate(12)
        self.assertEqual(piatra.get_duritate(), 7)

    def test_30_obiecte_cate_10_din_fiecare_clasa(self):
        pietre = self.model.get_toate_pietrele()
        self.assertIsInstance(pietre, list)
        self.assertEqual(len(pietre), 30)
        self.assertEqual(len({p.get_id() for p in pietre}), 30)
        for clasa in (PiatraPretioasa, PiatraMagmatica, PiatraSedimentara):
            self.assertEqual(sum(isinstance(p, clasa) for p in pietre), 10)

    def test_lista_returnata_nu_permite_stergerea_din_model(self):
        lista = self.model.get_toate_pietrele()
        lista.clear()
        self.assertEqual(len(self.model.get_toate_pietrele()), 30)

    def test_date_pentru_view_sunt_imuabile(self):
        with self.assertRaises(FrozenInstanceError):
            self.model.get_date_lista()[0].nume = 'Modificat'

    def test_adaugare_cu_virgula_zecimala(self):
        self.model.adauga_piatra('Pretioasa', ' Rubin ', '9', '4,1', '2,5')
        piatra = self.model.get_date_lista()[-1]
        self.assertEqual((piatra.nume, piatra.densitate, piatra.extra), ('Rubin', 4.1, 2.5))

    def test_validare_parametri(self):
        cazuri = [('Pretioasa', '', 5, 3, 1), ('Alt tip', 'X', 5, 3, 1),
                  ('Pretioasa', 'X', 0, 3, 1), ('Pretioasa', 'X', 11, 3, 1),
                  ('Pretioasa', 'X', 'nan', 3, 1), ('Pretioasa', 'X', 5, 'inf', 1),
                  ('Pretioasa', 'X', 5, -1, 1), ('Pretioasa', 'X', 5, 3, 0),
                  ('Magmatica', 'X', 5, 3, 1200.5), ('Magmatica', 'X', 5, 3, -10),
                  ('Sedimentara', 'X', 5, 3, 101), ('Sedimentara', 'X', 5, 3, -1),
                  ('Pretioasa', 'X', True, 3, 1), ('Pretioasa', 'X' * 101, 5, 3, 1)]
        for caz in cazuri:
            with self.subTest(caz=caz), self.assertRaises(ValueError):
                self.model.adauga_piatra(*caz)
        self.assertEqual(len(self.model.get_toate_pietrele()), 30)

    def test_limite_porozitate(self):
        for valoare in (0, 100):
            self.model.adauga_piatra('Sedimentara', 'Test', 5, 3, valoare)
        self.assertEqual(len(self.model.get_toate_pietrele()), 32)

    def test_id_pastrat_la_editare_si_schimbare_tip(self):
        id_piatra = self.model.get_date_lista()[0].id
        self.model.editeaza_piatra(id_piatra, 'Sedimentara', 'Schimbat', 4, 2.5, 30)
        date = self.model.get_date_piatra(id_piatra)
        self.assertEqual((date.id, date.tip, date.nume), (id_piatra, 'Sedimentara', 'Schimbat'))
        self.assertEqual(len(self.model.get_toate_pietrele()), 30)

    def test_editare_invalida_este_atomica(self):
        vechi = self.model.get_date_lista()[0]
        with self.assertRaises(ValueError):
            self.model.editeaza_piatra(vechi.id, 'Sedimentara', 'Schimbat', 4, 2.5, 999)
        self.assertEqual(self.model.get_date_piatra(vechi.id), vechi)

    def test_stergere_dupa_sortare(self):
        tinta = self.model.get_date_lista()[0]
        self.model.sorteaza_dupa('nume')
        self.model.sterge_piatra(tinta.id)
        self.assertNotIn(tinta.id, [p.id for p in self.model.get_date_lista()])
        self.assertEqual(len(self.model.get_toate_pietrele()), 29)

    def test_id_inexistent(self):
        with self.assertRaises(ValueError):
            self.model.sterge_piatra('lipsa')
        with self.assertRaises(ValueError):
            self.model.get_date_piatra('lipsa')

    def test_sortari_pe_toti_parametrii(self):
        for atribut in ('nume', 'duritate', 'densitate'):
            for desc in (False, True):
                with self.subTest(atribut=atribut, desc=desc):
                    self.model.sorteaza_dupa(atribut, desc)
                    valori = [getattr(p, atribut) for p in self.model.get_date_lista()]
                    cheie = str.casefold if atribut == 'nume' else None
                    self.assertEqual(valori, sorted(valori, key=cheie, reverse=desc))

    def test_criterii_invalide(self):
        with self.assertRaises(ValueError):
            self.model.sorteaza_dupa('altceva')
        with self.assertRaises(ValueError):
            self.model.get_date_grafic('altceva')

    def test_date_grafice_initiale(self):
        date = self.model.get_date_grafic('duritate')
        self.assertEqual(date.numere, (10, 10, 10))
        for real, asteptat in zip(date.valori, (8.95, 6.55, 3.55)):
            self.assertAlmostEqual(real, asteptat)
        for real, asteptat in zip(self.model.get_date_grafic('densitate').valori, (3.555, 2.71, 2.355)):
            self.assertAlmostEqual(real, asteptat)
        self.assertEqual(self.model.get_date_grafic('numar').valori, (10, 10, 10))

    def test_grafic_recalculat_dupa_crud(self):
        self.model.adauga_piatra('Pretioasa', 'Rubin', 10, 4, 2)
        date = self.model.get_date_grafic('duritate')
        self.assertEqual(date.numere, (11, 10, 10))
        self.assertAlmostEqual(date.valori[0], (89.5 + 10) / 11)
        id_piatra = self.model.get_date_lista()[-1].id
        self.model.editeaza_piatra(id_piatra, 'Sedimentara', 'Calcar nou', 2, 2, 10)
        self.assertEqual(self.model.get_date_grafic('numar').numere, (10, 10, 11))
        self.model.sterge_piatra(id_piatra)
        self.assertEqual(self.model.get_date_grafic('numar').numere, (10, 10, 10))

    def test_grafic_fara_date_nu_inventeaza_medii_zero(self):
        model = PiatraModel([])
        self.assertEqual(model.get_date_grafic('duritate').valori, (None, None, None))
        self.assertEqual(model.get_date_grafic('numar').valori, (0, 0, 0))
        model.adauga_piatra('Pretioasa', 'X', 5, 3, 1)
        self.assertEqual(model.get_date_grafic('duritate').valori, (5, None, None))

    def test_sortari_terminal_nu_schimba_ordinea_catalogului(self):
        inainte = self.model.get_date_lista()
        iesire = io.StringIO()
        with redirect_stdout(iesire):
            self.model.afiseaza_sortari_terminal()
        self.assertEqual(iesire.getvalue().count('Nume:'), 90)
        self.assertEqual(self.model.get_date_lista(), inainte)

    def test_id_duplicat_respins(self):
        piatra = self.model.get_toate_pietrele()[0]
        with self.assertRaises(ValueError):
            PiatraModel([piatra, piatra])
