# Conversione Fonetica 🧠

Sistema di conversione fonetica (Major System) per la lingua italiana: uno strumento per memorizzare numeri associandoli a parole.

## Cos'è il Major System?

Il **Major System** (o sistema di conversione fonetica) è una tecnica mnemonica che associa numeri a suoni consonantici, permettendo di trasformare sequenze numeriche in sequenze di parole facili da ricordare. È uno degli strumenti più potenti per memorizzare numeri come:

- Numeri di telefono
- Date storiche
- Codici PIN
- Costanti matematiche (π, e, φ)
- Numeri di carte di creditos
- E tutto ciò che può essere convertito in cifre!

Questa tecnica raggiunge il suo massimo potenziale se abbinata alla creazione di storie buffe, paradossali e assurde così da agevolare la memorizzazione.

## Come Funziona?

Ogni cifra decimale da 0 a 9 corrisponde a uno o più suoni consonantici specifici:

| Cifra | Suoni Italiani | Esempi |
|-------|----------------|---------|
| **0** | s, z, sc(i/e) | **s**ole, **z**ero, **sc**ienza |
| **1** | t, d | **t**oro, **d**ato |
| **2** | n, gn | **n**aso, **gn**omo |
| **3** | m | **m**ano, a**mm**ore |
| **4** | r | **r**osa, ca**rr**o |
| **5** | l, gli+vocale | **l**una, fi**gli**o, me**gli**o |
| **6** | c/g dolce | **ci**ao, **ge**lo, **ce**na, pa**gi**na |
| **7** | c/g dura, k, q | **c**asa, **g**atto, **ch**iave, **q**uadro |
| **8** | f, v | **f**iore, **v**ino |
| **9** | p, b | **p**ane, **b**arca |

### ⚠️ Regole Importanti

1. **Le vocali non contano**: servono solo a formare parole pronunciabili. Questo ha come vantaggio il fatto di poter associare a un numero più parole (così da poter scegliere quella che meglio si adatta alla nostra memoria), ma, data una parola, esiste un solo numero corrispondente.
2. **Le doppie contano una sola volta**: "bello" corrisponde a 95 (non 955, come si potrebbe invece pensare)
3. **Suoni speciali italiani**:
   - `gli` + vocale = suono unico (corrisponde al numero 5): "figlio" → 85, *non* 875 e *neppure* 865, quello che conta è il suono, non le lettere che lo compongono!
   - `gli` + consonante = due suoni: "glifo" → 758
   - `gn` = suono unico (corrisponde al numero 2): "gnomo" → 23
   - `sci/sce` = suono unico (corrisponde al numero 0): "coscienza" → 7020
4. Potrebbero esserci altri dettagli che ho omesso 🫣...


## Installazione

```bash
# Clona la repository (o scaricala da web)
git clone https://github.com/MrsSAS/Conversione-Fonetica
cd conversione_fonetica

```

## Requisiti

- Assicurarsi di avere Python 3.6 o superiore

```bash

python --version

```

## Utilizzo


```bash
python conversioneFonetica.py
```

Lo script caricherà in automatico il dizionario e avvierà una sessione interattiva:

```
==============================================================
MAJOR SYSTEM ITALIANO - Conversione Fonetica
==============================================================

Comandi disponibili:
  - Inserisci un numero per trovare le parole corrispondenti
  - 'test <parola>' per vedere il numero di una parola
  - 'q' o 'quit' per uscire

> 26
============================================================
Numero: 26
Parole trovate: x
============================================================
  1. ...
  2. anice
  3. ...
  4. noce
  ...

> test mamma
'naso' -> 20

> q
Arrivederci!
```

*N.B.*
Questo è solo uno strumento per agevolare la generazione di parole a partire da un numero, ma non è assolutamente garantita la qualità delle parole generate! L'obiettivo è esclusivamente quello di trovare un riscontro tra i numeri inseriti e l'elenco dei termini presenti nel dizionario usato, ma a ciascuno spetta il compito di scegliere la parola più conveniente da memorizzare, a seconda delle proprie esigenze.

## Esempi Pratici

### Memorizzare una data: 1492 (Scoperta dell'America)

```bash
> 1492
Numero: 1492
Parole trovate: x
  1. ...
  2. ...
  3. tirapugni
  ...

```

### Memorizzare un articolo di legge: 160 Codice Civile (Diritti inderogabili)

```bash
> 160
Numero: 160
Parole trovate: x
  1. ...
  2. ...
  3. decesso
  ...

```

### Memorizzare π (pi greco): 3.14159...

Essendo una cifra piuttosto lunga, è consigliabile spezzarla in 2 o più parole:

```bash
> 314
Parole trovate: x
  1. ...
  2. ...
  3. madre
  ...

> 159
Parole trovate: x
  1. ...
  2. ...
  3. talpa
  ...

```

## Contribuire

I contributi sono benvenuti! Ecco come puoi aiutare:

1. Segnala comportamenti inattesi, bug o casi limite
2. Proponi nuove funzionalità
3. Migliora la documentazione

## Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file `LICENSE` per maggiori dettagli.

## Riconoscimenti

- Ispirato dal [Major System](https://it.wikipedia.org/wiki/Conversione_fonetica) classico
- Adattato per le peculiarità fonetiche della lingua italiana
- Grazie a [Matteo Salvo](https://www.youtube.com/watch?v=E56DGcTSBu0) per avermi fatto scoprire questa fantastica tecnica mnemonica.
- Dizionario italiano da più di 95.000 parole da: [paroleitaliane](https://github.com/napolux/paroleitaliane/blob/main/paroleitaliane/95000_parole_italiane_con_nomi_propri.txt) di [@napolux](https://github.com/napolux).

## Contatti

Per domande, suggerimenti o segnalazioni:
- Apri una [issue](https://github.com/MrsSAS/Conversione-Fonetica/issues)
- Invia una pull request

---

**Buona memorizzazione!**