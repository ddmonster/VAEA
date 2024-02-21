import numpy as np
from modelservice.common.utils import Data_Base_Util
from fuzzywuzzy import process

class Search_Match():
    def __init__(self):
        self.dbu=Data_Base_Util()

    def get_all_product_feature_value_in_one_column(self,column_name):
        [is_success, return_value] = self.dbu.select_data_within_column(db=self.dbu.db_path(), table_name=self.dbu.table_name(),
                                                                   column_name=column_name)
        if is_success:
            return return_value
        else:

            raise Exception(f'Search all product value in column {column_name} error')

    def match_product_feature_value(self,feature_value,feature_name):
        all_product_value = self.get_all_product_feature_value_in_one_column(column_name=feature_name)

        score_list = []
        print(len(all_product_value))
        for product in all_product_value:
            match, score = process.extractOne(feature_value, [product])

            # 输出最匹配的字符串和匹配分数

            # print("Score:", score)
            score_list.append(score)
        # best_match = score_list.index(max(score_list))

        return np.asarray(score_list)

    # def match_product_type(self,product_type):
    #     all_product_name = self.get_all_product_name()
    #     best_match = process.extract(product_type, all_product_name,limit=999)
    #
    #     # 输出最匹配的字符串和匹配分数
    #     print("Best Match:", best_match)
    #     print("Best Match Length:", len(best_match))
    #     return best_match

if __name__ == '__main__':
    sm=Search_Match()
    sm.match_product_feature_value(feature_value='air fryer',feature_name='urls')
