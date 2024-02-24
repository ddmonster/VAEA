from modelservice.model.model import LLM_Model
from modelservice.common.utils import Common_Utils

class Feature_Engineering(LLM_Model):
    def __init__(self):
        super().__init__()
        self.cu =Common_Utils()
        self.init_feature_group = {
            'basic_info': ['product_name', 'brand', 'Manufacturer', 'Model_Name'],
            'popularity': ['star_rating', 'home_kitchen_rank', 'air_fryers_rank', 'number_of_reviews'],
            'price': ['mrp', 'sale_price'],
            'basic_functions': ['colour', 'Material', 'capacity', 'wattage', 'Weight'],
            'advanced_functions':['Has_Nontick_Coating', 'Max_Temperature_Setting', 'Control_Method', 'Special_Feature','Recommended_Users_For_Product'],
            'source': ['country_of_origin'],
            'description': [ 'description'],
            'others': ['asin', 'capacity_1', 'imported_by','technical_details']
        }

    def extraction(self,sentence):
        feature_string = self.ollama_extraction_feature(sentence=sentence)
        feature_json = self.cu.string_2_json(json_string=feature_string)
        print(feature_json)

        return feature_json

    def filter(self,item_tuple):
        product_json = self.cu.tuple_2_json(tuple_string=item_tuple)
        # bb = ["Multi Function : Broil , Roast , Bake , Grill , Fry", "Healthy Cooking : No Oil , No Fat , No Burn Flavor", "Perfect & Even Cooking", "Fast & Efficient Cooling.", "Save energy upto 60%"]
        for k,v in product_json.items():

            if (v == 'Not Available') | (v == 'NULL') | (v == 'not available'):
                for group_name, feature_list in self.init_feature_group.items():

                    if k in feature_list:
                        feature_list.remove(k)
                        self.init_feature_group[group_name] = feature_list
                    else:
                        continue
            else:
                continue

        for group_name, feature_list in self.init_feature_group.copy().items():
            if len(feature_list) == 0:
                del self.init_feature_group[group_name]

        del self.init_feature_group['others']
        print(self.init_feature_group)
        return self.init_feature_group,product_json



if __name__ == '__main__':
    from modelservice.database.dataset import Dateset

    sentence = "I'd like to buy a red PHILIPS fryer that has 3.2 litres and mades by plastic and the maximum energy consumption is two thousand wattage.I can use it to roast, broil and steam. In addition the product cannot be sold for more than 3000 rupee and the home kitchen rank is about 23000. Also, it should have the nonstick.Finally, it should be made in China and weight less than six kilograms."

    ds = Dateset()
    ds.make_dataset()

    fe = Feature_Engineering()
    result = fe.extraction(sentence=sentence)
