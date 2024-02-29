from modelservice.model.model import LLM_Model
from modelservice.common.utils import Common_Utils

'''
class Feature_Engineering:
    This class encapsulates the methods for feature extraction
'''
class Feature_Engineering(LLM_Model):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.cu =Common_Utils()
        self.init_feature_group = {
            'basic_info': ['product_name', 'brand', 'Manufacturer', 'Model_Name'],
            'popularity': ['star_rating', 'home_kitchen_rank', 'air_fryers_rank', 'number_of_reviews'],
            'price': ['mrp', 'sale_price'],
            'basic_functions': ['colour', 'Material', 'capacity', 'wattage', 'Weight'],
            'advanced_functions':['Has_Nontick_Coating', 'Max_Temperature_Setting', 'Control_Method', 'Special_Feature','Recommended_Users_For_Product'],
            'summary': ['country_of_origin','description'],
            'description': [ 'description'],
            'others': ['asin', 'capacity_1', 'imported_by','technical_details']
        }

    # extraction: This method extracts the features and feature values in the statement by asking LLM and transforms the returned json string into a json object.
    def extraction(self,sentence):
        feature_string = self.ollama_extraction_feature(sentence=sentence)
        feature_json = self.cu.string_2_json(json_string=feature_string)
        print(feature_json)

        return feature_json

    # filter: After matching the best products, further screening of features is required before further text generation. This filtering removes product features
    # that are empty or not available as much as possible.
    def filter(self,item_tuple):
        product_json = self.cu.tuple_2_json(tuple_string=item_tuple)

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
