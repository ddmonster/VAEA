import numpy as np

# 假设有一个矩阵
matrix = np.array([
    [1, 2, -1],
    [4, 5, -1],
    [7, 8, -1]
])

matrix_weights = matrix / np.sum(matrix, axis=0)
# 计算每一列的加权平均数
weighted_average = np.sum(matrix * matrix_weights, axis=0)
weighted_average = np.where(weighted_average==-1,0,weighted_average)
feature_weight= weighted_average / np.sum(weighted_average)
print(feature_weight)
weighted_average_per_row = np.average(matrix, axis=1, weights=feature_weight)
print(weighted_average_per_row)




# 假设有一个一维数组
arr = np.array([10, 5, 8, 3, 15])

# 获取每个元素的大小排名
element_ranks = np.argsort(arr)

# element_ranks现在包含每个元素在原数组中的排名
print("Element Ranks:", element_ranks)
print(np.random.rand())
