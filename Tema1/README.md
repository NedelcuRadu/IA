## Tema 1 - Căutare informată - Comparație între tehnicile de căutare
## Problema decupării - text preluat de pe http://irinaciocan.ro/inteligenta_artificiala

### 1. Context
Se consideră un grid (matrice) de dimensiuni N×M (N linii și M coloane). În grid avem litere de la a la z. Dorim prin tăieri succesive de linii și coloane să ajungem la o anumită stare scop.
Exemplu de grid:
```
abbacbq
ddaabbb
aaaffxc
aabccdc
adddaab
```

### 2. Stări și tranziții. Cost.
Mutările posibile sunt:

* taierea a X (X≥1) coloane. Cost: 1+ k/(nr coloane taiate), unde k reprezinta numărul, perechilor de vecini care sunt diferiti intre ei din zona decupată, fară a lua și simetricele perechilor. De exemplu, dacă am gasit perechea {(0,0), (0,1)} nu vom număra și perechea {(0,1), (0,0)}.
* taierea a X (X≥1) linii. Cost: (nr coloane)/(nr linii taiate)


### 3. Fișierul de intrare

Fișierul de intrare va conține gridul inițial și starea scop, cu o linie vidă între ele:
```
ddaabbb
aaaffxc
aabccdc
adddaab

abb
axc
```

### 4. Euristici folosite

* #### Euristica banală - returnează 1 dacă nu este stare finală și 0 altfel. 
Există cazuri pentru care este inadmisibilă.
``` 
Stare finală  Stare curentă:                                    
     ab             ab
     ab             ab           tai ultimele 3 linii        
                    aa           --------------------->    ajung în starea finală cu un cost de 2/3, dar euristica a aproximat un cost mai mare, de 1. => inadmisibil      
                    bb                cost 2/3 
                    cc
```

* #### Euristica 1 - Ține cont dacă trebuie să tai linii și/sau coloane.
``` 
Formulă: costColoane + costLinii, unde costColoane = 1, nrColoaneStareCurentă != nrColoaneStareFinală  ; costLinii = nrColoaneStareFinală / (nrLiniiStareCurentă - nrLiniiStareFinală), nrLiniiStareCurentă != nrLiniiStareFinală 
                                                     0, altfel                                                       0, altfel
``` 
**Justificare**
Avem următoarele cazuri:
1. Starea curentă diferă de starea finală prin X coloane. 
Dacă X = 0, atunci nu trebuie să tăiem nimic și costColoane = 0.
Daca X != 0, în cel mai bun caz aceste coloane sunt toate adiacente și nu conțin perechi de vecini diferiți, deci putem să le tăiem cu un cost total de 1.
2. Starea curentă diferă de starea finală prin X linii.
Dacă X = 0, atunci nu trebuie să tăiem nimic și costLinii = 0.
Daca X != 0, în cel mai bun caz aceste linii sunt toate adiacente, iar numărul de coloane este minim posibil, adică egal cu numărul de coloane al stării finale. 
Așadar, înlocuind în formula pentru cost, putem să le tăiem cu un cost de nrColoaneStareFinală / (nrLiniiStareCurentă - nrLiniiStareFinală)

* Euristica 2 - Ține cont doar dacă trebuie să tai coloane, justificarea este aceeași ca mai sus

* Euristica inadmisibilă - Pentru fiecare linie/coloană care trebuie tăiată, consider costul 1.
Exemplu:
``` 
Stare finală  Stare curentă:                                    
     ab             ab
     ab             ab           tai ultimele 3 linii        
                    aa           --------------------->    ajung în starea finală cu un cost de 2/3, dar euristica a aproximat un cost mai mare, de 5-2 = 3. => inadmisibil      
                    bb                cost 2/3 
                    cc
``` 
