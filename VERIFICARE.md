# Verificarea versiunii LL5

Verificată la 27 octombrie 2026.

## Rezultate

- **41 de teste Python trecute**, fără teste sărite în rularea cu dependențele grafice disponibile.
- Model și Presenter: validare, moștenire, getter/setter, listă de 30 de obiecte,
  CRUD, sortări, ID stabil, schimbarea tipului și actualizarea statisticilor.
- Arhitectură: fișierele originale există; Model și Presenter nu importă
  biblioteci grafice sau implementarea View; logica aplicației este în clase.
- Matplotlib: graficele au fost desenate cu backend-ul **Agg**, pentru toți cei
  trei indicatori; au fost verificate valorile barelor, etichetele, clasele fără
  obiecte, catalogul gol și reutilizarea axei. Graficul inițial a fost inspectat vizual.
- Imagini: cele trei fișiere locale sunt încărcate în CTkImage și reutilizate;
  lipsa imaginilor este tratată fără blocarea inițializării cache-ului.
- `python main.py --terminal`: 90 de afișări, adică 30 de obiecte pentru fiecare
  dintre cele trei criterii; ordinea catalogului este restaurată la final.
- Toate modulele aplicației au trecut verificarea de compilare Python.

## Limite ale verificării

Fereastra CustomTkinter și dialogurile nu au fost verificate vizual în această
rulare. Importurile grafice și randarea Matplotlib fără afișaj au fost verificate,
dar serverul grafic de test nu a putut fi inițializat complet. Aceste rezultate
nu reprezintă o verificare integrală a interacțiunilor desktop pe Windows/Linux/macOS.

Simularea din conversație este o reproducere separată în JavaScript. Logica
operațiilor și actualizarea graficelor au fost verificate într-un mediu DOM minimal,
fără un browser complet. Simularea nu execută codul Python sau widget-urile CTk.
Paginarea cu șase obiecte în simulare înlocuiește lista derulabilă a aplicației desktop.

## Verificare pe calculatorul tău

1. Instalează dependențele și rulează `python main.py`.
2. Verifică imaginile și cele 30 de carduri din fila Colecție.
3. Apasă fiecare buton de sortare de două ori și verifică schimbarea sensului.
4. Adaugă o piatră cu valori valide; verifică formularul și cu duritate invalidă.
5. Editează o piatră după sortare și schimbă-i tipul.
6. Anulează o ștergere, apoi confirmă alta.
7. În fila Grafice, schimbă cei trei indicatori și verifică actualizarea după CRUD.
8. Redimensionează fereastra până la dimensiunea minimă și verifică lizibilitatea.

Pentru a rerula testele: `python -m unittest discover -s tests -v`.
Fără dependențele grafice, testele pentru grafice și imagini se raportează ca
sărite; testele Model/Presenter/arhitectură pot rula separat.
