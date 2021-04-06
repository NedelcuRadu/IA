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

*  #### Euristica 2 - Ține cont doar dacă trebuie să tai coloane, justificarea este aceeași ca mai sus

*  #### Euristica inadmisibilă - Pentru fiecare linie/coloană care trebuie tăiată, consider costul 1.
Exemplu:
``` 
Stare finală  Stare curentă:                                    
     ab             ab
     ab             ab           tai ultimele 3 linii        
                    aa           --------------------->    ajung în starea finală cu un cost de 2/3, dar euristica a aproximat un cost mai mare, de 5-2 = 3. => inadmisibil      
                    bb                cost 2/3 
                    cc
``` 

### 5. Compararea algoritmilor pentru fișierele input1 și input2

| Algoritmul folosit                    	| Lungimea drumului 	| Costul drumului 	| Numărul maxim de noduri în memorie 	| Numărul total de noduri generate 	| Timpul pentru a găsi soluția (ms) 	|
|---------------------------------------	|-------------------	|:---------------:	|:----------------------------------:	|:--------------------------------:	|-----------------------------------	|
| Uniform Search                        	| 3 / 4             	|    4.4 / 6.25   	|              702 / 822             	|            770 / 1017            	| 40 / 86                           	|
| A* - euristica banală                 	| 3 / 4             	|    4.4 / 6.25   	|              300 / 432             	|             320 / 502            	| 15 / 27                           	|
| A* - euristica 1                      	| 3 / 4             	|    4.4 / 6.25   	|              89 / 159              	|             94 / 193             	| 5 / 12                            	|
| A* - euristica 2                      	| 3 / 4             	|    4.4 / 6.25   	|              300 / 426             	|             321 / 502            	| 16 / 29                           	|
| A* - euristica inadmisibilă           	| 3 / 4             	|    4.4 / 6.25   	|              694 / 782             	|             761 / 966            	| 36 / 56                           	|
| A* optimizat - euristica banală       	| 3 / 4             	|    4.4 / 6.25   	|              201 / 199             	|             278 / 374            	| 28 / 33                           	|
| A* optimizat - euristica 1            	| 3 / 4             	|    4.4 / 6.25   	|              80 / 101              	|             84 / 149             	| 13 / 29                           	|
| A* optimizat - euristica 2            	| 3 / 4             	|    4.4 / 6.25   	|              200 / 200             	|             279 / 377            	| 59 / 56                           	|
| A* optimizat - euristica inadmisibilă 	| 6  / 4            	|   11.75 /6.25   	|             1344 / 257             	|            5373 / 537            	| 1462 / 64                         	|
| IDA* - euristica banală               	| 3 / 4             	| 4.4 / 6.25      	|  53 / 163                          	| 1636 / 4820                      	| 105 / 312                         	|
| IDA* - euristica 1                    	| 3  / 4            	|    4.4 / 6.25   	|              77 / 186              	|            349 / 1133            	| 23 / 74                           	|
| IDA* - euristica 2                    	| 3 / 4             	|    4.4 / 6.25   	|              109 / 215             	|            1810 / 5321           	| 109 / 344                         	|
| IDA* - euristica inadmisibilă         	| 3 / 4             	|    4.4 / 6.25   	|              146 / 242             	|           6516 / 14895           	| 461 / 1074                        	|
