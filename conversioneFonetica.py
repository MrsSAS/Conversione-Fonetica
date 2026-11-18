import pickle
import os
import readline
from collections import defaultdict

class MajorSystemIT:
    """
    Sistema mnemonico della conversione fonetica per l'italiano.

    Mappatura numero -> suono:
    0 = s, z, sc(e/i)
    1 = t, d
    2 = n, gn
    3 = m
    4 = r
    5 = l, gli+vocale o fine parola
    6 = c/g/j dolce (ci, gi, ce, ge...)
    7 = c/g dura (k, ch, gh, ca, ga, cu, co, gu, go, q)
    8 = f, v
    9 = p, b
    """

    def __init__(self, dizionario_path='dizionario.txt'):
        self.dizionario_path = dizionario_path
        self.cache_path = dizionario_path + '.cache'
        self.parole_per_numero = defaultdict(list)

    def _dizionario_modificato(self):
        """Verifica se il dizionario o lo script sono stati modificati dopo la cache."""
        if not os.path.exists(self.cache_path):
            return True

        script_path = __file__
        dict_mtime = os.path.getmtime(self.dizionario_path)
        cache_mtime = os.path.getmtime(self.cache_path)

        if dict_mtime > cache_mtime:
            return True

        if os.path.exists(script_path) and os.path.getmtime(script_path) > cache_mtime:
            return True

        return False


    def parola_a_numero(self, parola):
        """Converte una parola italiana in numero secondo il Major System."""
        parola = parola.lower()
        numero = ''
        i = 0
        ultimo_numero = None  # Per gestire le doppie

        VOCALI = set('aeiouyàâèéìòôù')
        VOCALI_PALATALI = set('eièéìíî')

        while i < len(parola):
            char = parola[i]

            # 1. Trigrammi specifici
            # cch / ggh: occlusiva velare geminata (suono duro = 7)
            if i + 2 < len(parola) and parola[i:i+3] in ['cch', 'ggh']:
                if ultimo_numero != '7':
                    numero += '7'
                    ultimo_numero = '7'
                i += 3
                continue

            # 2. Bigrammi specifici
            if i + 1 < len(parola):
                bi = parola[i:i+2]

                # gn = 2 (suono unico)
                if bi == 'gn':
                    if ultimo_numero != '2':
                        numero += '2'
                        ultimo_numero = '2'
                    i += 2
                    continue

                # ch / gh = 7 (suono duro)
                if bi in ['ch', 'gh']:
                    if ultimo_numero != '7':
                        numero += '7'
                        ultimo_numero = '7'
                    i += 2
                    continue

                # cq = 7 (rafforzamento di q, suono duro)
                if bi == 'cq':
                    if ultimo_numero != '7':
                        numero += '7'
                        ultimo_numero = '7'
                    i += 2
                    continue

                # cc:
                # - se seguito da vocale palatale (e, i...) -> suono dolce geminato (6)
                # - altrimenti -> suono duro geminato (7)
                if bi == 'cc':
                    if i + 2 < len(parola) and parola[i+2] in VOCALI_PALATALI:
                        if ultimo_numero != '6':
                            numero += '6'
                            ultimo_numero = '6'
                    else:
                        if ultimo_numero != '7':
                            numero += '7'
                            ultimo_numero = '7'
                    i += 2
                    continue

                # gg:
                # - se seguito da vocale palatale (e, i...) -> suono dolce geminato (6)
                # - altrimenti -> suono duro geminato (7)
                if bi == 'gg':
                    if i + 2 < len(parola) and parola[i+2] in VOCALI_PALATALI:
                        if ultimo_numero != '6':
                            numero += '6'
                            ultimo_numero = '6'
                    else:
                        if ultimo_numero != '7':
                            numero += '7'
                            ultimo_numero = '7'
                    i += 2
                    continue

                # gli:
                # - se 'gl' è seguito da 'i' E (fine parola O altra vocale) -> laterale palatale (5)
                #   (consumiamo 'gl', lasciando 'i' e le vocali successive per azzerare ultimo_numero)
                # - altrimenti (es. 'gl' + altra vocale come 'globo', o 'gli' + consonante come 'glifo')
                #   sono suoni separati g (7) e l (5)
                if bi == 'gl' and i + 2 < len(parola) and parola[i+2] == 'i':
                    if i + 3 == len(parola) or parola[i+3] in VOCALI:
                        if ultimo_numero != '5':
                            numero += '5'
                            ultimo_numero = '5'
                        i += 2
                        continue

                # sc prima di vocale palatale (e, i...) = 0 (suono unico /ʃ/)
                # (consumiamo 'sc', lasciando la vocale successiva per azzerare ultimo_numero)
                if bi == 'sc' and i + 2 < len(parola) and parola[i+2] in VOCALI_PALATALI:
                    if ultimo_numero != '0':
                        numero += '0'
                        ultimo_numero = '0'
                    i += 2
                    continue

            # 3. Caratteri singoli
            if char in ['s', 'z']:
                if ultimo_numero != '0':
                    numero += '0'
                    ultimo_numero = '0'
            elif char in ['t', 'd']:
                if ultimo_numero != '1':
                    numero += '1'
                    ultimo_numero = '1'
            elif char == 'n':
                if ultimo_numero != '2':
                    numero += '2'
                    ultimo_numero = '2'
            elif char == 'm':
                if ultimo_numero != '3':
                    numero += '3'
                    ultimo_numero = '3'
            elif char == 'r':
                if ultimo_numero != '4':
                    numero += '4'
                    ultimo_numero = '4'
            elif char == 'l':
                if ultimo_numero != '5':
                    numero += '5'
                    ultimo_numero = '5'
            elif char in ['c', 'g']:
                # c o g prima di vocale palatale (e, i...) -> dolce (6)
                # altrimenti -> duro (7)
                if i + 1 < len(parola) and parola[i+1] in VOCALI_PALATALI:
                    if ultimo_numero != '6':
                        numero += '6'
                        ultimo_numero = '6'
                else:
                    if ultimo_numero != '7':
                        numero += '7'
                        ultimo_numero = '7'
            elif char == 'j':
                if ultimo_numero != '6':
                    numero += '6'
                    ultimo_numero = '6'
            elif char in ['k', 'q']:
                if ultimo_numero != '7':
                    numero += '7'
                    ultimo_numero = '7'
            elif char in ['f', 'v']:
                if ultimo_numero != '8':
                    numero += '8'
                    ultimo_numero = '8'
            elif char in ['p', 'b']:
                if ultimo_numero != '9':
                    numero += '9'
                    ultimo_numero = '9'
            else:
                # Vocali e altre lettere azzerano l'ultimo numero
                ultimo_numero = None

            i += 1

        return numero if numero else None

    def carica_dizionario(self):
        """Carica il dizionario (dalla cache o lo rigenera) e crea l'indice numero -> parole."""

        # Prova a caricare dalla cache
        if os.path.exists(self.cache_path) and not self._dizionario_modificato():
            try:
                with open(self.cache_path, 'rb') as f:
                    self.parole_per_numero = pickle.load(f)
                print(f"Ho trovato {len(self.parole_per_numero)} sequenze numeriche.")
                return
            except Exception as e:
                print(f"Errore nel caricamento cache: {e}. Ricostruisco...")

        print("Caricamento dizionario in corso...")

        try:
            with open(self.dizionario_path, 'r', encoding='utf-8') as f:
                for linea in f:
                    parola = linea.strip()
                    if not parola: continue
                    numero = self.parola_a_numero(parola)
                    if not numero: continue
                    self.parole_per_numero[numero].append(parola)

            # Salva la cache
            with open(self.cache_path, 'wb') as f:
                pickle.dump(dict(self.parole_per_numero), f)
            print(f"Dizionario caricato e cache salvata! {len(self.parole_per_numero)} sequenze.")

        except FileNotFoundError:
            print(f"Errore: file '{self.dizionario_path}' non trovato.")

        except Exception as e:
            print(f"Errore durante il caricamento: {e}")

    def cerca_parole(self, numero, mode="esatta"):
        """
        Trova tutte le parole che corrispondono a un numero.

        mode:
            "esatta"    -> corrispondenza esatta
            "prefisso"   -> la sequenza numerica inizia con numero
            "suffisso"   -> la sequenza numerica termina con numero
            "contiene" -> la sequenza numerica contiene numero
        """
        numero_str = str(numero)

        if mode == "esatta":
            parole = self.parole_per_numero.get(numero_str, [])
        else:
            parole = []

            for chiave, lista_parole in self.parole_per_numero.items():
                if mode == "prefisso" and chiave.startswith(numero_str):
                    parole.extend(lista_parole)

                elif mode == "suffisso" and chiave.endswith(numero_str):
                    parole.extend(lista_parole)

                elif mode == "contiene" and numero_str in chiave:
                    parole.extend(lista_parole)

        return sorted(parole)

    def mostra_risultati(self, numero, max_risultati=1000, mode="esatta"):
        """Mostra i risultati della ricerca."""

        parole = self.cerca_parole(numero, mode=mode)

        descrizioni = {
            "esatta": "esatte per",
            "prefisso": "che iniziano con",
            "suffisso": "che terminano con",
            "contiene": "che contengono"
        }

        modo = descrizioni.get(mode, "corrispondenti a")

        if mode == "prefisso":
            comando_visualizzato = f"{numero}+"
        elif mode == "suffisso":
            comando_visualizzato = f"+{numero}"
        elif mode == "contiene":
            comando_visualizzato = f"+{numero}+"
        else:
            comando_visualizzato = str(numero)

        print(f"\n{'='*60}")
        print(f"Numero: {comando_visualizzato}")
        print(f"Parole {modo} {numero}: {len(parole)}")
        print(f"{'='*60}")

        if parole:
            for i, parola in enumerate(parole[:max_risultati], 1):
                if mode != "esatta":
                    num = self.parola_a_numero(parola)
                    print(f"{i:3d}. {parola:20s} ({num})")
                else:
                    print(f"{i:3d}. {parola}")

            if len(parole) > max_risultati:
                print(f"\n... e altre {len(parole) - max_risultati} parole.")
        else:
            print("Nessuna parola trovata per questo numero.")

    def modalita_interattiva(self):
        """Modalità interattiva per cercare parole."""
        print("\n" + "="*60)
        print("MAJOR SYSTEM ITALIANO - Conversione Fonetica")
        print("="*60)
        print("\nComandi disponibili:")
        print("  - Inserisci un numero per trovare le parole corrispondenti")
        print("  - Inserisci un numero seguito da '+' per trovare le parole che iniziano con quel numero")
        print("  - Inserisci '+' seguito da un numero per trovare le parole che terminano con quel numero")
        print("  - Inserisci '+' all'inizio e alla fine di un numero per trovare le parole che contengono quel numero")
        print("  - Inserisci una parola per vedere il numero corrispondente")
        print("  - Premi 'ctrl + c' oppure '!' per uscire")
        print()

        while True:
            try:

                comando = input("\n> ").strip()
                if comando == "!":
                    print("\nInterrotto. Arrivederci!")
                    break

                if comando.isalpha():
                    parola = comando.strip()
                    numero = self.parola_a_numero(parola)
                    if numero:
                        print(f"'{parola}' -> {numero}")
                    else:
                        print(f"'{parola}', come da regole, non produce alcun numero.")
                    continue

                # Determina la modalità di ricerca
                mode = "esatta"

                if comando.startswith('+') and comando.endswith('+'):
                    # +23+
                    mode = "contiene"
                    comando = comando[1:-1].strip()

                elif comando.startswith('+'):
                    # +23
                    mode = "suffisso"
                    comando = comando[1:].strip()

                elif comando.endswith('+'):
                    # 23+
                    mode = "prefisso"
                    comando = comando[:-1].strip()

                if comando.isdigit():
                    self.mostra_risultati(comando, mode=mode)
                else:
                    print(
                        "Inserisci un comando valido:\n"
                        "  23    = esatto\n"
                        "  23+   = inizia con\n"
                        "  +23   = termina con\n"
                        "  +23+  = contiene"
                    )

            except KeyboardInterrupt:
                print("\nInterrotto. Arrivederci!")
                break
            except Exception as e:
                print(f"Errore, segnale non valido: {e}")


# Esempio di utilizzo
if __name__ == "__main__":
    # Crea l'istanza del sistema
    ms = MajorSystemIT('dizionario.txt')

    # Carica il dizionario
    ms.carica_dizionario()
    # Avvia modalità interattiva
    ms.modalita_interattiva()
