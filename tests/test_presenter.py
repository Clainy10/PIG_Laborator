import unittest

from Model.model import PiatraModel
from Presenter.presenter import PiatraPresenter


class ViewFalsa:
    def __init__(self):
        self.confirmare = True
        self.actualizari_grafic = 0
        self.eroare = None

    def configureaza_actiuni(self, *callbackuri):
        self.callbackuri = callbackuri

    def afiseaza_elemente_in_cadre(self, pietre):
        self.pietre = pietre

    def actualizeaza_sortare(self, atribut, descrescator):
        self.atribut, self.descrescator = atribut, descrescator

    def afiseaza_grafic(self, date):
        self.date_grafic = date
        self.actualizari_grafic += 1

    def deschide_dialog_adaugare(self, on_salveaza, obiect_existent=None):
        self.on_salveaza, self.obiect_existent = on_salveaza, obiect_existent

    def confirma_stergere(self, nume):
        return self.confirmare

    def afiseaza_eroare(self, mesaj):
        self.eroare = mesaj


class TestPresenter(unittest.TestCase):
    def setUp(self):
        self.model, self.view = PiatraModel(), ViewFalsa()
        self.presenter = PiatraPresenter(self.model, self.view)
        self.presenter.initializeaza()

    def test_initializare_callbackuri_si_grafic(self):
        self.assertEqual(len(self.view.callbackuri), 5)
        self.assertEqual(len(self.view.pietre), 30)
        self.assertEqual(self.view.date_grafic.criteriu, 'duritate')

    def test_callback_adaugare_actualizeaza_si_graficul(self):
        self.view.callbackuri[0]()
        self.assertIsNone(self.view.on_salveaza('Pretioasa', 'Rubin', '9', '4', '2'))
        self.assertEqual(len(self.view.pietre), 31)
        self.assertEqual(self.view.date_grafic.numere, (11, 10, 10))
        self.assertEqual(self.view.actualizari_grafic, 2)

    def test_validarea_esuat_nu_actualizeaza_view(self):
        mesaj = self.presenter.adauga_obiect('Pretioasa', 'Test', '99', '3', '1')
        self.assertIsInstance(mesaj, str)
        self.assertEqual(len(self.view.pietre), 30)
        self.assertEqual(self.view.actualizari_grafic, 1)

    def test_editare_ramane_corecta_dupa_sortare(self):
        tinta = self.view.pietre[0]
        self.presenter.deschide_editare(tinta.id)
        self.presenter.sorteaza('nume')
        self.assertEqual(self.view.obiect_existent.id, tinta.id)
        self.assertIsNone(self.view.on_salveaza('Sedimentara', 'Editat', '4', '2', '50'))
        self.assertEqual(self.model.get_date_piatra(tinta.id).nume, 'Editat')
        self.assertEqual(self.view.date_grafic.numere, (9, 10, 11))

    def test_stergere_anulata_apoi_confirmata(self):
        tinta = self.view.pietre[0]
        self.view.confirmare = False
        self.presenter.sterge_obiect(tinta.id)
        self.assertEqual(len(self.view.pietre), 30)
        self.view.confirmare = True
        self.presenter.sterge_obiect(tinta.id)
        self.assertEqual(len(self.view.pietre), 29)
        self.assertEqual(self.view.date_grafic.numere, (9, 10, 10))

    def test_sortare_alterneaza_si_se_pastreaza_dupa_adaugare(self):
        self.presenter.sorteaza('duritate')
        self.assertFalse(self.view.descrescator)
        self.presenter.sorteaza('duritate')
        self.assertTrue(self.view.descrescator)
        self.presenter.adauga_obiect('Pretioasa', 'Nou', '10', '3', '1')
        self.assertEqual(self.view.pietre[0].nume, 'Nou')
        self.presenter.sorteaza('densitate')
        self.assertFalse(self.view.descrescator)

    def test_schimbare_grafic_pastrata_dupa_modificari(self):
        self.view.callbackuri[4]('numar')
        self.presenter.adauga_obiect('Magmatica', 'Nou', '6', '3', '1200')
        self.assertEqual(self.view.date_grafic.criteriu, 'numar')
        self.assertEqual(self.view.date_grafic.valori, (10, 11, 10))

    def test_criterii_invalide_nu_corup_starea(self):
        self.presenter.sorteaza('gresit')
        self.assertIsNone(self.view.atribut)
        self.presenter.schimba_grafic('gresit')
        self.assertEqual(self.view.date_grafic.criteriu, 'duritate')
        self.assertIsInstance(self.view.eroare, str)

    def test_obiect_disparut_inainte_de_salvare(self):
        tinta = self.view.pietre[0]
        self.presenter.deschide_editare(tinta.id)
        self.model.sterge_piatra(tinta.id)
        self.assertIsInstance(self.view.on_salveaza('Pretioasa', 'X', '5', '3', '1'), str)
        self.presenter.deschide_editare(tinta.id)
        self.assertIsInstance(self.view.eroare, str)

    def test_catalog_gol(self):
        presenter = PiatraPresenter(PiatraModel([]), self.view)
        presenter.initializeaza()
        self.assertEqual(self.view.pietre, ())
        self.assertEqual(self.view.date_grafic.numere, (0, 0, 0))
