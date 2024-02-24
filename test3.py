# import numpy as np
#
# # 假设有一个矩阵
# matrix = np.array([
#     [1, 2, -1],
#     [4, 5, -1],
#     [7, 8, -1]
# ])
#
# matrix_weights = matrix / np.sum(matrix, axis=0)
# # 计算每一列的加权平均数
# weighted_average = np.sum(matrix * matrix_weights, axis=0)
# weighted_average = np.where(weighted_average==-1,0,weighted_average)
# feature_weight= weighted_average / np.sum(weighted_average)
# print(feature_weight)
# weighted_average_per_row = np.average(matrix, axis=1, weights=feature_weight)
# print(weighted_average_per_row)
#
#
#
#
# # 假设有一个一维数组
# arr = np.array([10, 5, 8, 3, 15])
#
# # 获取每个元素的大小排名
# element_ranks = np.argsort(arr)
#
# # element_ranks现在包含每个元素在原数组中的排名
# print("Element Ranks:", element_ranks)
# print(np.random.rand())


import re

text ="```jsonIntroducing the Prestige Electric Air Fryer PAF 6.0 - the perfect kitchen companion for roasting and baking enthusiasts! With its sleek black design and innovative technology, this air fryer allows you to cook a variety of dishes to perfection, all while using less oil than traditional deep-frying methods. Get ready to enjoy crispy roasted vegetables, juicy chicken, and delectable baked goods with the touch of a button. Upgrade your kitchen game with the Prestige Electric Air Fryer PAF 6.0!```"

pattern = re.compile(r"```json(.*?)```", re.DOTALL)
match = pattern.search(text)

if match:
    matched_content = match.group(1)
    print("Matched Content:")
    print(matched_content)
else:
    print("No match found.")