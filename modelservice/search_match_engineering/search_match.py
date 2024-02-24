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

        return np.asarray(score_list)


    def create_attention_matrix(self,feature_json,data_num):
        i = 0
        init_matrix = np.full((data_num, 15), -1)
        for k,v in feature_json.items():
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
        result = self.dbu.get_a_row(db=self.dbu.db_path(),table_name=self.dbu.table_name(),row_num=max_attention_index)
        if result is None:
            raise Exception('Get most attention item failed')
        else:
            print(f'Best result is: {result[1][0]}')
            return result[1][0]

    def fuzzy_matching(self,feature_result,data_num):
        attention_matrix = self.create_attention_matrix(feature_json=feature_result, data_num=data_num)
        best_item = self.get_attention_item(attention_matrix=attention_matrix)
        return best_item

    def exact_match(self,product_name):
        result=self.dbu.select_data_within_kv(db = self.dbu.db_path(),table_name=self.dbu.table_name(),kv = {'product_name':f'{product_name}'})
        if result is None:
            raise Exception('Exact matching failed')
        else:
            match_result = result[1]
            if len(match_result)>0:
                return match_result[0]
            else:
                return None

    def match_product(self,feature_result,data_num):
        product_name = feature_result["product_name"]
        if (product_name is None) | (product_name == ""):
            best_item = self.fuzzy_matching(feature_result=feature_result,data_num=data_num)
            print('Product name is None')
            return best_item

        else:
            #从数据库精准匹配产品名
            exact_match = self.exact_match(product_name=product_name)
            if exact_match is None: #匹配不到就模糊匹配
                best_item = self.fuzzy_matching(feature_result=feature_result, data_num=data_num)
                print('Cannot match product name using exact match, turning to fuzzy match')
                return best_item
            else: #匹配到了就直接输出
                print('Can match product name using exact match')
                return exact_match



if __name__ == '__main__':

    from modelservice.database.dataset import Dateset
    from modelservice.feature_engineering.feature_extraction import Feature_Engineering
    from modelservice.product_text_generation_engineering.llm_generation_text import Genertion_Text

    sentence = "I'd like to buy a red PHILIPS fryer that has 3.2 litres and mades by plastic and the maximum energy consumption is two thousand wattage.I can use it to roast, broil and steam. In addition the product cannot be sold for more than 3000 rupee and the home kitchen rank is about 23000. Also, it should have the nonstick.Finally, it should be made in China and weight less than six kilograms."
    # sentence = "I'd like to buy a red PHILIPS fryer named PHILIPS Digital Air Fryer that has 3.2 litres and mades by plastic and the maximum energy consumption is two thousand wattage.I can use it to roast, broil and steam. In addition the product cannot be sold for more than 3000 rupee and the home kitchen rank is about 23000. Also, it should have the nonstick.Finally, it should be made in China and weight less than six kilograms."


    ds = Dateset()
    data_num = ds.make_dataset()

    fe = Feature_Engineering()
    result = fe.extraction(sentence=sentence)
    #要开发一个产品名精准匹配，如果匹配到了直接输出结果不用进入搜索匹配算法
    if (result is None) | (result == 'None'):
        feedback = f'Feature json is {result}. Cannot find any feature, please try again'
        print(feedback)
    else:
        sm=Search_Match()
        # attention_matrix = sm.create_attention_matrix(feature_json=result,data_num=data_num)
        # best_item = sm.get_attention_item(attention_matrix=attention_matrix)
        best_item = sm.match_product(feature_result=result,data_num=data_num)
        feature_group_json,product_json = fe.filter(item_tuple=best_item)
        print(product_json)
        gt = Genertion_Text()
        product_text = gt.generate_product_text(feature_froup_json=feature_group_json, product_json=product_json)
        print('-----------------------')
        print(product_text)


