



true = 1
false = 0

# oppgave 1 a)

import pygame

class Transportmiddel():
    def __init__(self, lastekapasitet, personkapasitet, vekt): 
        self.lastekapasitet = lastekapasitet
        self.personkapasitet = personkapasitet
        self.vekt = vekt

class Personbil (Transportmiddel):
    def __init__(self, lastekapasitet, personkapasitet, vekt, piggdekk):
        super().__init__(lastekapasitet, personkapasitet, vekt)
        self.piggdekk = piggdekk

class Buss (Transportmiddel):
    def __init__(self, lastekapasitet, personkapasitet, vekt, piggdekk, kjetting):
        super().__init__(lastekapasitet, personkapasitet, vekt)
        self.piggdekk = piggdekk
        self.kjetting = kjetting

class Lastebil(Transportmiddel):
    def __init__ (self, lastekapasitet, personkapasitet, vekt, piggdekk, kjetting):
        super().__init__(lastekapasitet, personkapasitet,vekt)
        self.piggdekk = piggdekk
        self.kjetting = kjetting

class Tog (Transportmiddel):
    def __init__(self, lastekapasitet, personkapasitet, vekt):
        super().__init__(lastekapasitet, personkapasitet, vekt)


# oppgave 1 b)

# Da init-metoden er definert i 1a, viser jeg bare at jeg lager ett objekt
# Dette objektet har attributter:
# piggdekk, kjetting
# lastekapasitet, personkapasitet, vekt - arvet fra parent

lastebil = Lastebil (1000, 3, 2000, true, false)


# Oppgave 2 a)


FAKTOR_BIL = 10
FAKTOR_BUSS = 100
FAKTOR_LASTEBIL = 300
FAKTOR_TOG = 0



def slitasje(transportmiddel):
    sann_slitasje = 0
    for t in transportmiddel:
        if isinstance(t, Personbil):
            sann_slitasje =+ FAKTOR_BIL
        if isinstance(t, Buss):
            sann_slitasje =+ FAKTOR_BUSS
        if isinstance(t, Lastebil):
            sann_slitasje =+ FAKTOR_LASTEBIL
        if isinstance(t, Tog):
            sann_slitasje =+ FAKTOR_TOG

    return sann_slitasje
    

# Oppgave 2 b)



class Lastebil(Transportmiddel):
    SLITASJE_FAKTOR = 100
    def __init__ (self, lastekapasitet, personkapasitet, vekt, piggdekk, kjetting):
        super().__init__(lastekapasitet, personkapasitet,vekt)
        self.piggdekk = piggdekk
        self.kjetting = kjetting

def slitasje2(transportmiddel):
    return sum((t.SLITASJE_FAKTOR for t in transportmiddel))

# Oppgave 3

# Utregning av slitasje for forskjellige objecter (må legges i metoder).

# Personbil
slitasje_verdi = self.vekt * self.SLITASJE_FAKTOR
    if self.piggdekk:
        slitasje_verdi *= 3

# Lastebil eller buss
slitasje_verdi = self.vekt * math.log(self.vekt) * self.SLITASJE_FAKTOR

if self.piggdekk:
    slitasje_verdi *= 3
if self.kjetting:
    slitasje_verdi *= 10

#Tog - settes til 0 

#Hovedfunksjon som regner ut total slitasje for mange objecter

def slitasje(transportmiddel)
    total = 0 
    for tm in transportmiddel:
        total += tm.slitasje()
    return total


#New class (for Tog og lastebil)
class tungtransport(transportmiddel):
    def __init__ (self, lastekapasitet, personkapasitet)
    super().__init__(lastekapasitet, personkapasitet, vekt)
    slitasje_verdi = self.vekt * math.log(self.vekt) * self.SLITASJE_FAKTOR
    

 
