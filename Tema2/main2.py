import time
import copy
import pygame
import sys
import math


def distEuclid(p0, p1):
    (x0, y0) = p0
    (x1, y1) = p1
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)


def mean(values):
    if len(values):
        return sum(values) / len(values)
    return 0


def median(values):
    n = len(values)
    if n == 0:
        return 0
    s = sorted(values)
    if n % 2:
        return s[n // 2]
    else:
        n = n // 2
        try:
            return (s[n] + s[n + 1]) / 2
        except:
            return 0


def maxim(values):
    if len(values):
        return max(values)
    return 0


def minim(values):
    if len(values):
        return min(values)
    return 0


def distanta(indiceNodStart, indiceNodSf):
    distante = [0] * 34
    visited = [False] * 34
    queue = []
    queue.append(indiceNodStart)
    visited[indiceNodStart] = True
    while queue:
        s = queue.pop(0)
        for i in Graph.listaAdiacenta[s]:
            if visited[i] == False:
                queue.append(i)
                distante[i] = distante[s] + 1
                visited[i] = True
                if i == indiceNodSf:
                    return distante[indiceNodSf]
    return 20


def diff(coord1, coord2):
    return [coord1[0] - coord2[0], coord1[1] - coord2[1]]


def add(coord1, coord2):
    return [coord1[0] + coord2[0], coord1[1] + coord2[1]]


class Graph:
    # coordonatele nodurilor ()
    noduri = [
        (2, 0), (3, 0), (4, 0),  # 0   1    2
        (2, 1), (3, 1), (4, 1),  # 3   4    5
        (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2),  # 6   7    8   9   10  11  12
        (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3),  # 13  14   15  16   17  18  19
        (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),  # 20  21   22  23   24  25  26
        (2, 5), (3, 5), (4, 5),  # 27  28   29
        (2, 6), (3, 6), (4, 6)  # 30  31   32
    ]
    muchii = [(0, 1), (0, 3), (0, 4), (1, 2), (1, 4), (2, 5), (2, 4), (3, 4), (3, 8), (4, 5), (8, 9), (9, 10), (9, 4),
              (8, 4), (4, 10), (10, 5), (6, 7), (7, 8), (10, 11), (11, 12),
              (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19),
              (20, 21), (21, 22), (22, 23), (23, 24), (24, 25), (25, 26),
              (27, 28), (28, 29), (30, 31), (31, 32), (6, 13), (13, 20), (7, 14), (14, 21), (8, 15), (15, 22), (9, 16),
              (16, 23), (10, 17), (17, 24), (11, 18), (18, 25), (12, 19), (19, 26),
              (22, 27), (27, 30), (23, 28), (28, 31), (24, 29), (29, 32), (6, 14), (20, 14), (14, 22), (14, 8), (8, 16),
              (22, 16), (16, 10), (16, 24), (10, 18), (24, 18), (18, 26), (18, 12),
              (22, 28), (30, 28), (28, 32), (28, 24)]
    listaAdiacenta = {0: [1, 3, 4],
                      1: [0, 2, 4],
                      2: [1, 5, 4],
                      3: [0, 4, 8],
                      4: [0, 1, 2, 3, 5, 9, 8, 10],
                      5: [2, 4, 10],
                      6: [7, 13, 14],
                      7: [6, 8, 14],
                      8: [3, 9, 4, 7, 15, 14, 16],
                      9: [8, 10, 4, 16],
                      10: [9, 4, 5, 11, 17, 16, 18],
                      11: [10, 12, 18],
                      12: [11, 19, 18],
                      13: [14, 6, 20],
                      14: [13, 15, 7, 21, 6, 20, 22, 8],
                      15: [14, 16, 8, 22],
                      16: [15, 17, 9, 23, 8, 22, 10, 24],
                      17: [16, 18, 10, 24],
                      18: [17, 19, 11, 25, 10, 24, 26, 12],
                      19: [18, 12, 26],
                      20: [21, 13, 14],
                      21: [20, 22, 14],
                      22: [21, 23, 15, 27, 14, 16, 28],
                      23: [22, 24, 16, 28],
                      24: [23, 25, 17, 29, 16, 18, 28],
                      25: [24, 26, 18],
                      26: [25, 19, 18],
                      27: [28, 22, 30],
                      28: [27, 29, 23, 31, 22, 30, 32, 24],
                      29: [28, 24, 32],
                      30: [31, 27, 28],
                      31: [30, 32, 28],
                      32: [31, 29, 28]}
    scalare = 100
    translatie = 20
    razaPct = 10
    razaPiesa = 20


class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(53, 80, 115),
                 culoareFundalSel=(89, 134, 194), text="", font="arial", fontDimensiune=16, culoareText=(255, 255, 255),
                 valoare=""):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        # creez obiectul font
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        # aici centram textul
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += (spatiuButoane + b.w)

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        # atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


############# ecran initial ########################
def deseneaza_alegeri(display, tabla_curenta):
    btn_alg = GrupButoane(
        top=30,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="minimax", valoare="minimax"),
            Buton(display=display, w=80, h=30, text="alphabeta", valoare="alphabeta")
        ],
        indiceSelectat=1)
    btn_juc = GrupButoane(
        top=100,
        left=30,
        listaButoane=[
            Buton(display=display, w=35, h=30, text="vulpi", valoare="V"),
            Buton(display=display, w=35, h=30, text="oi", valoare="O")
        ],
        indiceSelectat=0)
    btn_ordine = GrupButoane(
        top=170,
        left=30,
        listaButoane=[
            Buton(display=display, w=50, h=30, text="primul", valoare="1"),
            Buton(display=display, w=50, h=30, text="al doilea", valoare="2")
        ],
        indiceSelectat=0)
    btn_dificultate = GrupButoane(
        top=240,
        left=30,
        listaButoane=[
            Buton(display=display, w=70, h=30, text="Incepator", valoare="1"),
            Buton(display=display, w=70, h=30, text="Mediu", valoare="2"),
            Buton(display=display, w=70, h=30, text="Avansat", valoare="3")
        ],
        indiceSelectat=0)
    ok = Buton(display=display, top=310, left=30, w=40, h=30, text="ok", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_ordine.deseneaza()
    btn_dificultate.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_juc.selecteazaDupacoord(pos):
                        if not btn_ordine.selecteazaDupacoord(pos):
                            if not btn_dificultate.selecteazaDupacoord(pos):
                                if ok.selecteazaDupacoord(pos):
                                    display.fill((0, 0, 0))  # stergere ecran
                                    tabla_curenta.deseneaza_grid()
                                    return btn_juc.getValoare(), btn_alg.getValoare(), btn_ordine.getValoare(), btn_dificultate.getValoare()
        pygame.display.update()


def deseneaza_alegeri_jvj(display, tabla_curenta):
    btn_juc = GrupButoane(
        top=100,
        left=30,
        listaButoane=[
            Buton(display=display, w=35, h=30, text="vulpi", valoare="V"),
            Buton(display=display, w=35, h=30, text="oi", valoare="O")
        ],
        indiceSelectat=0)
    btn_ordine = GrupButoane(
        top=170,
        left=30,
        listaButoane=[
            Buton(display=display, w=50, h=30, text="primul", valoare="1"),
            Buton(display=display, w=50, h=30, text="al doilea", valoare="2")
        ],
        indiceSelectat=0)
    ok = Buton(display=display, top=310, left=30, w=40, h=30, text="ok", culoareFundal=(155, 0, 55))
    btn_juc.deseneaza()
    btn_ordine.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_juc.selecteazaDupacoord(pos):
                    if not btn_ordine.selecteazaDupacoord(pos):
                        if ok.selecteazaDupacoord(pos):
                            display.fill((0, 0, 0))  # stergere ecran
                            tabla_curenta.deseneaza_grid()
                            return btn_juc.getValoare(), btn_ordine.getValoare()
        pygame.display.update()


def deseneaza_moduri(display):
    btn_alg = GrupButoane(
        top=30,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="J vs J", valoare="jvj"),
            Buton(display=display, w=80, h=30, text="C vs J", valoare="cvj"),
            Buton(display=display, w=80, h=30, text="C vs C", valoare="cvc")
        ],
        indiceSelectat=1)
    ok = Buton(display=display, top=310, left=30, w=40, h=30, text="ok", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if ok.selecteazaDupacoord(pos):
                        display.fill((0, 0, 0))  # stergere ecran
                        return btn_alg.getValoare()
        pygame.display.update()


def deseneaza_calculatoare(display, tabla_curenta):
    btn_alg1 = GrupButoane(
        top=30,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="minimax", valoare="minimax"),
            Buton(display=display, w=80, h=30, text="alphabeta", valoare="alphabeta")
        ],
        indiceSelectat=1)
    btn_estimeaza1 = GrupButoane(
        top=100,
        left=30,
        listaButoane=[
            Buton(display=display, w=100, h=30, text="Estimarea 1", valoare="1"),
            Buton(display=display, w=100, h=30, text="Estimarea 2", valoare="2")
        ],
        indiceSelectat=0)
    btn_alg2 = GrupButoane(
        top=170,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="minimax", valoare="minimax"),
            Buton(display=display, w=80, h=30, text="alphabeta", valoare="alphabeta")
        ],
        indiceSelectat=1)
    btn_estimeaza2 = GrupButoane(
        top=240,
        left=30,
        listaButoane=[
            Buton(display=display, w=100, h=30, text="Estimarea 1", valoare="Estimarea 1"),
            Buton(display=display, w=100, h=30, text="Estimarea 2", valoare="Estimarea 2")
        ],
        indiceSelectat=0)
    btn_incep = GrupButoane(
        top=310,
        left=30,
        listaButoane=[
            Buton(display=display, w=35, h=30, text="Vulpi", valoare="1"),
            Buton(display=display, w=35, h=30, text="Oi", valoare="2")
        ],
        indiceSelectat=0)
    ok = Buton(display=display, top=380, left=30, w=40, h=30, text="ok", culoareFundal=(155, 0, 55))
    btn_alg1.deseneaza()
    btn_alg2.deseneaza()
    btn_estimeaza1.deseneaza()
    btn_estimeaza2.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg1.selecteazaDupacoord(pos):
                    if not btn_alg2.selecteazaDupacoord(pos):
                        if not btn_estimeaza1.selecteazaDupacoord(pos):
                            if not btn_estimeaza2.selecteazaDupacoord(pos):
                                if not btn_incep.selecteazaDupacoord(pos):
                                    if ok.selecteazaDupacoord(pos):
                                        display.fill((0, 0, 0))  # stergere ecran
                                        tabla_curenta.deseneaza_grid()
                                        return btn_alg1.getValoare(), btn_estimeaza1.getValoare(), btn_alg2.getValoare(), btn_estimeaza2.getValoare(), btn_incep.getValoare()
        pygame.display.update()


ADANCIME_MAX = 2
nr_noduri_generate = 0
noduri_minmax = []
noduri_alphabeta = []
timpi_JMIN = []
timpi_JMAX = []
timp_initial = 0
pygame.init()
pygame.display.set_caption("Nedelcu Radu - Vulpi Si Oi")
# dimensiunea ferestrei in pixeli
ecran = pygame.display.set_mode(size=(800, 800))

pygame.init()
culoareEcran = (255, 255, 255)
culoareLinii = (0, 0, 0)
piesaAlba = pygame.image.load(r'E:\PyCharmProjects\Tema2IA\piesa-alba.png')
diametruPiesa = 2 * Graph.razaPiesa
piesaAlba = pygame.transform.scale(piesaAlba, (diametruPiesa, diametruPiesa))
piesaNeagra = pygame.image.load(r'E:\PyCharmProjects\Tema2IA\piesa-neagra.png')
piesaNeagra = pygame.transform.scale(piesaNeagra, (diametruPiesa, diametruPiesa))
piesaSelectata = pygame.image.load(r"E:\PyCharmProjects\Tema2IA\piesa-rosie.png")
piesaSelectata = pygame.transform.scale(piesaSelectata, (diametruPiesa, diametruPiesa))
nodPiesaSelectata = False
coordonateNoduri = [[Graph.translatie + Graph.scalare * x for x in nod] for nod in Graph.noduri]


def manancaOi(jocuri):
    mutari = set()
    for joc in jocuri:
        for vulpe in joc.pieseNegre:
            indexVecini = vecini(vulpe)
            for vecin in indexVecini:
                if coordonateNoduri[vecin] in joc.pieseAlbe:
                    directie = diff(vulpe, coordonateNoduri[vecin])  # Ma uit pe ce directie ar fi mutata vulpea
                    indexVeciniOaie = vecini(coordonateNoduri[vecin])
                    for vecinOaie in indexVeciniOaie:
                        if coordonateNoduri[vecinOaie] not in joc.pieseAlbe + joc.pieseNegre and diff(
                                coordonateNoduri[vecin],
                                coordonateNoduri[vecinOaie]) == directie:  # Vecinul oii e liber si pe directia buna
                            pieseNegreNoi = copy.deepcopy(joc.pieseNegre)
                            pieseAlbeNoi = copy.deepcopy(joc.pieseAlbe)
                            pieseAlbeNoi[:] = [x for x in pieseAlbeNoi if
                                               x != coordonateNoduri[vecin]]  # Scot oaia mancata
                            pieseNegreNoi[:] = [x for x in pieseNegreNoi if x != vulpe]  # Scot vechea pozitie a vulpii
                            pieseNegreNoi.append(coordonateNoduri[vecinOaie])  # Adaug noua pozitie
                            jn = Joc(pieseAlbeNoi, pieseNegreNoi)
                            mutari.add(jn)
    return mutari


def manancaOiComplet(jocuri):
    while manancaOi(jocuri):
        jocuri = manancaOi(jocuri)
    return jocuri


def veciniCuOiDeMancat(nodVulpe, pieseAlbe, pieseNegre):
    indexVecini = vecini_din_index(nodVulpe)
    veciniDeMancat = []
    for vecin in indexVecini:
        if coordonateNoduri[vecin] in pieseAlbe:
            directie = diff(coordonateNoduri[nodVulpe],
                            coordonateNoduri[vecin])  # Ma uit pe ce directie ar fi mutata vulpea
            indexVeciniOaie = vecini(coordonateNoduri[vecin])
            for vecinOaie in indexVeciniOaie:
                directie2 = diff(coordonateNoduri[vecin], coordonateNoduri[vecinOaie])
                if coordonateNoduri[
                    vecinOaie] not in pieseAlbe + pieseNegre and directie2 == directie:  # Vecinul oii e liber si pe directia buna
                    veciniDeMancat.append((vecin, vecinOaie))
    return veciniDeMancat


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    JMIN = None
    JMAX = None
    pieseAlbe = [coordonateNoduri[i] for i in range(13, 33)]
    pieseNegre = [coordonateNoduri[0], coordonateNoduri[2]]
    scor_maxim = 0
    j_curent = "O"

    def setDisplay(self, ecran):
        self.display = ecran

    def __init__(self, pieseAlbe=None, pieseNegre=None):
        # creez proprietatea ultima_mutare # (l,c)
        self.ultima_mutare = None

        if pieseAlbe:
            # e data tabla, deci suntem in timpul jocului
            self.pieseAlbe = pieseAlbe
            self.pieseNegre = pieseNegre
        else:
            ######## calculare scor maxim ###########

            self.__class__.scor_maxim = 1000

    def deseneaza_grid(self, nodPiesaSelectata=None):  # tabla de exemplu este ["#","x","#","0",......]
        ecran.fill(culoareEcran)
        for nod in coordonateNoduri:
            pygame.draw.circle(surface=ecran, color=culoareLinii, center=nod, radius=Graph.razaPct,
                               width=0)  # width=0 face un cerc plin

        for muchie in Graph.muchii:
            p0 = coordonateNoduri[muchie[0]]
            p1 = coordonateNoduri[muchie[1]]
            pygame.draw.line(surface=ecran, color=culoareLinii, start_pos=p0, end_pos=p1, width=5)
        for nod in self.pieseAlbe:
            ecran.blit(piesaAlba, (nod[0] - Graph.razaPiesa, nod[1] - Graph.razaPiesa))
        for nod in self.pieseNegre:
            ecran.blit(piesaNeagra, (nod[0] - Graph.razaPiesa, nod[1] - Graph.razaPiesa))
        if nodPiesaSelectata:
            ecran.blit(piesaSelectata, (nodPiesaSelectata[0] - Graph.razaPiesa, nodPiesaSelectata[1] - Graph.razaPiesa))
        pygame.display.update()

    def deseneaza_castigator(self):  # tabla de exemplu este ["#","x","#","0",......]
        global piesaAlba, piesaNeagra
        ecran.fill(culoareEcran)
        castigator = self.final()
        if castigator == "V":
            piesaNeagra = piesaSelectata
        else:
            piesaAlba = piesaSelectata
        for nod in coordonateNoduri:
            pygame.draw.circle(surface=ecran, color=culoareLinii, center=nod, radius=Graph.razaPct,
                               width=0)  # width=0 face un cerc plin
        for muchie in Graph.muchii:
            p0 = coordonateNoduri[muchie[0]]
            p1 = coordonateNoduri[muchie[1]]
            pygame.draw.line(surface=ecran, color=culoareLinii, start_pos=p0, end_pos=p1, width=5)
        for nod in self.pieseAlbe:
            ecran.blit(piesaAlba, (nod[0] - Graph.razaPiesa, nod[1] - Graph.razaPiesa))
        for nod in self.pieseNegre:
            ecran.blit(piesaNeagra, (nod[0] - Graph.razaPiesa, nod[1] - Graph.razaPiesa))
        if nodPiesaSelectata:
            ecran.blit(piesaSelectata, (nodPiesaSelectata[0] - Graph.razaPiesa, nodPiesaSelectata[1] - Graph.razaPiesa))
        pygame.display.update()

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
        if len(self.pieseAlbe) < 9:
            return "V"
        if all(coordonateNoduri[i] in self.pieseAlbe for i in
               [0, 1, 2, 3, 4, 5, 8, 9, 10]):  # Daca toate cele 9 locuri de sus sunt ocupate de oi
            return "O"
        return False

    def mutari_valide(self, jucator):
        l_mutari = []
        if jucator == "O":  # Muta oile
            for oaie in self.pieseAlbe:  # Iau toate oile
                indexVecini = vecini(oaie)  # Iau vecinii
                indexStart = coordonateNoduri.index(oaie)
                for vecin in indexVecini:  # Pt fiecare vecin
                    if not (indexStart > vecin or abs(indexStart - vecin) == 1):
                        # Oile nu au voie sa se duca in jos (adica pe un nod cu indicele mai mare decat cel curent)
                        continue
                    if coordonateNoduri[vecin] not in self.pieseAlbe + self.pieseNegre:  # Vecinul e liber
                        pieseNegreNoi = copy.deepcopy(self.pieseNegre)
                        pieseAlbeNoi = copy.deepcopy(self.pieseAlbe)
                        pieseAlbeNoi[:] = [x for x in pieseAlbeNoi if x != oaie]  # Scot vechea piesa
                        pieseAlbeNoi.append(coordonateNoduri[vecin])  # Adaug noua pozitie
                        jn = Joc(pieseAlbeNoi, pieseNegreNoi)
                        l_mutari.append(jn)
        else:  # Muta vulpile
            # 1.Verific vecinii
            # 2. Vad daca sunt oi
            # 3. Daca e oaie, verific daca poate fi luata (vecinul pe directia respectiva sa fie gol)
            # 4. Daca am oi de luat, ma opresc.
            # Daca nu, pur si simplu mut vulpea intr-un loc liber
            table_noi = manancaOiComplet({self})
            table_noi -= {self}
            if len(table_noi) >= 1:
                l_mutari.extend(table_noi)
            else:
                for vulpe in self.pieseNegre:
                    indexVecini = vecini(vulpe)
                    for vecin in indexVecini:
                        if coordonateNoduri[vecin] not in self.pieseAlbe + self.pieseNegre:  # Daca vecinul e gol
                            pieseNegreNoi = copy.deepcopy(self.pieseNegre)
                            pieseAlbeNoi = copy.deepcopy(self.pieseAlbe)
                            pieseNegreNoi[:] = [x for x in pieseNegreNoi if x != vulpe]  # Scot vechea pozitie a vulpii
                            pieseNegreNoi.append(coordonateNoduri[vecin])  # Adaug noua pozitie
                            jn = Joc(pieseAlbeNoi, pieseNegreNoi)
                            l_mutari.append(jn)
        return l_mutari

    def estimeaza_scor(self, adancime, estimare="1"):
        t_final = self.final()
        nr_oi = len(self.pieseAlbe)
        if estimare == "1":
            if t_final == self.__class__.JMAX:  # A castigat calculatorul
                if self.__class__.JMAX == "V":  # Juca cu vulpile
                    return (self.__class__.scor_maxim - adancime - len(
                        timpi_JMAX))  # Vreau sa castige in cat mai putine mutari
                else:  # Juca cu oile - vreau sa castige in cat mai putine mutari si cat mai multe oi
                    return (self.__class__.scor_maxim - adancime + nr_oi - len(timpi_JMAX))
            elif t_final == self.__class__.JMIN:  # A castigat utilizatorul
                if self.__class__.JMAX == "V":  # Juca cu vulpile
                    return (-self.__class__.scor_maxim + adancime + len(
                        timpi_JMAX))  # Vreau sa traga cat mai mult de timp
                else:  # Juca cu oile - vreau sa castige in cat mai putine mutari si cat mai multe oi
                    return (-self.__class__.scor_maxim + adancime - nr_oi + len(timpi_JMAX))
            else:  # Daca nu e final, tin cont de cate oi sunt pe pozitia finala
                nr_oi_potrivite = len([coordonateNoduri[i] in self.pieseAlbe for i in
                                       [0, 1, 2, 3, 4, 5, 8, 9, 10]])
                nr_oi_luate = 20 - nr_oi
                if self.__class__.JMAX == "V":  # Daca calculatorul joaca cu vulpile
                    return nr_oi_luate - nr_oi_potrivite  # Vreau sa fie cat mai putine
                else:  # Juca cu oile - vreau sa fie cat mai multe
                    return nr_oi_potrivite - nr_oi_luate
        else:  # Estimarea 2 - Starile finale se calculeaza la fel, la starea intermediara iau distanta
            if t_final == self.__class__.JMAX:  # A castigat calculatorul
                if self.__class__.JMAX == "V":  # Juca cu vulpile
                    return (self.__class__.scor_maxim - adancime)  # Vreau sa castige in cat mai putine mutari
                else:  # Juca cu oile - vreau sa castige in cat mai putine mutari si cat mai multe oi
                    return (self.__class__.scor_maxim - adancime + nr_oi)
            elif t_final == self.__class__.JMIN:  # A castigat utilizatorul
                if self.__class__.JMAX == "V":  # Juca cu vulpile
                    return (-self.__class__.scor_maxim + adancime)  # Vreau sa traga cat mai mult de timp
                else:  # Juca cu oile - vreau sa castige in cat mai putine mutari si cat mai multe oi
                    return (-self.__class__.scor_maxim + adancime - nr_oi)
            else:  # Daca nu e final, tin cont de cate oi sunt pe pozitia finala
                distantaTotala = 0
                if nr_oi:
                    distantaTotala = sum([distanta(coordonateNoduri.index(nod), 0) for nod in self.pieseAlbe])
                nr_oi_mancate = 20 - nr_oi
                if self.__class__.JMAX == "V":  # Daca calculatorul joaca cu vulpile
                    return nr_oi_mancate * 3 - distantaTotala  # Vreau sa fie cat mai mare distanta
                else:  # Juca cu oile - vreau sa fie cat mai mica
                    return -distantaTotala - nr_oi_mancate

    def sirAfisare(self):
        sir = f"Sunt {len(self.pieseAlbe)} oi la pozitiile {[coordonateNoduri.index(nod) for nod in self.pieseAlbe]}\n"
        sir += f"Sunt  {len(self.pieseNegre)} vulpi la pozitiile {[coordonateNoduri.index(nod) for nod in self.pieseNegre]}\n"
        return sir

    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return self.sirAfisare()


def vecini(nod):
    index_nod = coordonateNoduri.index(nod)
    vec = []
    for (a, b) in Graph.muchii:
        if a == index_nod:
            vec.append(b)
        if b == index_nod:
            vec.append(a)
    return vec


def vecini_din_index(index_nod):
    vec = []
    for (a, b) in Graph.muchii:
        if a == index_nod:
            vec.append(b)
        if b == index_nod:
            vec.append(a)
    return vec


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari_valide(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]
        if len(l_stari_mutari) == 0:
            print("Remiza")
            exit()
        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir

    def __repr__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if (final):
        if (final == "remiza"):
            print("Remiza!")
        else:
            print("A castigat " + final)
            stare_curenta.tabla_joc.deseneaza_castigator()
        return True
    return False


def main_cvj():
    global ADANCIME_MAX, nr_noduri_generate, noduri_alphabeta, noduri_minmax
    # setari interf grafica

    # initializare tabla
    tabla_curenta = Joc()
    tabla_curenta.setDisplay(ecran)
    Joc.JMIN, tip_algoritm, primul, dificultate = deseneaza_alegeri(ecran, tabla_curenta)
    print(Joc.JMIN, tip_algoritm, primul)
    if dificultate == "1":
        ADANCIME_MAX = 3
    elif dificultate == "2":
        ADANCIME_MAX = 4
    else:
        ADANCIME_MAX = 5
    Joc.JMAX = 'V' if Joc.JMIN == 'O' else 'O'
    print("Tabla initiala")
    print(str(tabla_curenta))
    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, Joc.JMIN if primul == "1" else Joc.JMAX, ADANCIME_MAX)
    tabla_curenta.deseneaza_grid()
    nodPiesaSelectata = False
    while True:
        if stare_curenta.j_curent == Joc.JMIN:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    afis_info()
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    timp_initial = time.time()
                    pos = pygame.mouse.get_pos()  # coordonatele cursorului la momentul clickului
                    for nod in coordonateNoduri:
                        if distEuclid(pos, nod) <= Graph.razaPct:
                            if Joc.JMIN == "V":
                                piesa = piesaNeagra
                                pieseCurente = stare_curenta.tabla_joc.pieseNegre
                                pieseOpuse = stare_curenta.tabla_joc.pieseAlbe
                            else:
                                piesa = piesaAlba
                                pieseCurente = stare_curenta.tabla_joc.pieseAlbe
                                pieseOpuse = stare_curenta.tabla_joc.pieseNegre
                            if Joc.JMIN == "O":  # Joaca cu oile
                                if nod not in stare_curenta.tabla_joc.pieseAlbe + stare_curenta.tabla_joc.pieseNegre:
                                    if nodPiesaSelectata:
                                        n0 = coordonateNoduri.index(nod)
                                        n1 = coordonateNoduri.index(nodPiesaSelectata)
                                        directie = diff(nodPiesaSelectata, nod)
                                        n2 = coordonateNoduri.index(add(nod, directie))
                                        if not (n1 > n0 or abs(n0 - n1) == 1):
                                            break
                                        if (n0, n1) in Graph.muchii or (n1, n0) in Graph.muchii:
                                            pieseCurente.remove(nodPiesaSelectata)
                                            pieseCurente.append(nod)
                                            # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                            nodPiesaSelectata = False
                                else:
                                    if nod in pieseCurente:
                                        if nodPiesaSelectata == nod:
                                            nodPiesaSelectata = False
                                        else:
                                            nodPiesaSelectata = nod
                            else:  # Joaca cu vulpile
                                if nod not in stare_curenta.tabla_joc.pieseNegre:  # Nu poate selecta decat vulpi
                                    vulpeN1 = coordonateNoduri.index(stare_curenta.tabla_joc.pieseNegre[0])
                                    vulpeN2 = coordonateNoduri.index(stare_curenta.tabla_joc.pieseNegre[1])
                                    oiDeMancat1 = veciniCuOiDeMancat(vulpeN1, stare_curenta.tabla_joc.pieseAlbe,
                                                                     stare_curenta.tabla_joc.pieseNegre)
                                    oiDeMancat2 = veciniCuOiDeMancat(vulpeN2, stare_curenta.tabla_joc.pieseAlbe,
                                                                     stare_curenta.tabla_joc.pieseNegre)
                                    # Vad la fiecare vulpe daca are de mancat, daca cel putin una trebuie sa mananca, nu il las sa o selecteze pe cealalta
                                    if nodPiesaSelectata:  # Are deja o vulpe selectata
                                        n0 = coordonateNoduri.index(nod)
                                        if len(oiDeMancat1) and n0 not in map(lambda x: x[0],
                                                                              oiDeMancat1):
                                            break
                                        elif len(oiDeMancat2) and n0 not in map(lambda x: x[0],
                                                                                oiDeMancat2):
                                            break
                                        # Vad daca are oi de mancat
                                        n1 = coordonateNoduri.index(nodPiesaSelectata)
                                        oiDeMancat = veciniCuOiDeMancat(n1, stare_curenta.tabla_joc.pieseAlbe,
                                                                        stare_curenta.tabla_joc.pieseNegre)
                                        print(oiDeMancat)
                                        if len(oiDeMancat) == 0:  # Nu are oi de mancat, muta vulpea
                                            if ((n0, n1) in Graph.muchii or (
                                            n1, n0) in Graph.muchii) and nod not in stare_curenta.tabla_joc.pieseAlbe:
                                                pieseCurente.remove(nodPiesaSelectata)
                                                pieseCurente.append(nod)
                                            else:
                                                break
                                        if len(oiDeMancat) > 1:  # Are oi de mancat, dar poate sa aleaga
                                            if n0 in map(lambda x: x[0],
                                                         oiDeMancat):  # Daca pozitia selectata e in vecinii cu oi de mancat
                                                pieseCurente.remove(nodPiesaSelectata)  # Mut vulpea
                                                pieseCurente.append(coordonateNoduri[oiDeMancat[n0][1]])
                                                pieseOpuse.remove(coordonateNoduri[n0])  # Mananc oaia
                                                oiDeMancat = veciniCuOiDeMancat(oiDeMancat[n0][1], pieseOpuse,
                                                                                pieseCurente)
                                        while len(oiDeMancat) == 1:  # Daca are oi de mancat, e obligatoriu sa o faca
                                            pieseCurente.remove(nodPiesaSelectata)
                                            pieseCurente.append(
                                                coordonateNoduri[oiDeMancat[0][1]])  # Mut vulpea pe noua pozitie
                                            pieseOpuse.remove(coordonateNoduri[oiDeMancat[0][0]])  # Mananc oaia
                                            oiDeMancat = veciniCuOiDeMancat(oiDeMancat[0][1], pieseOpuse, pieseCurente)
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                        nodPiesaSelectata = False
                                else:
                                    if nod in pieseCurente:
                                        if nodPiesaSelectata == nod:
                                            nodPiesaSelectata = False
                                        else:
                                            nodPiesaSelectata = nod
                            # afisarea starii jocului in urma mutarii utilizatorului
                            elapsed = round((time.time() - timp_initial) * 1000)
                            timpi_JMIN.append(elapsed)
                            print(f"Jucatorul a gandit timp de {elapsed}ms")
                            print("\nTabla dupa mutarea jucatorului")
                            print(str(stare_curenta))
                            if nodPiesaSelectata:
                                stare_curenta.tabla_joc.deseneaza_grid(nodPiesaSelectata)
                            else:
                                stare_curenta.tabla_joc.deseneaza_grid()
                            # testez daca jocul a ajuns intr-o stare finala
                            # si afisez un mesaj corespunzator in caz ca da
                            if (afis_daca_final(stare_curenta)):
                                return
        # -------------------------------- CAZ PT JMAX (MUTA CALCULATOR)
        else:
            print("Muta calculatorul")
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            nr_noduri_generate = 0
            if tip_algoritm == 'minimax':
                stare_actualizata = min_max(stare_curenta)
                noduri_minmax.append(nr_noduri_generate)
            else:  # tip_algoritm=="alphabeta"
                stare_actualizata = alpha_beta(-5000, 5000, stare_curenta)
                noduri_alphabeta.append(nr_noduri_generate)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print(f"Nr. noduri generate {nr_noduri_generate}. Estimarea scorului: {stare_actualizata.scor}")
            print("Tabla dupa mutarea calculatorului\n" + str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            timpi_JMAX.append(t_dupa - t_inainte)
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            stare_curenta.tabla_joc.deseneaza_grid()
            if (afis_daca_final(stare_curenta)):
                return
            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


def main_cvc():
    global ADANCIME_MAX, nr_noduri_generate, noduri_alphabeta, noduri_minmax
    # setari interf grafica

    # initializare tabla
    tabla_curenta = Joc()
    tabla_curenta.setDisplay(ecran)
    alg1, estimeaza1, alg2, estimeaza2, incepe = deseneaza_calculatoare(ecran, tabla_curenta)
    Joc.JMIN = 'O'
    Joc.JMAX = 'V' if Joc.JMIN == 'O' else 'O'
    print("Tabla initiala")
    print(str(tabla_curenta))
    # creare stare initiala

    stare_curenta = Stare(tabla_curenta, Joc.JMIN if incepe == "1" else Joc.JMAX, ADANCIME_MAX)
    tabla_curenta.deseneaza_grid()
    while True:
        if stare_curenta.j_curent == Joc.JMIN:
            print("Muta calculatorul JMIN")
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            nr_noduri_generate = 0
            if alg1 == 'minimax':
                stare_actualizata = min_max(stare_curenta, estimeaza1)
                noduri_minmax.append(nr_noduri_generate)
            else:  # tip_algoritm=="alphabeta"
                stare_actualizata = alpha_beta(-5000, 5000, stare_curenta, estimeaza1)
                noduri_alphabeta.append(nr_noduri_generate)

            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print(f"Nr. noduri generate {nr_noduri_generate}. Estimarea scorului: {stare_actualizata.scor}")
            print("Tabla dupa mutarea calculatorului\n" + str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            timpi_JMIN.append(t_dupa - t_inainte)
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            stare_curenta.tabla_joc.deseneaza_grid()
            if (afis_daca_final(stare_curenta)):
                return

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
        # -------------------------------- CAZ PT JMAX (MUTA CALCULATOR)
        else:

            print("Muta calculatorul JMAX")
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            nr_noduri_generate = 0
            if alg2 == 'minimax':
                stare_actualizata = min_max(stare_curenta, estimeaza2)
                noduri_minmax.append(nr_noduri_generate)
            else:  # tip_algoritm=="alphabeta"
                stare_actualizata = alpha_beta(-5000, 5000, stare_curenta, estimeaza2)
                noduri_alphabeta.append(nr_noduri_generate)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print(f"Nr. noduri generate {nr_noduri_generate}. Estimarea scorului: {stare_actualizata.scor}")
            print("Tabla dupa mutarea calculatorului\n" + str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            timpi_JMAX.append(t_dupa - t_inainte)
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            stare_curenta.tabla_joc.deseneaza_grid()
            if afis_daca_final(stare_curenta):
                return
            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


def main_jvj():
    # setari interf grafica

    # initializare tabla
    tabla_curenta = Joc()
    tabla_curenta.setDisplay(ecran)
    Joc.JMIN, primul = deseneaza_alegeri_jvj(ecran, tabla_curenta)
    Joc.JMAX = 'V' if Joc.JMIN == 'O' else 'O'
    print("Tabla initiala")
    print(str(tabla_curenta))
    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, Joc.JMIN if primul == "1" else Joc.JMAX, ADANCIME_MAX)
    tabla_curenta.deseneaza_grid()
    nodPiesaSelectata = False
    while True:
        if stare_curenta.j_curent == Joc.JMIN:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    afis_info()
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    timp_initial = time.time()
                    pos = pygame.mouse.get_pos()  # coordonatele cursorului la momentul clickului
                    for nod in coordonateNoduri:
                        if distEuclid(pos, nod) <= Graph.razaPct:
                            if Joc.JMIN == "V":
                                piesa = piesaNeagra
                                pieseCurente = stare_curenta.tabla_joc.pieseNegre
                                pieseOpuse = stare_curenta.tabla_joc.pieseAlbe
                            else:
                                piesa = piesaAlba
                                pieseCurente = stare_curenta.tabla_joc.pieseAlbe
                                pieseOpuse = stare_curenta.tabla_joc.pieseNegre
                            if Joc.JMIN == "O":  # Joaca cu oile
                                if nod not in stare_curenta.tabla_joc.pieseAlbe + stare_curenta.tabla_joc.pieseNegre:
                                    if nodPiesaSelectata:
                                        n0 = coordonateNoduri.index(nod)
                                        n1 = coordonateNoduri.index(nodPiesaSelectata)
                                        directie = diff(nodPiesaSelectata, nod)
                                        if not (n1 > n0 or abs(n0 - n1) == 1):
                                            break
                                        if (n0, n1) in Graph.muchii or (n1, n0) in Graph.muchii:
                                            pieseCurente.remove(nodPiesaSelectata)
                                            pieseCurente.append(nod)
                                            # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                            nodPiesaSelectata = False
                                else:
                                    if nod in pieseCurente:
                                        if nodPiesaSelectata == nod:
                                            nodPiesaSelectata = False
                                        else:
                                            nodPiesaSelectata = nod
                            else:  # Joaca cu vulpile
                                if nod not in stare_curenta.tabla_joc.pieseNegre:  # Nu poate selecta decat vulpi
                                    vulpeN1 = coordonateNoduri.index(stare_curenta.tabla_joc.pieseNegre[0])
                                    vulpeN2 = coordonateNoduri.index(stare_curenta.tabla_joc.pieseNegre[1])
                                    oiDeMancat1 = veciniCuOiDeMancat(vulpeN1, stare_curenta.tabla_joc.pieseAlbe,
                                                                     stare_curenta.tabla_joc.pieseNegre)
                                    oiDeMancat2 = veciniCuOiDeMancat(vulpeN2, stare_curenta.tabla_joc.pieseAlbe,
                                                                     stare_curenta.tabla_joc.pieseNegre)
                                    # Vad la fiecare vulpe daca are de mancat, daca cel putin una trebuie sa mananca, nu il las sa o selecteze pe cealalta
                                    if nodPiesaSelectata:  # Are deja o vulpe selectata
                                        n0 = coordonateNoduri.index(nod)
                                        if len(oiDeMancat1) and n0 not in map(lambda x: x[0],
                                                                              oiDeMancat1):
                                            break
                                        elif len(oiDeMancat2) and n0 not in map(lambda x: x[0],
                                                                                oiDeMancat2):
                                            break
                                        # Vad daca are oi de mancat
                                        n1 = coordonateNoduri.index(nodPiesaSelectata)
                                        oiDeMancat = veciniCuOiDeMancat(n1, stare_curenta.tabla_joc.pieseAlbe,
                                                                        stare_curenta.tabla_joc.pieseNegre)
                                        print(oiDeMancat)
                                        if len(oiDeMancat) == 0:  # Nu are oi de mancat, muta vulpea
                                            if ((n0, n1) in Graph.muchii or (
                                                    n1,
                                                    n0) in Graph.muchii) and nod not in stare_curenta.tabla_joc.pieseAlbe:
                                                pieseCurente.remove(nodPiesaSelectata)
                                                pieseCurente.append(nod)
                                            else:
                                                break
                                        aMancat = False
                                        if len(oiDeMancat) > 1:  # Are oi de mancat, dar poate sa aleaga
                                            if n0 in map(lambda x: x[0],
                                                         oiDeMancat):  # Daca pozitia selectata e in vecinii cu oi de mancat
                                                pieseCurente.remove(nodPiesaSelectata)  # Mut vulpea
                                                pieseCurente.append(coordonateNoduri[oiDeMancat[n0][1]])
                                                vulpeCurenta = coordonateNoduri[oiDeMancat[n0][1]]
                                                pieseOpuse.remove(coordonateNoduri[n0])  # Mananc oaia
                                                oiDeMancat = veciniCuOiDeMancat(oiDeMancat[n0][1], pieseOpuse,
                                                                                pieseCurente)
                                                aMancat = True
                                        if not aMancat:
                                            vulpeCurenta = nodPiesaSelectata
                                        while len(oiDeMancat) == 1:  # Daca are oi de mancat, e obligatoriu sa o faca
                                            pieseCurente.remove(vulpeCurenta)
                                            pieseCurente.append(
                                                coordonateNoduri[oiDeMancat[0][1]])  # Mut vulpea pe noua pozitie
                                            vulpeCurenta = coordonateNoduri[oiDeMancat[0][1]]
                                            pieseOpuse.remove(coordonateNoduri[oiDeMancat[0][0]])  # Mananc oaia
                                            oiDeMancat = veciniCuOiDeMancat(oiDeMancat[0][1], pieseOpuse, pieseCurente)
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                        nodPiesaSelectata = False
                                else:
                                    if nod in pieseCurente:
                                        if nodPiesaSelectata == nod:
                                            nodPiesaSelectata = False
                                        else:
                                            nodPiesaSelectata = nod
                            # afisarea starii jocului in urma mutarii utilizatorului
                            elapsed = round((time.time() - timp_initial) * 1000)
                            timpi_JMIN.append(elapsed)
                            print(f"Jucatorul a gandit timp de {elapsed}ms")
                            print("\nTabla dupa mutarea jucatorului")
                            print(str(stare_curenta))
                            if nodPiesaSelectata:
                                stare_curenta.tabla_joc.deseneaza_grid(nodPiesaSelectata)
                            else:
                                stare_curenta.tabla_joc.deseneaza_grid()
                            # testez daca jocul a ajuns intr-o stare finala
                            # si afisez un mesaj corespunzator in caz ca da
                            if (afis_daca_final(stare_curenta)):
                                return
        # -------------------------------- CAZ PT JMAX
        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    afis_info()
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    timp_initial = time.time()
                    pos = pygame.mouse.get_pos()  # coordonatele cursorului la momentul clickului
                    for nod in coordonateNoduri:
                        if distEuclid(pos, nod) <= Graph.razaPct:
                            if Joc.JMAX == "V":
                                piesa = piesaNeagra
                                pieseCurente = stare_curenta.tabla_joc.pieseNegre
                                pieseOpuse = stare_curenta.tabla_joc.pieseAlbe
                            else:
                                piesa = piesaAlba
                                pieseCurente = stare_curenta.tabla_joc.pieseAlbe
                                pieseOpuse = stare_curenta.tabla_joc.pieseNegre
                            if Joc.JMAX == "O":  # Joaca cu oile
                                if nod not in stare_curenta.tabla_joc.pieseAlbe + stare_curenta.tabla_joc.pieseNegre:
                                    if nodPiesaSelectata:
                                        n0 = coordonateNoduri.index(nod)
                                        n1 = coordonateNoduri.index(nodPiesaSelectata)
                                        if not (n1 > n0 or abs(n0 - n1) == 1):
                                            break
                                        if (n0, n1) in Graph.muchii or (n1, n0) in Graph.muchii:
                                            pieseCurente.remove(nodPiesaSelectata)
                                            pieseCurente.append(nod)
                                            # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                            nodPiesaSelectata = False
                                else:
                                    if nod in pieseCurente:
                                        if nodPiesaSelectata == nod:
                                            nodPiesaSelectata = False
                                        else:
                                            nodPiesaSelectata = nod
                            else:  # Joaca cu vulpile
                                if nod not in stare_curenta.tabla_joc.pieseNegre:  # Nu poate selecta decat vulpi
                                    vulpeN1 = coordonateNoduri.index(stare_curenta.tabla_joc.pieseNegre[0])
                                    vulpeN2 = coordonateNoduri.index(stare_curenta.tabla_joc.pieseNegre[1])
                                    oiDeMancat1 = veciniCuOiDeMancat(vulpeN1, stare_curenta.tabla_joc.pieseAlbe,
                                                                     stare_curenta.tabla_joc.pieseNegre)
                                    oiDeMancat2 = veciniCuOiDeMancat(vulpeN2, stare_curenta.tabla_joc.pieseAlbe,
                                                                     stare_curenta.tabla_joc.pieseNegre)
                                    # Vad la fiecare vulpe daca are de mancat, daca cel putin una trebuie sa mananca, nu il las sa o selecteze pe cealalta
                                    if nodPiesaSelectata:  # Are deja o vulpe selectata
                                        n0 = coordonateNoduri.index(nod)
                                        if len(oiDeMancat1) and n0 not in map(lambda x: x[0],
                                                                              oiDeMancat1):
                                            break
                                        elif len(oiDeMancat2) and n0 not in map(lambda x: x[0],
                                                                                oiDeMancat2):
                                            break
                                        # Vad daca are oi de mancat
                                        n1 = coordonateNoduri.index(nodPiesaSelectata)
                                        oiDeMancat = veciniCuOiDeMancat(n1, stare_curenta.tabla_joc.pieseAlbe,
                                                                        stare_curenta.tabla_joc.pieseNegre)
                                        print(oiDeMancat)
                                        if len(oiDeMancat) == 0:  # Nu are oi de mancat, muta vulpea
                                            if ((n0, n1) in Graph.muchii or (
                                                    n1,
                                                    n0) in Graph.muchii) and nod not in stare_curenta.tabla_joc.pieseAlbe:
                                                pieseCurente.remove(nodPiesaSelectata)
                                                pieseCurente.append(nod)
                                            else:
                                                break
                                        if len(oiDeMancat) > 1:  # Are oi de mancat, dar poate sa aleaga
                                            if n0 in map(lambda x: x[0],
                                                         oiDeMancat):  # Daca pozitia selectata e in vecinii cu oi de mancat
                                                pieseCurente.remove(nodPiesaSelectata)  # Mut vulpea
                                                pieseCurente.append(coordonateNoduri[oiDeMancat[n0][1]])
                                                pieseOpuse.remove(coordonateNoduri[n0])  # Mananc oaia
                                                oiDeMancat = veciniCuOiDeMancat(oiDeMancat[n0][1], pieseOpuse,
                                                                                pieseCurente)
                                        while len(oiDeMancat) == 1:  # Daca are oi de mancat, e obligatoriu sa o faca
                                            pieseCurente.remove(nodPiesaSelectata)
                                            pieseCurente.append(
                                                coordonateNoduri[oiDeMancat[0][1]])  # Mut vulpea pe noua pozitie
                                            pieseOpuse.remove(coordonateNoduri[oiDeMancat[0][0]])  # Mananc oaia
                                            oiDeMancat = veciniCuOiDeMancat(oiDeMancat[0][1], pieseOpuse, pieseCurente)
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                        nodPiesaSelectata = False
                                else:
                                    if nod in pieseCurente:
                                        if nodPiesaSelectata == nod:
                                            nodPiesaSelectata = False
                                        else:
                                            nodPiesaSelectata = nod
                            # afisarea starii jocului in urma mutarii utilizatorului
                            elapsed = round((time.time() - timp_initial) * 1000)
                            timpi_JMAX.append(elapsed)
                            print(f"Jucatorul a gandit timp de {elapsed}ms")
                            print("\nTabla dupa mutarea jucatorului")
                            print(str(stare_curenta))
                            if nodPiesaSelectata:
                                stare_curenta.tabla_joc.deseneaza_grid(nodPiesaSelectata)
                            else:
                                stare_curenta.tabla_joc.deseneaza_grid()
                            # testez daca jocul a ajuns intr-o stare finala
                            # si afisez un mesaj corespunzator in caz ca da
                            if (afis_daca_final(stare_curenta)):
                                return


def afis_info():
    print(f"Programul a rulat timp de {round(1000 * (time.time() - timp_initial))}ms")
    print(f"JMIN a facut {len(timpi_JMIN)} mutari iar JMAX a facut {len(timpi_JMAX)} mutari")
    print(
        f"Pt JMIN: MAX: {maxim(timpi_JMIN)}ms, MIN: {minim(timpi_JMIN)}ms, MEDIA: {mean(timpi_JMIN)}ms, MEDIANA: {median(timpi_JMIN)}ms")
    print(
        f"Pt JMAX: MAX: {maxim(timpi_JMAX)}ms, MIN: {minim(timpi_JMAX)}ms, MEDIA: {mean(timpi_JMAX)}ms, MEDIANA: {median(timpi_JMAX)}ms")
    if len(noduri_minmax):
        print(
            f"Alg minmax: MAX: {max(noduri_minmax)}, MIN: {min(noduri_minmax)}, MEDIA: {mean(noduri_minmax)}, MEDIANA: {median(noduri_minmax)}")
    if len(noduri_alphabeta):
        print(
            f"Alg alphabeta: MAX: {max(noduri_alphabeta)}, MIN: {min(noduri_alphabeta)}, MEDIA: {mean(noduri_alphabeta)}, MEDIANA: {median(noduri_alphabeta)}")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                print("Game resumed")
                return


# region Algoritmi
def min_max(stare, tip_estimare="1"):
    global nr_noduri_generate
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime, tip_estimare)
        nr_noduri_generate += 1
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare, tip_estimare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)
    stare.scor = stare.stare_aleasa.scor
    return stare


def alpha_beta(alpha, beta, stare, tip_estimare="1"):
    global nr_noduri_generate
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime, tip_estimare)
        nr_noduri_generate += 1
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')
        stare.mutari_posibile.sort(key=lambda x: x.tabla_joc.estimeaza_scor(stare.adancime,tip_estimare))
        for mutare in stare.mutari_posibile:
            # calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare, tip_estimare)

            if (scor_curent < stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if (alpha < stare_noua.scor):
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')
        stare.mutari_posibile.sort(key=lambda x: -x.tabla_joc.estimeaza_scor(stare.adancime,tip_estimare))
        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare, tip_estimare)

            if (scor_curent > stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if (beta > stare_noua.scor):
                beta = stare_noua.scor
                if alpha >= beta:
                    break
    stare.scor = stare.stare_aleasa.scor

    return stare


# endregion
if __name__ == "__main__":
    timp_initial = time.time()
    mod = deseneaza_moduri(ecran)
    if mod == "cvc":
        main_cvc()
    elif mod == "cvj":
        main_cvj()
    else:
        main_jvj()
    afis_info()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
