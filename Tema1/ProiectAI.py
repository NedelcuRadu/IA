import sys
import os
import time
from heapq import heapify, heappop, heappush
from multiset import *

globalMaxNoduri = 0
maxNoduri = 0
if len(sys.argv) != 5:
    print('Usage: python ProiectAI.py cale_folder_intrare cale_folder_iesire nr_sol timp_timeout')
    print('Ex: python ProiectAI.py AIInput AIOutput 4 10')


def binSearch(val, array, cost):
    '''

    :param val: valoarea cautata
    :param array: lista cu obiecte
    :param cost: functie care primeste ca parametru un obiect din array si returneaza o valoare
    :return: indexul valorii daca exista, cel mai mare index mai mic decat valoarea altfel
    '''
    i = 0
    step = 1
    max = len(array)
    while step < max:
        step *= 2
    while step:
        if i + step < max and cost(array[i + step]) < val:
            i += step
        step //= 2
    return i + 1


class NodParcurgere:
    def __lt__(self, other):
        if self.f == other.f:
            return self.g > other.g
        return self.f < other.f

    def __eq__(self, other):
        return self.info == other.info

    def __hash__(self):
        return hash((repr(self.info), self.parinte, self.g, self.h, self.f, self.id))

    def __init__(self, info, parinte, cost=0, h=0, id=0,
                 mutare=None):  # mutare e pentru a putea afisa eficient ce linii/coloane am taiat
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost
        self.h = h
        self.f = self.g + self.h
        self.id = id
        self.mutare = mutare

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, f, fullInfo=True):  # scrie si nodul
        l = self.obtineDrum()
        for nod in l:
            f.write(f"Nodul cu id: {nod.id}\n")
            if fullInfo:
                f.write(str(nod))
        f.write(f"Cost: {self.g}\n")
        f.write(f"Lungime: {len(l)}\n")

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return sir

    def __str__(self):
        sir = ""
        for linie in self.info:
            sir += linie + '\n'
        sir += '\n'
        try:
            tip, start, nr = self.mutare
        except:
            return sir
        sir += 'Am taiat '
        if tip == 'l':
            if nr == 0:
                sir += f"linia {start}"
            else:
                sir += f"liniile "
                for k in range(start, start + nr + 1):
                    sir += str(k) + " "
        else:
            if nr == 0:
                sir += f"coloana {start}"
            else:
                sir += f"coloanele "
                for k in range(start, start + nr + 1):
                    sir += str(k) + " "
        sir += '\n'
        return sir


class Graph:  # graful problemei
    def __init__(self, nume_fisier):
        '''

        :param nume_fisier: calea catre fisierul de input

        Citeste input-ul si seteaza starile de start/scopurile
        '''
        # De modificat in functie de problema - DONE
        g = open(nume_fisier, 'r')
        inputFisier = g.readlines()
        indiceSplit = 0
        for i in range(len(inputFisier)):  # Parcurg liniile citite, caut linia vida si elimin \n de la final
            if len(inputFisier[i]) == 1:
                indiceSplit = i
            inputFisier[i] = inputFisier[i].strip()
        if indiceSplit == 0:
            print(f"Date de intrare invalide in fisierul {nume_fisier}")
            exit()

        stareInitiala = inputFisier[:indiceSplit]
        stareFinala = inputFisier[indiceSplit + 1:]
        self.start = stareInitiala
        self.scopuri = [stareFinala]
        self.final = Multiset()
        initialM = len(stareInitiala[0])
        finalM = len(stareFinala[0])
        temp = Multiset()
        for linie in stareInitiala:
            if len(linie) != initialM:
                print(f"Date de intrare invalide in fisierul {nume_fisier}")
                self.ok = False
                return
            temp.update(linie)
        for linie in stareFinala:  # Fac un multiset cu elementele din starea finala
            if len(linie) != finalM:
                print(f"Date de intrare invalide in fisierul {nume_fisier}")
                self.ok = False
                return
            self.final.update(linie)
        g.close()
        if not temp >= self.final:  # Daca in starea initiala nu apar toate caracterele din starea finala (asta cuprinde si cazul in care nu se respecta nr de linii/coloane
            print(f"Nu se poate ajunge in starea finala in fisierul {nume_fisier}")
            self.ok = False
            return
        self.noduri = dict()  # Fac un dictionar cu (nod,id)
        self.addNode(NodParcurgere(stareFinala, None))
        self.addNode(NodParcurgere(self.start, None, 0, self.calculeaza_h(self.start)))
        self.ok = True

    def addNode(self, nodParcurgere):
        """
        Adauga nodParcurgere in graf pentru a putea tine minte ID-ul
           :param nodParcurgere: NodParcurgere
           :return nothing
       """
        try:
            indice = self.noduri[nodParcurgere]
            nodParcurgere.id = indice
        except KeyError:
            indice = len(self.noduri) - 1
            nodParcurgere.id = indice
            self.noduri[nodParcurgere] = indice

    def testeaza_scop(self, nodCurent):
        '''

        :param nodCurent:
        :return: Bool, true daca e stare scop, false altfel
        '''
        return nodCurent.info in self.scopuri

    def genereazaCombinatii(self, nrCol,
                            deTaiat):  # Indicele de start, cate pot sa tai
        combinatii = []
        for i in range(nrCol):
            for j in range(deTaiat):
                if i + j < nrCol:
                    combinatii.append((i, j))
        return combinatii

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica_banala"):
        """

        :param nodCurent: NodParcurgere
        :param tip_euristica:
        :return: listaSuccesori :obj:'list' of :obj:'NodParcurgere'
        """
        listaSuccesori = []
        nr_linii_de_taiat = len(nodCurent.info) - len(self.scopuri[0])
        nr_coloane_de_taiat = len(nodCurent.info[0]) - len(self.scopuri[0][0])
        for start, nr in self.genereazaCombinatii(len(nodCurent.info), nr_linii_de_taiat):
            info_nou, costTaiere = self.taieLinia(nodCurent.info, start, nr)
            if self.checkStare(info_nou):
                nod_nou = NodParcurgere(info_nou, nodCurent, cost=nodCurent.g + costTaiere,
                                        h=self.calculeaza_h(info_nou, tip_euristica), mutare=('l', start, nr))
                if not nodCurent.contineInDrum(info_nou):
                    listaSuccesori.append(nod_nou)
        for start, nr in self.genereazaCombinatii(len(nodCurent.info[0]), nr_coloane_de_taiat):
            info_nou, costTaiere = self.taieColoana(nodCurent.info, start, nr)
            if self.checkStare(info_nou):
                nod_nou = NodParcurgere(info_nou, nodCurent, cost=nodCurent.g + costTaiere,
                                        h=self.calculeaza_h(info_nou, tip_euristica), mutare=('c', start, nr))
                if not nodCurent.contineInDrum(info_nou):
                    listaSuccesori.append(nod_nou)
        return listaSuccesori

    def taieLinia(self, info, start, nr):
        """

        :param info: informatia dintr-un nod
        :param start: indexul de unde incepe taierea
        :param nr: cate linii adiacente taiem (0 inseamna ca tai doar linia cu indicele start)
        :return: informatia updatata si costul
        """
        info_nou = []
        nr_linii = start + nr + 1
        nr_col = len(info[0])  # Nu ar trebui sa fie nr linii inainte de taiere?
        for i in range(len(info)):
            if i < start or i > start + nr:
                info_nou.append(info[i])
        return info_nou, nr_col / nr_linii

    def taieColoana(self, info, start, nr):
        """

        :param info: informatia dintr-un nod
        :param start: indexul de unde incepe taierea
        :param nr: cate coloane adiacente taiem (0 inseamna ca tai doar coloana cu indicele start)
        :return: informatia updatata si costul
        """
        nr_coloane = nr + 1
        max_i = len(info)
        max_j = len(info[0])
        info_nou = []
        for linie in info:
            info_nou.append(linie[:start] + linie[(start + nr + 1):])
        cost = 0
        for j in range(start, min(start + nr + 1, max_j)):
            for i in range(max_i):
                try:
                    if info[i + 1][j] != info[i][j] and j <= start + nr:
                        cost += 1
                except:
                    pass
                try:
                    if info[i][j + 1] != info[i][j] and j + 1 <= start + nr:
                        cost += 1
                except:
                    pass
        return info_nou, 1 + cost / nr_coloane

    def calculeaza_h(self, infoNod, tip_euristica="euristica_banala"):
        if tip_euristica == "euristica_banala":
            if infoNod not in self.scopuri:
                return 1
            return 0
        elif tip_euristica == "euristica1":  # In cel mai bun caz pot sa tai o singura data linie si coloana
            # costul minim fiind 1 pt coloana
            # (nr coloane final)/(nr linii curent - nr linii final) pt linii
            costColoane = 0
            costLinii = 0
            if len(infoNod[0]) != len(self.scopuri[0][0]): #Daca e nevoie sa tai coloane
                costColoane = 1
            if len(infoNod) - len(self.scopuri[0]) > 0: #Daca e nevoie sa tai linii
                costLinii = len(self.scopuri[0][0]) / (len(infoNod) - len(self.scopuri[0]))
            return costColoane + costLinii
        elif tip_euristica == "euristica2": # Nu e la fel de "precisa" ca prima, nu mai tine cont de costul liniilor
            costColoane = 0
            if len(infoNod[0]) != len(self.scopuri[0][0]):
                costColoane = 1
            return costColoane
        elif tip_euristica == "inadmisibila":  # Pt fiecare linie si coloana care trebuie taiata pun costul 1
            return len(infoNod) - len(self.scopuri[0]) + len(infoNod[0] - len(self.scopuri[0][0]))
        return 1

    def checkStare(self, infoNod):  # Verific daca se poate ajunge din starea curenta in starea finala

        if len(infoNod) < len(self.scopuri[0]) or len(infoNod[0]) < len(self.scopuri[0][
                                                                            0]):  # Daca nu are cel putin la fel de multe linii si coloane (putem taia, nu putem adauga)
            return False  # Verificarea asta este inclusa in cea de mai jos, dar se face in O(1) si ne poate scapa de una mai scumpa
        temp = Multiset()
        for linie in infoNod:
            temp.update(linie)
        return temp >= self.final  # Daca nu are cel putin destule caractere ex starea finala contine 'z' iar starea curenta nu
    # Ar mai merge verificat daca se respecta si ordinea aparitiei caracterelor, dar ar dura cel putin N*M => nu e fezabil


def uniform_cost(f, gr, tipEuristica="euristica_banala", nrSolutiiCautate=1, timeOut=100000):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [
        NodParcurgere(gr.start, None)]  # Primul nod e cel cu info din starea initiala, nu are parinte, costurile sunt 0
    t1, t2 = time.time(), time.time()
    milis = round(1000 * (t2 - t1))
    max_noduri = 0
    noduri_generate = 0
    while len(c) > 0 and milis < timeOut:
        nodCurent = c.pop(0)
        gr.addNode(nodCurent)
        if gr.testeaza_scop(nodCurent):
            timpGasire = time.time()
            f.write("Solutie: \n")
            nodCurent.afisDrum(f)
            f.write(f"Timp pt a gasi solutia: {round(1000 * (timpGasire - t1))} ms\n")
            f.write(f"Nr maxim noduri in memorie: {max_noduri}\n")
            f.write(f"Nr de noduri generate: {noduri_generate}\n")
            f.write("----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tipEuristica)
        noduri_generate += len(lSuccesori)
        t2 = time.time()
        milis = round(1000 * (t2 - t1))
        if milis > timeOut:
            f.write("TIMED OUT\n")
            return
        for s in lSuccesori:
            i = binSearch(s.g, c, lambda x: x.g)  # Sortez dupa g
            c.insert(i, s)
        max_noduri = max(max_noduri, len(c))
    milis = round(1000 * (time.time() - t1))
    if milis>timeOut:
        f.write("TIMED OUT\n")
        return


def a_star_optimizat(f, gr, tipEuristica="euristica_banala", nrSolutiiCautate=1, timeOut=1000000000):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    heapify(c)
    # coada c este numita Open (noduri neexpandate inca) in algoritmul dat la curs
    # closed e cu nodurile expandate
    closed = []
    t1 = time.time()
    t2 = time.time()
    max_noduri = 0
    noduri_generate = 0
    milis = round(1000 * (t2 - t1))
    while len(c) > 0 and milis < timeOut:
        nodCurent = heappop(c)
        gr.addNode(nodCurent)
        closed.append(nodCurent)
        if gr.testeaza_scop(nodCurent):
            timpGasire = time.time()
            f.write("Solutie: \n")
            nodCurent.afisDrum(f)
            f.write(f"Timp pt a gasi solutia: {round(1000 * (timpGasire - t1))} ms\n")
            f.write(f"Nr maxim noduri in memorie: {max_noduri}\n")
            f.write(f"Nr de noduri generate: {noduri_generate}\n")
            f.write("----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tipEuristica)
        noduri_generate += len(lSuccesori)
        max_noduri = max(max_noduri, len(c) + len(lSuccesori) + len(closed))
        t2 = time.time()
        milis = round(1000 * (t2 - t1))
        if milis > timeOut:
            f.write('TIMED OUT\n')
            return
        for s in lSuccesori:
            gasitC = False
            for nodC in c:
                if s.info == nodC.info:
                    gasitC = True
                    if s.f >= nodC.f:
                        lSuccesori[:] = [x for x in lSuccesori if
                                         x != s]  # lSuccesori.remove(s) crapa din cauza ca deja iterez peste lista
                    else:  # s.f<nodC.f
                        c[:] = [x for x in c if x != nodC]
            if not gasitC:
                for nodC in closed:
                    if s.info == nodC.info:
                        if s.f >= nodC.f:
                            lSuccesori[:] = [x for x in lSuccesori if
                                             x != s]
                        else:  # s.f<nodC.f
                            closed[:] = [x for x in closed if x != nodC]
            heapify(c)
        for s in lSuccesori:
            heappush(c, s)
    milis = round(1000 * (time.time() - t1))
    if milis > timeOut:
        f.write('TIMED OUT\n')
        return

def a_star(f, gr, tipEuristica="euristica_banala", nrSolutiiCautate=1, timeOut=10000000000):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    heapify(c)
    t1 = time.time()
    t2 = time.time()
    max_noduri = 0
    noduri_generate = 0
    milis = round(1000 * (t2 - t1))
    while len(c) > 0 and milis < timeOut:
        nodCurent = heappop(c)
        gr.addNode(nodCurent)
        if gr.testeaza_scop(nodCurent):
            timpGasire = time.time()
            f.write("Solutie: \n")
            nodCurent.afisDrum(f)
            f.write(f"Timp pt a gasi solutia: {round(1000 * (timpGasire - t1))} ms\n")
            f.write(f"Nr maxim noduri in memorie: {max_noduri}\n")
            f.write(f"Nr de noduri generate: {noduri_generate}\n")
            f.write("----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tipEuristica)
        noduri_generate += len(lSuccesori)
        t2 = time.time()
        milis = round(1000 * (t2 - t1))
        for s in lSuccesori:
            heappush(c, s)
        max_noduri = max(max_noduri, len(c))
    milis = round(1000 * (time.time() - t1))
    if milis > timeOut:
        f.write('TIMED OUT\n')
        return

def ida_star(f, gr, tipEuristica="euristica_banala", nrSolutiiCautate=1, timeOut=100000):
    def construieste_drum(gr, startTime, noduri_generate, nodCurent, limita, nrSolutiiCautate,
                          tipEuristica="euristica_banala"):
        global maxNoduri, globalMaxNoduri
        milis = round(1000 * (time.time() - startTime))
        if milis > timeOut:
            f.write("TIMED OUT")
            return nrSolutiiCautate, float('inf'), noduri_generate
        if nodCurent.f > limita:
            return nrSolutiiCautate, nodCurent.f, noduri_generate
        if gr.testeaza_scop(nodCurent) and nodCurent.f == limita:
            f.write("Solutie: \n")
            nodCurent.afisDrum(f)
            f.write(f"Timp pt a gasi solutia: {round(1000 * (time.time() - startTime))} ms\n")
            f.write(f"Nr maxim noduri in memorie: {globalMaxNoduri}\n")
            f.write(f"Nr de noduri generate: {noduri_generate}\n")
            f.write("----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return 0, "gata", 0
        lSuccesori = gr.genereazaSuccesori(nodCurent, tipEuristica)
        noduri_generate += len(lSuccesori)
        maxNoduri += len(lSuccesori)
        globalMaxNoduri = max(maxNoduri, globalMaxNoduri)
        minim = 2e9
        for s in lSuccesori:
            maxNoduri -= 1
            gr.addNode(s)
            milis = round(1000 * (time.time() - startTime))
            if milis > timeOut:
                return nrSolutiiCautate, float('inf'), noduri_generate
            nrSolutiiCautate, rez, noduri_generate = construieste_drum(gr, t1, noduri_generate,
                                                                       s, limita, nrSolutiiCautate, tipEuristica)
            if rez == "gata":
                return 0, "gata", noduri_generate
            minim = min(minim, rez)
        return nrSolutiiCautate, minim, noduri_generate

    global maxNoduri
    t1 = time.time()
    noduri_generate = 0
    nodStart = NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))
    limita = nodStart.f
    while round(1000 * (time.time() - t1)) < timeOut:
        nrSolutiiCautate, rez, noduri_generate = construieste_drum(gr, t1, noduri_generate, nodStart,
                                                                   limita,
                                                                   nrSolutiiCautate, tipEuristica)
        if rez == "gata":
            break
        if rez == float('inf'):
            f.write("Nu exista solutii!\n")
            break
        limita = rez


functii = [uniform_cost, a_star, a_star_optimizat, ida_star]
euristici = ["euristica_banala", "euristica1", "euristica2", "inadmisibil"]
# Daca nu exista folderul de output, il creez
if not os.path.exists(sys.argv[2]):
    os.mkdir(sys.argv[2])

nrSol = int(sys.argv[3])
timeOut = int(sys.argv[4])

# Pentru fiecare fisier de input

for numeFisier in os.listdir(sys.argv[1]):
    g = Graph(sys.argv[1] + '/' + numeFisier)  # Creez graful - ID-ul nodurilor va fi mai mare decat genereaza fiecare algoritm in parte deoarece nu resetez etichetele
    if g.ok:  # Daca sunt ok datele de intrare
        for functie in functii:  # Pt fiecare dintre cele 4 functii
            for euristica in euristici:  # Pt fiecare euristica
                print(f"Apelez {functie.__name__} cu {euristica} pentru {numeFisier}")
                numeFisierOutputLocal = "output_" + "_" + functie.__name__ + "_" + euristica + "_" + numeFisier[
                                        :-4] + ".txt"  # Tai terminatia fisierului, adaug numele functiei + .txt
                stream = open(sys.argv[2] + "/" + numeFisierOutputLocal, "w")
                functie(stream, g, euristica, nrSol, timeOut)
                # închid fișierul
                stream.close()
