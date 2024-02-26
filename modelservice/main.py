import os
from modelservice.chart.analysis_chart import Dashboard_Chart
from modelservice.database.dataset import Dateset
from modelservice.common.config import Config
from modelservice.search_match_engineering.search_match import Search_Match
from modelservice.feature_engineering.feature_extraction import Feature_Engineering
from modelservice.product_text_generation_engineering.llm_generation_text import Genertion_Text
from modelservice.product_text_generation_engineering.rule_based_generation_text import Rule_Based_Generation_Text

class Product_Introduce_NLG(Config):
    def __init__(self):
        super().__init__()
        self.ds = Dateset()
        self.fe = Feature_Engineering()
        self.sm = Search_Match()
        self.gt = Genertion_Text()
        self.dc = Dashboard_Chart()
        self.rb = Rule_Based_Generation_Text()

    def product_introduction(self,sentence):

        data_num = self.ds.make_dataset()
        result = self.fe.extraction(sentence=sentence)

        if (result is None) | (result == 'None'):
            feedback = f'Sorry,Feature json is {result}. Cannot find any feature, please try again.'
            print(feedback)

            return {'product_introduction':feedback,'image_path':None,'data':None}

        else:
            try:
                best_item = self.sm.match_product(feature_result=result, data_num=data_num)
                feature_group_json, product_json = self.fe.filter(item_tuple=best_item)
                print(product_json)
                product_text = self.gt.generate_product_text(feature_froup_json=feature_group_json, product_json=product_json)
                print('-----------------------')
                print(product_text)

            except Exception as e:
                feedback = f'Sorry, cannot find any feature, please try again.'
                print(feedback)
                print(e)

                return {'product_introduction':feedback,'image_path':None,'data':None}

            else:
                image_path = os.path.join(self.image_folder_path(),product_json['id']+'.jpg')
                if not os.path.exists(image_path):
                    image_path = None

                return {'product_introduction': product_text,'image_path':image_path,'data':product_json}

    def product_dashboard_1(self,brand):
        result = self.dc.world_map_analysis(brand)
        if result is None:
            return None

        html_path,map_dic = result
        text = self.rb.world_map_text_generation(brand=brand,map_dic=map_dic)

        return {'html_path':html_path,'text':text}

    def product_dashboard_2(self):
        pass

    def main_run(self,sentence):
        result_json = self.product_introduction(sentence=sentence)
        if result_json['data'] is None:
            result_json['dashboard_1']=None
            result_json['dashboard_2']=None
            result_json['dashboard_3']=None

        else:
            brand = result_json['data']['brand']
            if brand == 'Not Available':
                result_json['dashboard_1'] = None
            else:
                dashboard_1 = self.product_dashboard_1(brand=brand)
                result_json['dashboard_1']=dashboard_1

        print('final result', result_json)




if __name__ == '__main__':
    sentence1 = "I'd like to buy a red PHILIPS fryer that has 3.2 litres and mades by plastic and the maximum energy consumption is two thousand wattage.I can use it to roast, broil and steam. In addition the product cannot be sold for more than 3000 rupee and the home kitchen rank is about 23000. Also, it should have the nonstick.Finally, it should be made in China and weight less than six kilograms."
    sentence2 = "I'd like to buy a fryer that has 3.2 litres and the maximum energy consumption is two thousand wattage.I can use it to roast, broil and steam. In addition the product cannot be sold for more than 3000 rupee and the home kitchen rank is about 23000. Also, it should have the nonstick.Finally, it should be made in China"
    sentences = [sentence1]
    for sentence in sentences:
        pin=Product_Introduce_NLG()
        pin.main_run(sentence=sentence)
    # print(113333)
    # pin.product_introduction(sentence=sentence)