# Jocul Vulpi Și Oi

* Jocul este intre doi jucatori. Unul din ei reprezinta vulpile și celălalt reprezintă oile.
* Scopul oilor este să ajungă să umple pătrățelul de sus (de 3x3=9 locații). Dacă jucătorul cu oile reușește acest lucru, atunci câștigă.
* Nu există o regulă referitoare la cine mută primul, așadar utilizatorul va fi întrebat, după ce a ales tipul de piese cu care dorește să joace, și dacă dorește să fie primul care mută
* Oile se pot muta doar în sus (pe coloană și diagonală) și în lateral (stânga sau dreapta) numai către o poziție conectată, imediat vecină (nu se trece printr-o altă poziție pentru a ajunge la ea). O poziție e conectată cu altă poziție dacă pe tabla de joc există o linie între ele.
* Vulpile se pot deplasa către o poziție conectată, imediat vecină, în orice direcție. Vulpile pot captura oi sărind peste ele. Pentru a putea sări peste o oaie, aceasta trebuie să fie pe o poziție conectată vecină cu o vulpe, și în aceeași direcție (în linie dreaptă, trasată pe tabla de joc, după ea) să se găsească o poziție liberă (în care va sări vulpea). După săritura, piesa corespunzătoare oii va fi luată de pe tabla de joc. Capturările se pot face și în lanț, dacă după capturarea unei piese există o altă piesă relativă la noua poziție a vulpii, îndeplinind condițiile de capturare. Capturarea este obligatorie (vulpea nu poate refuza să captureze oile) și trebuie să le captureze în lanț până nu mai are oi disponibile în lanțul respectiv. în felul asta se pot dezvolta strategii de a înlătura vulpea dintr-un loc dorit de oi (de exemplu, să scoată vulpea din pătrățelul de sus.
* Fiecare jucător mută o singură piesă când îi vine rândul.


Jocul se termină în următoarele situații:
- oile umplu pătrățelul de sus, caz în care câștigă oile
- vulpile capturează oi până când acestea ajung să fie mai puține de 9.
