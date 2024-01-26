import matplotlib.pyplot as plt
import json
from datetime import datetime


with open('DATA/user_data', 'r') as json_file:
    user_data = json.load(json_file)

with open('DATA/game_data', 'r') as json_file:
    game_data = json.load(json_file)

scores = []
for game in game_data:
    scores.append(game_data[game]["average_score"])

game_votes = []
for game in game_data:
    game_votes.append(game_data[game]["votes_count"])

review_counts = []
for user in user_data:
    review_counts.append(user_data[user]["vote_count"])

date_strings = []
for user in user_data:
    date_strings.append(user_data[user]["first_review"])

dates = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in date_strings]
dates.sort()
current_date = datetime.now()
ages = [(current_date - date_obj).days // 365 for date_obj in dates]

# print(min(ages))
# print(max(ages))
# plt.hist(ages, bins=range(0, 17))
# plt.title("Histogram wieku działalności użytkowników")
# plt.xlabel("Wiek (lata)")
# plt.ylabel("Ilość użytkowników")
# plt.xticks(range(0, 17))
# plt.savefig("Images/histogram_wieku.png")
# plt.show()

# plt.hist(review_counts, bins= range(0, 160, 10))
# plt.xticks(range(0, 150, 10))
# plt.title("Histogram ilości ocen użytkowników")
# plt.xlabel("Ilość ocen")
# plt.ylabel("Ilość użytkowników")
# plt.savefig("Images/ilosc_ocen_uzytkownika.png")
# plt.show()
#
plt.hist(review_counts, log=True)
plt.title("Histogram ilości ocen użytkowników")
plt.xlabel("Ilość ocen")
plt.ylabel("Ilość użytkowników")
# plt.savefig("Images/ilosc_ocen_uzytkownika_log.png")
plt.show()
#
#
#
# plt.hist(scores, bins=range(10))
# plt.title("Histogram ocen gier")
# plt.xlabel("Wynik")
# plt.ylabel("Ilość gier")
# plt.savefig("Images/oceny_gier.png")
# plt.xticks(range(0, 10))
# plt.show()
#
# plt.hist(game_votes)
# plt.title("Histogram ilości ocen dla gier")
# plt.xlabel("Ilość ocen")
# plt.ylabel("Ilość gier")
# plt.savefig("Images/ilosc_ocen_gier.png")
# plt.show()
#
plt.hist(game_votes, bins=range(0,20000, 1000), log=True)
plt.title("Histogram ilości ocen dla gier")
plt.xlabel("Ilość ocen")
plt.ylabel("Ilość gier")
plt.savefig("Images/ilosc_ocen_gier_Log.png")
plt.show()


