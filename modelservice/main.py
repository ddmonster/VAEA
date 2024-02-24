from modelservice.database.dataset import Dateset
from modelservice.search_match_engineering.search_match import Search_Match
from modelservice.feature_engineering.feature_extraction import Feature_Engineering
from modelservice.product_text_generation_engineering.generation_text import Genertion_Text


class Product_Introduce_NLG():
    def __init__(self):
        self.ds = Dateset()
        self.fe = Feature_Engineering()
        self.sm = Search_Match()
        self.gt = Genertion_Text()

    def product_introduction(self,sentence):

        data_num = self.ds.make_dataset()
        result = self.fe.extraction(sentence=sentence)
        # 要开发一个产品名精准匹配，如果匹配到了直接输出结果不用进入搜索匹配算法
        if (result is None) | (result == 'None'):
            feedback = f'Feature json is {result}. Cannot find any feature, please try again'
            print(feedback)
        else:

            best_item = self.sm.match_product(feature_result=result, data_num=data_num)
            feature_group_json, product_json = self.fe.filter(item_tuple=best_item)
            print(product_json)
            product_text = self.gt.generate_product_text(feature_froup_json=feature_group_json, product_json=product_json)
            print('-----------------------')
            print(product_text)

if __name__ == '__main__':
    sentence = "I'd like to buy a red PHILIPS fryer that has 3.2 litres and mades by plastic and the maximum energy consumption is two thousand wattage.I can use it to roast, broil and steam. In addition the product cannot be sold for more than 3000 rupee and the home kitchen rank is about 23000. Also, it should have the nonstick.Finally, it should be made in China and weight less than six kilograms."
    # sentence = "I'd like to buy a red PHILIPS fryer named PHILIPS Digital Air Fryer that has 3.2 litres and mades by plastic and the maximum energy consumption is two thousand wattage.I can use it to roast, broil and steam. In addition the product cannot be sold for more than 3000 rupee and the home kitchen rank is about 23000. Also, it should have the nonstick.Finally, it should be made in China and weight less than six kilograms."

    pin=Product_Introduce_NLG()
    pin.product_introduction(sentence=sentence)