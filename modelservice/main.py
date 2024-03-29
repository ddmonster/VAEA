import os
from modelservice.chart.analysis_chart import Dashboard_Chart
from modelservice.database.dataset import Dateset
from modelservice.common.config import Config
from modelservice.search_match_engineering.search_match import Search_Match
from modelservice.feature_engineering.feature_extraction import Feature_Engineering
from modelservice.product_text_generation_engineering.llm_generation_text import LLM_Genertion_Text
from modelservice.product_text_generation_engineering.rule_based_generation_text import Rule_Based_Generation_Text

'''
class Product_Introduce_NLG: 
    Product introduction generation class, under the four methods, one method to generate the product introduction, the other three methods to 
    generate the dashboard storytelling and dashboard

'''

class Product_Introduce_NLG(Config):
    def __init__(self,model=None):
        super().__init__()
        self.ds = Dateset()
        self.fe = Feature_Engineering(model=model)
        self.sm = Search_Match()
        self.gt = LLM_Genertion_Text(model=model)
        self.dc = Dashboard_Chart()
        self.rb = Rule_Based_Generation_Text()

    # product_introduction: The product introduces the main methods of natural language generation, including automatic dataset entry, text feature
    # extraction, product matching, paragraph generation and other functions.
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
                product_text = self.gt.generate_product_text(feature_group_json=feature_group_json, product_json=product_json)
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

    # product_dashboard_1: Generate a map of a brand's product origins and corresponding text descriptions.
    def product_dashboard_1(self,brand):
        result = self.dc.world_map_analysis(brand)
        if result is None:
            return None

        html_path,map_dic = result
        text = self.rb.world_map_text_generation(brand=brand,map_dic=map_dic)

        return {'html_path':html_path,'text':text}

    # product_dashboard_2: Generate a chart of selling prices between different brands, per star level. This is a 3D bar chart. A corresponding text
    # description is also generated.
    def product_dashboard_2(self):
        result = self.dc.bard3d_analysis()
        if result is None:
            return None

        html_path, y_scale_data, x_scale_data, z_data = result
        text = self.rb.bar3d_map_text_generation(y_scale_data=y_scale_data,x_scale_data=x_scale_data,z_data=z_data)

        return {'html_path': html_path, 'text': text}

    # product_dashboard_3: This is a time flow diagram. Showing and presenting the day's selling prices by day, the graph is automatically sliding.
    def product_dashboard_3(self):
        result = self.dc.flow_analysis()
        if result is None:
            return None

        html_path, date_list, brands_list, sale_price_total_dic, mrp_total_dic = self.dc.flow_analysis()
        text = self.rb.flow_chart_text_generation(date_list=date_list,brands_list=brands_list,sale_price_total_dic=sale_price_total_dic,mrp_total_dic=mrp_total_dic)
        return {'html_path': html_path, 'text': text}

    # main_run: Execution method. Inputs a sentence and returns the JSON result.
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

            dashboard_2 = self.product_dashboard_2()
            result_json['dashboard_2']=dashboard_2

            dashboard_3 = self.product_dashboard_3()
            result_json['dashboard_3'] = dashboard_3

        print('final result', result_json)
        return result_json




if __name__ == '__main__':
    sentence1 = "I'd like to buy a red PHILIPS fryer that has 3.2 litres and mades by plastic and the maximum energy consumption is two thousand wattage.I can use it to roast, broil and steam. In addition the product cannot be sold for more than 3000 rupee and the home kitchen rank is about 23000. Also, it should have the nonstick.Finally, it should be made in China and weight less than six kilograms."
    sentence2 = "I'd like to buy a fryer that has 3.2 litres and the maximum energy consumption is two thousand wattage.I can use it to roast, broil and steam. In addition the product cannot be sold for more than 3000 rupee and the home kitchen rank is about 23000. Also, it should have the nonstick.Finally, it should be made in China"
    sentence3 = "I want to buy a fryer"
    sentences = [sentence1]
    for sentence in sentences:
        pin=Product_Introduce_NLG()
        pin.main_run(sentence=sentence)
