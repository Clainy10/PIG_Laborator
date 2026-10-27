# Catalog de pietre — Laboratoarele 1–5

Proiect Python cu CustomTkinter, Matplotlib și arhitectură **Model–View–Presenter**.
Structura inițială `Model / Presenter / View / main.py` este păstrată.

## Pornire

Necesită Python **3.10+**, Tkinter și o sesiune grafică desktop.
Din directorul `Lab1`, instalează dependențele și pornește aplicația:

```bash
python -m venv .venv
```

Activează mediul în terminalul pe care îl folosești:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
source .venv/bin/activate
```

```bash
python -m pip install -r requirements.txt
python main.py
```

Pe Debian/Ubuntu, dacă lipsește Tkinter, instalează pachetul `python3-tk` al
sistemului. Tkinter nu se instalează prin `pip`. Dacă apare o eroare despre
`DISPLAY`, aplicația trebuie pornită într-o sesiune grafică.

Demonstrația LL1 rulează fără CustomTkinter, Matplotlib sau interfață grafică:

```bash
python main.py --terminal
```

## Structura păstrată și completările pentru LL5

| Fișier | Rol |
| --- | --- |
| `Model/Interface/interface.py` | `IPiatra`: cele șase metode abstracte de setare/primire |
| `Model/Class/baseclass.py` | `Piatra`: implementare concretă, validare comună și ID stabil |
| `Model/Class/clase_pietre.py` | `PiatraPretioasa`, `PiatraMagmatica`, `PiatraSedimentara` |
| `Model/model.py` | Lista de obiecte, generare, CRUD, sortare, calcule statistice și date pentru afișare |
| `Presenter/presenter.py` | `PiatraPresenter`: toate cazurile de utilizare și legătura Model–View; contractul `IPiatraView` |
| `View/view.py` | Fereastra, cache-ul imaginilor, cardurile CTkFrame și callback-urile |
| `View/dialog_adaugare.py` | Formularul comun de adăugare și editare |
| **`View/grafic.py`** | **Nou pentru LL5:** `GraficPietre` și `CadruGrafic`, cu integrarea Matplotlib în CTkFrame |
| **`View/imagini/`** | **Nou:** cele trei imagini reprezentative locale și proveniența lor |
| `main.py` | `MainApp`: creează și conectează obiectele, apoi pornește aplicația |
| `tests/` | Verificări automate pentru domeniu, Model, Presenter și arhitectură |

Nu s-au redenumit și nu s-au mutat fișierele aplicației inițiale.
`README.md`, `requirements.txt`, `.gitignore` și `tests/` sunt fișiere auxiliare
pentru utilizare, GitHub și verificare.

## Cum este respectat MVP

1. **View** citește valorile câmpurilor și transmite evenimentul prin callback
   către **Presenter**. Nu construiește entități și nu calculează medii.
2. **Presenter** apelează operația corespunzătoare din **Model**.
3. **Model** validează datele și actualizează lista; tot aici se calculează
   valorile pentru grafice.
4. **Presenter** solicită datele actualizate și le trimite către **View**.
5. **View** actualizează cardurile și desenează graficul primit.

Model nu importă View, Tkinter, Pillow sau Matplotlib. Presenter nu importă
implementarea View și nu accesează widget-uri. `IPiatraView` este contractul
folosit de Presenter; la teste este implementat de o View falsă.
View importă din Model doar clasele de date `DatePiatra` și `DateGrafic`,
care sunt înregistrări imuabile fără operații asupra catalogului.

Toată logica aplicației este în metode de clasă. La nivel de modul sunt doar
importuri, definiții de clase și, în `main.py`, declanșatorul standard
`if __name__ == "__main__": MainApp().run()`.
Nu există funcții libere pentru logica aplicației.

## Cerințele laboratoarelor

| Laborator | Implementare |
| --- | --- |
| LL1 | Interfață, clasă concretă, trei clase derivate, minimum trei parametri comuni, listă de 30 de obiecte: câte 10 din fiecare clasă, sortări și afișare în terminal |
| LL2 | Integrarea CustomTkinter și trei butoane pentru sortări. Afișarea istorică în CTkTextbox este înlocuită cu lista de cadre cerută ulterior la LL4 |
| LL3 | Model, View și Presenter în directoarele și fișierele inițiale, callback-uri View → Presenter → Model |
| LL4 | CTkFrame pentru fiecare piatră, adăugare prin CTkEntry/CTkOptionMenu, ștergere cu confirmare și editare |
| LL5 | Matplotlib într-o clasă distinctă de CTkFrame; calcule în Model, orchestrare și actualizare în Presenter |

Valorile inițiale sunt cele demonstrative din proiectul primit, rotunjite pentru
a evita afișarea erorilor de reprezentare în virgulă mobilă. Nu sunt măsurători
științifice reale ale specimenelor din imagini.

## Funcționalități

- În fila **Colecție**: 30 de carduri, cu imagine, nume, tip, duritate, densitate,
  parametrul specific, editare și ștergere.
- Parametrul specific este caratul pentru prețioase, temperatura de topire
  pentru magmatice și porozitatea pentru sedimentare.
- **Adaugă piatră** deschide formularul; **Editează** precompletează același formular.
  Tipul poate fi schimbat, iar eticheta parametrului specific se actualizează.
- Un clic pe **Nume / Duritate / Densitate** sortează crescător. Următorul clic
  pe același criteriu inversează ordinea. Sortarea activă rămâne aplicată după modificări.
- Editarea și ștergerea folosesc **ID-uri stabile**, nu indecși care se schimbă la sortare.
- În fila **Grafice**, selectorul schimbă între duritate medie pe clasă,
  densitate medie pe clasă și număr de pietre pe clasă.
- Graficul se actualizează după adăugare, editare și ștergere, păstrând criteriul ales.
- Dacă o clasă nu mai are obiecte, media ei este `None` și apare „fără date”.
  Numărul de obiecte este în continuare zero. Catalogul complet gol are un mesaj dedicat.
- Imaginile sunt încărcate o singură dată din `View/imagini/`, fără cereri de rețea.
  Lipsa unei imagini nu blochează operațiile asupra catalogului.

### Validare

Nume obligatoriu, maximum 100 de caractere; duritate Mohs între 1 și 10;
densitate și carate pozitive; temperatură de topire întreagă și pozitivă;
porozitate între 0 și 100%. Sunt acceptate punctul și virgula zecimală.
NaN, infinit și valori nenumerice sunt respinse. Erorile sunt afișate în formular.
Editările invalide nu schimbă parțial obiectele.

### Limite intenționate

Datele rămân în memorie, la fel ca în proiectul inițial; repornirea restaurează
cele 30 de obiecte demo. Nu s-au adăugat bază de date, autentificare sau persistență.
`get_toate_pietrele()` întoarce o copie a listei; entitățile păstrează setterele cerute
la LL1. View primește doar înregistrări imuabile, nu aceste entități.

## Teste

Testele pentru Model și Presenter nu au nevoie de bibliotecile grafice:

```bash
python -m unittest discover -s tests -v
python -m compileall -q main.py Model Presenter View
```

Acoperă moștenirea, interfața, getterele/setterele, cele 30 de obiecte,
validarea, sortările, CRUD, identitatea după sortare, recalcularea statisticilor,
catalogul gol și separarea MVP. Verificarea grafică este descrisă separat în
`VERIFICARE.md`.

## Publicare în propriul repository GitHub

Poți numi repository-ul `python-mvp-pietre`. Creează-l din
[GitHub — New repository](https://github.com/new), alege vizibilitatea dorită
și lasă-l gol: README-ul și `.gitignore` sunt deja în acest proiect.
Nu selecta o licență fără să decizi ce permisiuni vrei să oferi asupra codului.

Din directorul extras **Lab1**:

```bash
git init
git branch -M main
git add .
git commit -m "Completeaza LL5: MVP, imagini locale si grafice Matplotlib"
git remote add origin https://github.com/UTILIZATOR/python-mvp-pietre.git
git push -u origin main
```

Înlocuiește `UTILIZATOR` și numele repository-ului cu valorile tale.
Dacă repository-ul conține deja commit-uri, clonează-l întâi și copiază în el
conținutul directorului Lab1, apoi fă commit; nu forța publicarea peste istoricul existent.
Nu încărca `.venv` sau `__pycache__`. Nu încărca arhiva ZIP drept codul repository-ului;
încarcă fișierele extrase.

## Documentație de referință

- [Matplotlib — integrare în Tk](https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html)
- [Matplotlib — ghid de început](https://matplotlib.org/stable/users/explain/quick_start.html)
- [CustomTkinter — CTkFrame](https://customtkinter.tomschimansky.com/documentation/widgets/frame/)
- [GitHub — crearea unui repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/quickstart-for-repositories)
