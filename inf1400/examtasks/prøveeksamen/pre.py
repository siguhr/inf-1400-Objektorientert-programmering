import random

types = ["lastebil", "buss", "tog", "bil"]
types_vekting = [10, 2, 1, 50]
dekk_verdi = ["piggfritt", "piggdekk", "kjetting"]
dekk_vekting = [5, 5, 1]

strekning_dekke = ["asfalt", "betong", "grus"]
strekning_vekting = [10, 2, 5]

overflatedekke = ["yes", "no"]
overflatedekke_vekting = [1, 10]

class object():
    def __init__(self, vekt):
        self.max_vekt = vekt

    def lag_kjoretoy():
        kjoretoy = {}
        kjoretoy["type"] = random.choices(types, types_vekting)[0]
        kjoretoy["dekk"] = random.choices(dekk_verdi, dekk_vekting)[0]
        return kjoretoy

    def kjor_over(kjoretoy, strekning):
        strekning["holdbarhet"] -= slitasje(kjoretoy)

class lastebil(object):
    def __init__(self, vekt):
        super().__init__(vekt)

    def slitasje(kjoretoy):
        slitasje = 0
        if kjoretoy["type"] == "lastebil":
            slitasje = 300
        if kjoretoy["dekk"] == "piggdekk":
            slitasje *= 3
        if kjoretoy["dekk"] == "kjetting":
            slitasje *= 10
        return slitasje

class buss(object):
    def __init__(self, vekt):
        super().__init__(vekt)


    def slitasje(kjoretoy):
        slitasje = 0
        if kjoretoy["type"] == "buss":
            slitasje = 100
        if kjoretoy["dekk"] == "piggdekk":
            slitasje *= 3
        if kjoretoy["dekk"] == "kjetting":
            slitasje *= 10
        return slitasje

class tog(object):
    def __init__(self, vekt):
        super().__init__(vekt)
        pass

    def slitasje(kjoretoy):
        slitasje = 0
        if kjoretoy["type"] == "tog":
            slitasje = 0

        if kjoretoy["dekk"] == "piggdekk":
            slitasje *= 0
        if kjoretoy["dekk"] == "kjetting":
            slitasje *= 0
        return slitasje

class bil(object):
    def __init__(self, vekt):
        super().__init__(vekt)

    def slitasje(kjoretoy):
        slitasje = 0
        if kjoretoy["type"] == "bil":
            slitasje = 10
            
        if kjoretoy["dekk"] == "piggdekk":
            slitasje *= 3
        if kjoretoy["dekk"] == "kjetting":
            slitasje *= 10

        if kjoretoy["overflatedekke"] == "no":
            return slitasje
        
        if kjoretoy["overflatedekke"] == "yes":
            
        return slitasje

class veistrekning():
    def __init__(self):
        pass

    def lag_veistrekning(nummer):
        strekning = {}
        overflate = {}
        strekning["nummer"] = nummer
        strekning["trenger_vedlikehold"] = False
        strekning["dekke"] = random.choices(strekning_dekke, strekning_vekting)[0]
        if strekning["dekke"] == "asfalt":
            strekning["holdbarhet"] = 10000
        if strekning["dekke"] == "betong":
            strekning["holdbarhet"] = 50000
        if strekning["dekke"] == "grus":
            strekning["holdbarhet"] = 3000

            
        return strekning

            if overflate["dekke"] == "yes":
                if strekning["dekke"] == "betong":

                strekning.beregn_overflatedekke_betong(strekning)
                return strekning
        

class overflatedekk(veistrekning):
    def __init__(self):
        super().__init__(self)
        pass
    
    def beregn_overflatedekke (kjoretoy):
        slitasje *= 0.40 

    






if __name__ == "__main__":
    kjoretoy = []
    strekninger = []
    for _ in range(1000):
        kjoretoy.append(lag_kjoretoy())
    for n in range(50):
        strekninger.append(lag_veistrekning(n))
    for k in kjoretoy:
        for s in strekninger:
            kjor_over(k, s)
            if s["holdbarhet"] < 1000 and not s["trenger_vedlikehold"]:
                print("Strekning {} må vedlikeholdes!".format(s["nummer"]))
                s["trenger_vedlikehold"] = True