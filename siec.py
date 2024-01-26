import json
import scipy
from datetime import datetime
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx import NetworkXError
from pyvis.network import Network
from networkx.algorithms import community


#Dla wszystkich na raz

with open('DATA/user_data', 'r') as json_file:
    user_data = json.load(json_file)

with open('DATA/game_data', 'r') as json_file:
    game_data = json.load(json_file)

# Dla 1000 najpopularniejszych gier
# top_1000_games_data = {}
# c = 0
# for game in game_data:
#     top_1000_games_data[game] = game_data[game]
#     c += 1
#     if c >= 1000:
#         break


# # Ze względu na wiek
# current_date = datetime.now()
# young_users = {}
# adult_users = {}
# old_users = {}
#
# # Ze względu na doświadczenie
# inexperienced_users = {}
# experienced_users = {}
# veteran_users = {}


# for user in user_data:
#     age = (current_date - datetime.strptime(user_data[user]["first_review"], "%Y-%m-%d")).days // 365
#     experience = user_data[user]["vote_count"]
#     if age < 5:
#         young_users[user] = user_data[user]
#     elif age < 10:
#         adult_users[user] = user_data[user]
#     else:
#         old_users[user] = user_data[user]
#     if experience > 40:
#         veteran_users[user] = user_data[user]
#     elif experience > 10:
#         experienced_users[user] = user_data[user]
#     else:
#         inexperienced_users[user] = user_data[user]


def graph_group_of_interest(group_of_interest, name):
    Graph = nx.Graph()
    nt = Network('1000px', '1000px')
    for game in top_1000_games_data:
        Graph.add_node(game)

    for user in group_of_interest:
        Graph.add_node(f"u{user}")
        for game in group_of_interest[user]["votes"]:
            if game in top_1000_games_data and group_of_interest[user]["votes"][game] >= 7:
                Graph.add_edge(f"u{user}", game)

    if nx.is_bipartite(Graph):
        New_graph = nx.bipartite.weighted_projected_graph(Graph,[game for game in top_1000_games_data])
        # print(f"Liczba węzłów: {New_graph.number_of_nodes()}")
        # print(f"Liczba krawędzi: {New_graph.number_of_edges()}")
        # print(f"Średni stopień węzłów: {np.mean(list(dict(New_graph.degree()).values()))}")
        # print(f"Współczynnik klastrowania: {nx.average_clustering(New_graph)}")
        # try:
        #     print(f"Średnica grafu: {nx.diameter(New_graph)}")
        # except NetworkXError:
        #     print("Graf nie jest spójny")
        # try:
        #     communities = list(community.girvan_newman(New_graph))
        #     print(f"Grupowania dla {name}: {communities}")
        #     modularity = community.modularity(communities, New_graph)
        #     print(f"Modularność dla {name}: {modularity}")
        # except:
        #     print(f"Nie udało się znaleźć grupowań dla {name}")


        pos = nx.kamada_kawai_layout(New_graph, scale=20)
        nx.draw(New_graph, pos, with_labels=True)
        plt.title(f"Graph for Group of Interest: {name}")
        plt.savefig(f"Images/Graph_{name}.png")

    else:
        print("Powstaly graf nie jest dwudzielny")

print("Dla młodych użytkowników")
graph_group_of_interest(young_users, "young_users")
# print("Dla dojrzałych użytkowników")
# graph_group_of_interest(adult_users, "adult_users")
# print("Dla starych użytkowników")
# graph_group_of_interest(old_users, "old_users")
# print("Dla niedoświadczonych użytkowników")
# graph_group_of_interest(inexperienced_users, "inexperienced_users")
# print("Dla doświadczonych użytkowników")
# graph_group_of_interest(experienced_users, "experienced_users")
# print("Dla weteranów")
# graph_group_of_interest(veteran_users, "veteran_users")

# with open(f"Results/{name}_results.txt", "w") as file:
# file.write(f"Liczba węzłów: {New_graph.number_of_nodes()}")
# file.write(f"Liczba krawędzi: {New_graph.number_of_edges()}")
# file.write(f"Średni stopień węzłów: {np.mean(list(dict(New_graph.degree()).values()))}")
# file.write(f"Współczynnik klastrowania: {nx.average_clustering(New_graph)}")
# file.write(f"Średnica grafu: {nx.diameter(New_graph)}")
# nt.from_nx(New_graph)
# nt.show('nx.html', notebook=False)

