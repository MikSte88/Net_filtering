from vndb_thigh_highs import VNDB, Config
from vndb_thigh_highs.models import VN, User, UserVN
import time


config = Config()
config.set_login("Okrutnik", "6BwSnYoKRy")
vndb = VNDB(config=config)
db_stats = vndb.dbstats()
user_vns = vndb.get_all_ulist(UserVN.user_id < 200)

# for user in user_vns:
#     print('xd')
#     print(user)
