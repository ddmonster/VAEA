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

    def match_product_feature_value(self,feature_name,feature_value):
        all_product_value = self.get_all_product_feature_value_in_one_column(column_name=feature_name)

        score_list = []
        for product in all_product_value:
            match, score = process.extractOne(feature_value, [product])
            score_list.append(score)

        print(score_list)
        return np.asarray(score_list)


    def create_attention_matrix(self,feature_json,data_num):
        i = 0
        init_matrix = np.full((data_num, 15), -1)
        for k,v in feature_json.items():
            print(k,v)
            if ((v is None)|(v=='')):
                i+=1
                continue
            score_list=self.match_product_feature_value(feature_name=k,feature_value=v)

            init_matrix[:, i] = score_list
            i+=1
        return init_matrix

    def get_feature_weights(self,matrix):
        matrix_weights = matrix / np.sum(matrix, axis=0)
        weighted_average = np.sum(matrix * matrix_weights, axis=0)
        weighted_average = np.where(weighted_average==-1,0,weighted_average)
        random_number = np.random.rand()
        if random_number<= 0.5:
            feature_weight= weighted_average / np.sum(weighted_average)
        else:
            feature_weight = (np.argsort(weighted_average)+1)/len(weighted_average)
        return feature_weight

    def get_attention_item(self,attention_matrix):
        feature_weight = self.get_feature_weights(matrix=attention_matrix)
        row_sums = np.average(attention_matrix, axis=1, weights=feature_weight)
        max_attention_index = np.argmax(row_sums)
        print(max_attention_index)
        result = self.dbu.get_a_row(db=self.dbu.db_path(),table_name=self.dbu.table_name(),row_num=max_attention_index)
        if result is None:
            raise Exception('Get most attention item failed')
        else:
            print(f'Best result is: {result[1][0]}')
            return result[1][0]

    # def match_product_type(self,product_type):
    #     all_product_name = self.get_all_product_name()
    #     best_match = process.extract(product_type, all_product_name,limit=999)
    #
    #     # 输出最匹配的字符串和匹配分数
    #     print("Best Match:", best_match)
    #     print("Best Match Length:", len(best_match))
    #     return best_match

if __name__ == '__main__':

    from modelservice.database.dataset import Dateset
    from modelservice.feature_engineering.feature_extraction import Feature_Engineering

    sentence = "I'd like to buy a red PHILIPS fryer that has 3.2 litres and mades by plastic and the maximum energy consumption is two thousand wattage.I can use it to roast, broil and steam. In addition the product cannot be sold for more than 3000 rupee and the home kitchen rank is about 23000. Also, it should have the nonstick.Finally, it should be made in China and weight less than six kilograms."

    ds = Dateset()
    data_num = ds.make_dataset()

    fe = Feature_Engineering()
    result = fe.extraction(sentence=sentence)

    sm=Search_Match()
    attention_matrix = sm.create_attention_matrix(feature_json=result,data_num=data_num)
    best_item = sm.get_attention_item(attention_matrix=attention_matrix)

