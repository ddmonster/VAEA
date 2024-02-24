from langchain.output_parsers import ResponseSchema
from modelservice.product_text_generation_engineering.planning import Documentation_Planning
from modelservice.product_text_generation_engineering.planning import Micro_Planning
from modelservice.common.config import Config
from modelservice.model.model import LLM_Model
from modelservice.common.utils import Common_Utils


class Genertion_Text(LLM_Model):
    def __init__(self):
        super().__init__()
        self.dp = Documentation_Planning()
        self.mp = Micro_Planning()
        self.config = Config()
        self.cu = Common_Utils()
    def generate_product_text(self,feature_froup_json,product_json):
        order_list = self.get_order_from_product_json(feature_froup_json=feature_froup_json)
        product_total_text = ''
        product_name = self.cu.match_product_name(product_name=product_json['product_name'])
        for i,order in enumerate(order_list):
            try:
                if i == 0:
                    paragraph = f'self.dp.paragraph_{order}(is_opening=True,is_closing=False)'

                elif i == len(order_list)-1:
                    paragraph = f'self.dp.paragraph_{order}(is_opening=False,is_closing=True)'

                else:
                    paragraph = f'self.dp.paragraph_{order}(is_opening=False,is_closing=False)'

                group_name,group_intro = eval(paragraph)

                group_feature_contain = eval(f'self.mp.{group_name}()')
                # print(group_name,'----',group_intro,'----',group_feature_contain)
                group_feature_json = {}
                response_schemas = []
                for feature in group_feature_contain:
                    group_feature_json[feature]=product_json[feature]
                    schema = ResponseSchema(name=feature, description=self.config.prompt_info()[feature])
                    response_schemas.append(schema)


                paragraph_text_result = self.ollama_generation_one_paragraph(response_schemas=response_schemas,product_name=product_name,
                                                     paragraph_intro=group_intro,input_json=group_feature_json)

                paragraph_text_result = self.cu.match_text(text=paragraph_text_result)
                print(paragraph_text_result)
                product_total_text += paragraph_text_result
            except Exception as e:
                print(f'Exception occured {e}')
                continue
        try:
            paragraph_7 = eval(f'self.mp.{self.dp.paragraph_7()}()')
            paragraph_7_data = eval(product_json[paragraph_7[0]])

            product_total_text += f"Let's review this {product_name}:\n"
            for sentence in paragraph_7_data:
                sentence_new = f' -|->  {sentence}\n'
                print(sentence_new)
                product_total_text += sentence_new
        except Exception as e:
            pass

        if product_total_text == '':
            raise Exception('Product introduction is empty.')

        return product_total_text


    def get_order_from_product_json(self,feature_froup_json):
        json_keys= feature_froup_json.keys()
        order_list = []
        for i,v in enumerate(json_keys):

            for i in range(6):
                paragraph = f'self.dp.paragraph_{i + 1}()'
                group = eval(paragraph)
                if v == group[0]:
                    order_list.append(i+1)
                    break

        order_list = sorted(order_list)
        return order_list

if __name__ == '__main__':
    gt = Genertion_Text()
    aa = {'basic_info': ['product_name', 'brand', 'Manufacturer', 'Model_Name'], 'popularity': ['star_rating', 'home_kitchen_rank', 'air_fryers_rank', 'number_of_reviews'], 'price': ['mrp', 'sale_price'], 'basic_functions': ['colour', 'Material', 'capacity', 'wattage', 'Weight'], 'advanced_functions': ['Has_Nonstick_Coating', 'Control_Method', 'Special_Feature', 'Recommended_Uses_For_Product'], 'description': ['description']}
    # gt.get_order_from_product_json(product_json=aa)

    bb = {'id': 'B08B3M4GMX', 'date': '3/1/2023', 'urls': 'https://www.amazon.in/Philips-HD9216-43-Fryer-Retractable/dp/B08B3M4GMX', 'product_name': 'PHILIPS Air Fryer - India’s No.1 Air Fryer Brand, With Rapid Air Technology, Uses up to 90% less fat, 1425W, 4.1 Liter, (Grey) (HD9216/43)', 'brand': 'PHILIPS', 'star_rating': '4.3', 'number_of_reviews': '335', 'mrp': '10495', 'sale_price': '6680', 'colour': 'Grey', 'capacity': '2 litres', 'wattage': '1400.0', 'country_of_origin': 'Not Available', 'home_kitchen_rank': '10548', 'air_fryers_rank': '16', 'technical_details': '{"Special Feature": "Manual", "Product Dimensions": "28.7D x 31.5W x 38.4H Centimeters", "Colour": "Grey", "Capacity": "2 litres", "Material": "Plastic", "Recommended Uses For Product": "Roast, Bake", "Item Weight": "8.56 Kilograms", "Brand": "PHILIPS", "Wattage": "1400 Watts", "Voltage": "220 Volts", "Control Method": "App", "Model Name": "HD9216/43", "Has Nonstick Coating": "Yes", "Min Temperature Setting": "40 Degrees Fahrenheit", "Manufacturer": "Philips", "Item model number": "HD9216/43", "ASIN": "B08B3M4GMX"}', 'description': '["Philips is India’s No.1 Airfryer brand (Source: Euromonitor International Limited; Consumer Appliances 2021ED)", "PHILIPS Air Fryer HD9216/43 uses up to 80% less fat, Air Fry, Roast, Bake, Grill, Reheat, 1400W, with dishwasher safe 4.1 Liter basket, Patented Rapid Air Technology, Starfish design, 360 °even frying, Black", "GUILT-FREE FOOD WITH 90% LESS OIL: With PATENTED RAPID AIR TECHNOLOGY Philips Air Fryer delivers all the crunch and tenderness of deep-frying with 90% less oil.", "TECHNOLOGY: Patented Rapid Air technology with unique starfish design pan ensures evenly fried results without flipping the food.; SMART ALL-IN-1 FUNCTIONALITY: Fry. Bake. Grill. Roast. And even reheat!", "EASE OF USE: Extra-long 1.8 m cord length for easy placement in your kitchen. 30 minutes timer with auto off. Wide temperature control from 80°C to 200 °C.", "NUTRIU APP: Get 200+ Indian and global recipes and some from celebrity Chef Ranveer Brar by downloading free NutriU App (IOS & Android).", "RECIPES MADE EASY: Make paneer or chicken tikka, pizza, grilled vegetables, Samosas, Kabab/Cutlet, Chicken Nuggets, Cakes/muffins and much more at touch of a button."]', 'asin': 'B08B3M4GMX', 'capacity_1': '2.0', 'Weight': '8.56 Kilograms', 'Has_Nonstick_Coating': 'Yes', 'Material': 'Plastic', 'Manufacturer': 'Philips', 'Control_Method': 'App', 'Model_Name': 'HD9216/43', 'Recommended_Uses_For_Product': 'Roast, Bake', 'Special_Feature': 'Manual', 'Max_Temperature_Setting': 'not available', 'Imported_By': 'not available'}
    # print(bb.keys())
    #          'Recommended_Users_For_Product'
    gt.generate_product_text(feature_froup_json = aa,product_json=bb)