import pickle
import os
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
        """Verifica se il dizionario è stato modificato dopo la cache."""
        if not os.path.exists(self.cache_path):
            return True
        
        dict_mtime = os.path.getmtime(self.dizionario_path)
        cache_mtime = os.path.getmtime(self.cache_path)
        
        return dict_mtime > cache_mtime

        
    def parola_a_numero(self, parola):
        """Converte una parola italiana in numero secondo il Major System."""
        parola = parola.lower()
        numero = ''
        i = 0
        ultimo_numero = None  # Per gestire le doppie
        
        while i < len(parola):
            # Gestione sequenze di 3+ caratteri per "gli"
            if i + 2 < len(parola):
                # Controlla se abbiamo "gli" seguito da vocale o fine parola
                if parola[i:i+2] == 'gl':
                    if i + 2 < len(parola) and parola[i+2] in 'aeiouy':
                        # "gli" + vocale = suono unico (5)
                        if ultimo_numero != '5':
                            numero += '5'
                            ultimo_numero = '5'
                        i += 3  # Salta g, l, vocale
                        continue
                    elif i + 2 == len(parola) - 1 and parola[i+2] == 'i':
                        # "gli" a fine parola = suono unico (5)
                        if ultimo_numero != '5':
                            numero += '5'
                            ultimo_numero = '5'
                        i += 3
                        continue
                    # Altrimenti "gl" + consonante = due suoni separati (continua normalmente)
                
                # sci/sce = 0
                tri = parola[i:i+3]
                if tri in ['sci', 'sce']:
                    if ultimo_numero != '0':
                        numero += '0'
                        ultimo_numero = '0'
                    i += 3
                    continue
            
            # Controlla "gli" a fine parola (2 caratteri rimanenti)
            if i + 2 == len(parola) and parola[i:i+3] == 'gli':
                if ultimo_numero != '5':
                    numero += '5'
                    ultimo_numero = '5'
                i += 3
                continue
            
            # Gestione sequenze di 2 caratteri
            if i + 1 < len(parola):
                bi = parola[i:i+2]
                
                # gn = 2
                if bi == 'gn':
                    if ultimo_numero != '2':
                        numero += '2'
                        ultimo_numero = '2'
                    i += 2
                    continue
                
                # ch = 7 (suono duro)
                if bi in ['ch', 'gh']:
                    if ultimo_numero != '7':
                        numero += '7'
                        ultimo_numero = '7'
                    i += 2
                    continue
                
                # ci/ce/gi/ge = 6 (suono dolce)
                if bi in ['ci', 'ce', 'gi', 'ge']:
                    if ultimo_numero != '6':
                        numero += '6'
                        ultimo_numero = '6'
                    i += 2
                    continue
            
            # Gestione caratteri singoli
            char = parola[i]
            
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
            # Controllo contesto per c/g
            elif char in ['c', 'g']:
                if i + 1 < len(parola):
                    next_char = parola[i + 1]
                    if next_char in ['e', 'i']:
                        # Già gestito sopra come sequenza
                        if ultimo_numero != '6':
                            numero += '6'
                            ultimo_numero = '6'
                        i += 1
                    else:
                        # Suono duro
                        if ultimo_numero != '7':
                            numero += '7'
                            ultimo_numero = '7'
                else:
                    # Fine parola, probabile suono duro
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
    
    def cerca_parole(self, numero):
        """Trova tutte le parole che corrispondono a un numero."""
        numero_str = str(numero)
        parole = self.parole_per_numero.get(numero_str, [])
        return sorted(parole)
    
    def mostra_risultati(self, numero, max_risultati=100):
        """Mostra i risultati della ricerca."""
        parole = self.cerca_parole(numero)
        
        print(f"\n{'='*60}")
        print(f"Numero: {numero}")
        print(f"Parole trovate: {len(parole)}")
        print(f"{'='*60}")
        
        if parole:
            for i, parola in enumerate(parole[:max_risultati], 1):
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
        print("  - 'test <parola>' per vedere il numero di una parola, anche inventata")
        print("  - 'q' o 'quit' per uscire")
        print()
        
        while True:
            try:
                comando = input("\n> ").strip()
                
                if comando.lower() in ['q', 'quit', 'esci']:
                    print("Arrivederci!")
                    break
                
                if comando.lower().startswith('test '):
                    parola = comando[5:].strip()
                    numero = self.parola_a_numero(parola)
                    if numero:
                        print(f"'{parola}' -> {numero}")
                    else:
                        print(f"'{parola}' non produce alcun numero (solo vocali?)")
                    continue
                
                if comando.isdigit():
                    self.mostra_risultati(comando)
                else:
                    print("Inserisci un numero valido o 'test <parola>' per testare una parola.")
                    
            except KeyboardInterrupt:
                print("\n\nInterrotto. Arrivederci!")
                break
            except Exception as e:
                print(f"Errore: {e}")


# Esempio di utilizzo
if __name__ == "__main__":
    # Crea l'istanza del sistema
    ms = MajorSystemIT('dizionario.txt')
    
    # Carica il dizionario
    ms.carica_dizionario()
    
    # Esempi di test
    print("\nEsempi di conversione:")
    test_parole = ['casa', 'zerbino', 'scienza', 'gatto', 'gnomo', 'figlio', 'ciao', 'chiave', 'matta', 'palla', 'carro', 'glifo', 'glicerina', 'aglio', 'cuore', 'quadro', 'soqquadro', 'acqua']
    for parola in test_parole:
        print(f"{parola:12s} -> {ms.parola_a_numero(parola)}")
    
    # Avvia modalità interattiva
    ms.modalita_interattiva()