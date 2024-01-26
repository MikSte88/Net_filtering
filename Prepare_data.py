import csv
import numpy as np
import json
from datetime import datetime

# vndb-votes-2024-01-09
# " Each line contains the VN id, user ID, vote, and date that the vote was cast,
# separated by a space. Votes are as listed on the site, multiplied by 10 (i.e. in the range of 10 - 100)."

# Kto zagłosował na co?

# Zamien na plik json po {uid: {"votes" : { vid : vote},
#                               "first_rev" : first_review_date}, WIEK
#                               "vote_count" : vote_count} ,DOŚWIADCZENIE

user_data = {}
game_data = {}

with open('vndb-votes-2024-01-09', "r") as file:
    for line in file:
        vn_id, user_id, vote, date_str = line.strip().split()
        vote = int(vote) // 10
        user_id = int(user_id)
        date = datetime.strptime(date_str, "%Y-%m-%d")

        if user_id not in user_data:
            user_data[user_id] = {"votes": {vn_id : vote},
                                  "first_review": date.strftime("%Y-%m-%d"),
                                  "vote_count": 1}
        else:
            user_data[user_id]["votes"][vn_id] = vote
            user_data[user_id]["vote_count"] += 1
            if date < datetime.strptime(user_data[user_id]["first_review"], "%Y-%m-%d"):
                user_data[user_id]["first_review"] = date.strftime("%Y-%m-%d")

        if vn_id not in game_data:
            game_data[vn_id] = {"average_score": vote,
                                "votes_count": 1}
        else:
            game_data[vn_id]["votes_count"] += 1
            game_data[vn_id]["average_score"] = np.round(game_data[vn_id]["average_score"] + ((vote - game_data[vn_id]["average_score"]) / game_data[vn_id]["votes_count"]),2)

sorted_game_data = dict(sorted(game_data.items(), key=lambda x: x[1]['votes_count'], reverse=True))
# sorted_user_data = dict(sorted(user_data.items()))
#
# with open('DATA/user_data', 'w') as json_file:
#     json.dump(sorted_user_data, json_file, indent=4)

with open('DATA/game_data', 'w') as json_file:
    json.dump(sorted_game_data, json_file, indent=2)
