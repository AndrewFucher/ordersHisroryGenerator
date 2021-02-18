# a1 = {"a": ["1", "2", "3"], "b" : {"1" : 4}}

# b1 = {"a": ["50", "2"], "b": {"1": 1, "2": [3, 4]}}

# def merge(a, b):
#     "merges b into a"
#     for key in b:
#         if key in a:# if key is in both a and b
#             if isinstance(a[key], dict) and isinstance(b[key], dict): # if the key is dict Object
#                 merge(a[key], b[key])
#             else:
#               a[key] = b[key]
#         else: # if the key is not in dict a , add it to dict a
#             a.update({key:b[key]})
#     return a

# c = merge(a1, b1)
# print(c)

# from datetime import date, datetime

# print(str(datetime.now()))

from datetime import date, datetime

# print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")))

import ordersHistoryGenerator
import json
from constants import *

with open("./config.json", "r") as file:
    config = json.load(file)

idList, sideList, instrumentList, px_InitList, px_FillList, volume_InitList, volume_FillList, notesList, tagsList, statusList, datetimeList = ordersHistoryGenerator.generateData(config)

# print(round(123456, -3))
# len(idList)
for i in range(1000, 7200):
    print("\t".join([str(i) for i in [idList[i], sideList[i], instrumentList[i], px_InitList[i], px_FillList[i], volume_InitList[i], volume_FillList[i], notesList[i], tagsList[i], statusList[i], datetimeList[i]]]))

# a = 3
# print("'{}'".format(a))
# print(date.today())

# seed = 1
# for i in range(30):
#     seed = (seed * LCG_A + LCG_C)%LCG_M
#     print(seed)

# print(divmod(496298443601 * LCG_A + LCG_C, LCG_M))