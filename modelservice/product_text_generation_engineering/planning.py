#规划种类优先级（段落顺序）


class Documentation_Planning():
    def __init__(self):
        pass

    def paragraph_1(self,is_opening=True,is_closing=False):
        if is_opening:
            return 'basic_info','This text is the beginning of the article and is used to present basic information about the product.'
        elif is_closing:
            return 'basic_info', 'This text is the ending of the article and is used to present basic information about the product.'

        else:
            return 'basic_info', 'This text is used to present basic information about the product.'
    def paragraph_2(self,is_opening=False,is_closing=False):
        if is_opening:
            return 'popularity','This text is the beginning of the article and is used to present the hotness of the product among the consumer base.'
        elif is_closing:
            return 'popularity', 'This text is the ending of the article and is used to present the hotness of the product among the consumer base.'
        else:
            return 'popularity', 'This text is used to present the hotness of the product among the consumer base.'

    def paragraph_3(self,is_opening=False,is_closing=False):
        if is_opening:
            return 'price','This text is the beginning of the article and is used to present the price of the product.'
        elif is_closing:
            return 'price', 'This text is the ending of the article and is used to present the price of the product.'
        else:
            return 'price', 'This text is used to present the price of the product.'


    def paragraph_4(self,is_opening=False,is_closing=False):
        if is_opening:
            return 'basic_functions','This text is the beginning of the article and is used to present the basic functions of the product.'
        elif is_closing:
            return 'basic_functions', 'This text is the ending of the article and is used to present the basic functions of the product.'
        else:
            return 'basic_functions', 'This text is used to present the basic functions of the product.'

    def paragraph_5(self,is_opening=False,is_closing=False):

        if is_opening:
            return 'advanced_functions', 'This text is the beginning of the article and is used to present the advanced functions of the product.'
        elif is_closing:
            return 'advanced_functions', 'This text is the ending of the article and is used to present the advanced functions of the product.'
        else:
            return 'advanced_functions', 'This text is used to present the advanced functions of the product.'

    def paragraph_6(self,is_opening=False,is_closing=True):
        if is_opening:
            return 'source', 'This text is the beginning of the article and is used to present the country of origin of the product.'
        elif is_closing:
            return 'source', 'This text is the ending of the article and is used to present the country of origin of the product.'
        else:
            return 'source', 'This text is used to present the country of origin of the product.'

    def paragraph_7(self):
        return 'description'


#规划种类内部的优先级（句子优先级）
class Micro_Planning():
    def __init__(self):
        pass

    def basic_info(self):

        return ['product_name', 'brand', 'Manufacturer', 'Model_Name']

    def price(self):
        return ['mrp', 'sale_price']

    def popularity(self):
        return ['star_rating', 'home_kitchen_rank', 'air_fryers_rank', 'number_of_reviews']

    def basic_functions(self):
        return ['colour', 'Material', 'capacity', 'wattage', 'Weight']

    def advanced_functions(self):
        return ['Has_Nonstick_Coating', 'Max_Temperature_Setting', 'Control_Method', 'Special_Feature','Recommended_Uses_For_Product']

    def source(self):
        return ['country_of_origin']

    def description(self):
        return ['description']
