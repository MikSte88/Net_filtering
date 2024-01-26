import networkx as nx
import json
import random
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


with open('DATA/user_data', 'r') as json_file:
    user_data = json.load(json_file)

with open('DATA/game_data', 'r') as json_file:
    game_data = json.load(json_file)

Graph = nx.Graph()


wszystkie_wyniki = {}

def czas_pracy(czas_rozpoczecia, czas_zakonczenia):
    czas_pracy = czas_zakonczenia - czas_rozpoczecia
    godziny, remainder = divmod(czas_pracy.seconds, 3600)
    minuty, sekundy = divmod(remainder, 60)
    return {"godziny": godziny, "minuty": minuty, "sekundy": sekundy}


def losuj_1000(dane, ilosc):

    klucze = list(dane.keys())


    polowa_kluczy = random.sample(klucze, ilosc)


    nowy_slownik = {klucz: dane[klucz] for klucz in polowa_kluczy}

    return nowy_slownik


def podziel_i_posortuj_gry_jakosc(słownik_gier):

    posortowane = sorted(słownik_gier.items(), key=lambda x: x[1]['average_score'], reverse=True)


    najlepsze = dict(posortowane[:1000])
    reszta = dict(posortowane[1000:])

    return najlepsze, reszta


def podziel_słownik(słownik, liczba):

    klucze = list(słownik.keys())


    pierwsze_1000 = klucze[:liczba]
    reszta = klucze[liczba:]

    słownik_1000 = {klucz: słownik[klucz] for klucz in pierwsze_1000}
    reszta_słownika = {klucz: słownik[klucz] for klucz in reszta}

    return słownik_1000, reszta_słownika


def podziel_słownik_graczy(słownik):
    posortowane_oceny = sorted(słownik.items(), key=lambda x: x[1]['vote_count'], reverse=True)

    najlepsze = dict(posortowane_oceny[:10000])
    reszta = dict(posortowane_oceny[10000:])

    return najlepsze, reszta


def badanie(gracze, gry,tytul, pozytywne=False, negatywne=False):
    print(tytul)
    wyniki = {}
    Graph = nx.Graph()
    Graph.clear()
    for game in gry:
        Graph.add_node(game)

    for user in gracze:
        Graph.add_node(f"u{user}")
        for game in gracze[user]["votes"]:
            if game in gry:
                if pozytywne:
                    if int(gracze[user]["votes"][game]) >= 7:
                        Graph.add_edge(f"u{user}", game)
                elif negatywne:
                    if int(gracze[user]["votes"][game]) <= 6:
                        Graph.add_edge(f"u{user}", game)
                else:
                    Graph.add_edge(f"u{user}", game)



    if nx.is_bipartite(Graph):
        try:
            print(datetime.now())
            czas_rozpoczecia = str(datetime.now())

            New_graph = nx.bipartite.weighted_projected_graph(Graph, nodes=[game for game  in gry])
            

            liczba_wzelow = New_graph.number_of_nodes()
            print(f"Liczba węzłów: {liczba_wzelow}")
            wyniki["liczba_wezlow"] = liczba_wzelow

            liczba_krawdzi = New_graph.number_of_edges()
            print(f"Liczba krawędzi: {liczba_krawdzi}")
            wyniki["liczba_krawedzi"] = liczba_krawdzi

            sredni_stopien_wezla = np.mean(list(dict(New_graph.degree()).values()))
            print(f"Średni stopień węzłów: {sredni_stopien_wezla}")
            wyniki["sredni_stopien_wezla"] = sredni_stopien_wezla

            gestosc = nx.density(New_graph)
            print(f"Gęstość: {gestosc}")
            wyniki["gestosc"] = gestosc

            print(datetime.now())

            plt.figure(figsize=(10, 10))
            New_graph.remove_nodes_from(list(nx.isolates(New_graph)))
            layout = nx.fruchterman_reingold_layout(New_graph)
            nx.draw(New_graph, pos=layout, with_labels=False, node_size=1, width=0.1)
            plt.title(f"{tytul} fruchterman reingold bez pojedynczych")
            plt.savefig(f"Grafy/graf_{tytul}_fruchterman_bez_pojedynczych.png")
        except MemoryError:
            print("ZA MALO PAMIECI BLAD - Blad")
            pass

        czas_zakonczenia = str(datetime.now())

        czas_pracy_wynik = czas_pracy(datetime.strptime(czas_rozpoczecia, "%Y-%m-%d %H:%M:%S.%f"),
                                      datetime.strptime(czas_zakonczenia, "%Y-%m-%d %H:%M:%S.%f"))
        wyniki["czas_pracy"] = czas_pracy_wynik

        # wszystkie_wyniki[tytul] = wyniki
        # with open(f'Results/{tytul}', 'w') as json_file:
        #     json_file.write(json.dumps(wyniki, indent=2))

    return 0

# Filtry graczy
gracze_losowi = losuj_1000(user_data, 10000)
top_10000_graczy, reszta_10000_graczy = podziel_słownik_graczy(user_data)

# Filtry gier
top_1000_gier_jakosc, reszta_1000_gier_jakosc = podziel_i_posortuj_gry_jakosc(game_data)
gry_losowe = losuj_1000(game_data, 1000)
top_1000_gier_popularnosc, reszta_1000_gier_popularnosc = podziel_słownik(game_data, 1000)

kat_graczy = [[user_data, "Wszyscy_gracze"], [gracze_losowi, "Losowe_10000_graczy"],
              [top_10000_graczy, "10000_najaktywniejszych_graczy"], [reszta_10000_graczy, "Wszyscy_gracze_poza_10000_najaktywniejszych"]]

kat_gier = [[game_data,"Wszystkie_gry"], [top_1000_gier_popularnosc, "1000_najpopularniejszych_gier"],
            [reszta_1000_gier_popularnosc, "Wszyskie_gry_poza_1000_najpopularniejszych"], [top_1000_gier_jakosc, "1000_najwyżej_ocenionych_gier"],
            [reszta_1000_gier_jakosc, "Wszyskie_gry_poza_1000_najwyzej_ocenionychh"], [gry_losowe, "Losowe_1000_gier"]]


# for filtr_gier in kat_gier:
#     for filtr_graczy in kat_graczy:
#         if filtr_gier[1] == "Wszystkie_gry" and filtr_graczy[1]== "Wszyscy_gracze":
#             pass
#         else:
#             badanie(filtr_graczy[0], filtr_gier[0], f"{filtr_gier[1]}+{filtr_graczy[1]}")
#             badanie(filtr_graczy[0], filtr_gier[0], f"{filtr_gier[1]}+{filtr_graczy[1]}+neg", negatywne=True)
#             badanie(filtr_graczy[0], filtr_gier[0], f"{filtr_gier[1]}+{filtr_graczy[1]}+poz", pozytywne=True)

# for filtr_gier in kat_gier:
#     for filtr_graczy in kat_graczy:
#         if filtr_gier[1] == "Wszystkie_gry" and filtr_graczy[1]== "Wszyscy_gracze":
#             badanie(filtr_graczy[0], filtr_gier[0], f"{filtr_gier[1]}+{filtr_graczy[1]}")
#             badanie(filtr_graczy[0], filtr_gier[0], f"{filtr_gier[1]}+{filtr_graczy[1]}+neg", negatywne=True)
#             badanie(filtr_graczy[0], filtr_gier[0], f"{filtr_gier[1]}+{filtr_graczy[1]}+poz", pozytywne=True)

badanie(top_10000_graczy, reszta_1000_gier_popularnosc, "Wszyskie_gry_poza_1000_najpopularniejszych+10000_najaktywniejszych_graczy")
# with open(f'Results/Calosc', 'w') as json_file:
#     json_file.write(json.dumps(wszystkie_wyniki, indent=2))
