import json
import  numpy as np
import matplotlib.pyplot as plt

with open('Wyniki.json', 'r') as json_file:
    wyniki = json.load(json_file)

sr_czasy_pracy = []
sr_gestosci = []
sr_sr_stopnie = []


oryginalny_sredni_stopien= wyniki["Wszystkie_gry+Wszyscy_gracze"]["sredni_stopien_wezla"]
oryginalna_gestosc= wyniki["Wszystkie_gry+Wszyscy_gracze"]["gestosc"]
czas_pracy = wyniki["Wszystkie_gry+Wszyscy_gracze"]["czas_pracy"]
oryginalny_czas_pracy = czas_pracy["godziny"] * 3600 + czas_pracy["minuty"] * 60 + czas_pracy["sekundy"]

wyniki_porownania = {}

min_delta_g = np.inf
min_delta_st = np.inf
min_delta_cp = np.inf


for wynik in wyniki:
    if wynik != "Wszystkie_gry+Wszyscy_gracze":
        t = {}
        czas_pracy = wyniki[wynik]["czas_pracy"]
        czas_pracy_w_sekundach = czas_pracy["godziny"] * 3600 + czas_pracy["minuty"] * 60 + czas_pracy["sekundy"]
        gestosc = wyniki[wynik]["gestosc"]
        sr_stopien = wyniki[wynik]["sredni_stopien_wezla"]
        delta_g = np.abs(gestosc - oryginalna_gestosc)
        t["delta_g"] = delta_g
        delta_st = np.abs(sr_stopien - oryginalny_sredni_stopien)
        t["delta_st"] = delta_st
        delta_cp = np.abs(czas_pracy_w_sekundach - oryginalny_czas_pracy)
        t["delta_cp"] = delta_cp
        wyniki_porownania[wynik] = t
        sr_czasy_pracy.append(delta_cp)
        sr_gestosci.append(delta_g)
        sr_sr_stopnie.append(delta_st)

sr_czasy_pracy = np.mean(sr_czasy_pracy)
sr_gestosci = np.mean(sr_gestosci)
sr_sr_stopnie = np.mean(sr_sr_stopnie)


def ocen_filtry(slownik, waga_g, waga_st, waga_cp):
    min_w = 0
    min_n = ""
    for klucz in slownik:
        wynik = slownik[klucz]
        f_celu = 0
        f_celu += (wynik["delta_g"] / sr_gestosci) * waga_g
        f_celu += (wynik["delta_st"] / sr_sr_stopnie) * waga_st
        f_celu += (wynik["delta_cp"] / sr_czasy_pracy) * waga_cp

        if f_celu < min_w:
            min_w = f_celu
            min_n = klucz
    return min_n

print(ocen_filtry(wyniki_porownania, 1, 5, -1))
print(wyniki["Wszystkie_gry+Wszyscy_gracze"])
print(wyniki[ocen_filtry(wyniki_porownania, 1, 5, -1)])
