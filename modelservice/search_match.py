from utils import Data_Base_Util
from fuzzywuzzy import process

class Search_Match():
    def __init__(self):
        self.dbu=Data_Base_Util()

    def get_all_product_name(self):
        [is_success, return_value] = self.dbu.select_data_within_column(db=self.dbu.db_path(), table_name=self.dbu.table_name(),
                                                                   column_name='product_name')
        if is_success:
            return return_value
        else:

            raise Exception('Search all product name error')

    def match_product_name(self,product_name):
        all_product_name = self.get_all_product_name()
        best_match, score = process.extractOne(product_name, all_product_name)

        # 输出最匹配的字符串和匹配分数
        print("Best Match:", best_match)
        print("Score:", score)
        return best_match

    def match_product_type(self,product_type):
        all_product_name = self.get_all_product_name()
        best_match = process.extract(product_type, all_product_name,limit=999)

        # 输出最匹配的字符串和匹配分数
        print("Best Match:", best_match)
        print("Best Match Length:", len(best_match))
        return best_match

if __name__ == '__main__':
    sm=Search_Match()
    sm.match_product_type('air fryer')
