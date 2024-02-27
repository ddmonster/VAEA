

'''
class Documentation_Planning:
    This class is the document planning class, which specifies to which paragraph the different categories of feature groups belong and which ones are to be introduced in this paragraph.
'''
class Documentation_Planning():
    def __init__(self):
        pass

    # paragraph_1: he first paragraph belongs to the category basic_info. This paragraph needs to describe basic product information. Note that this prompt will be used in the prompt project
    # to suggest what kind of content the model should generate based on the data. This can further improve accuracy. In addition, this paragraph defaults to an opening paragraph.
    def paragraph_1(self,is_opening=True,is_closing=False):
        if is_opening:
            return 'basic_info','This text is the beginning of the article and is used to present basic information about the product.'
        elif is_closing:
            return 'basic_info', 'This text is the ending of the article and is used to present basic information about the product.'

        else:
            return 'basic_info', 'This text is used to present basic information about the product.'

    # paragraph_2: The second paragraph falls under the category of POPULARITY and it focuses on the popularity of the product.
    def paragraph_2(self,is_opening=False,is_closing=False):
        if is_opening:
            return 'popularity','This text is the beginning of the article and is used to present the hotness of the product among the consumer base.'
        elif is_closing:
            return 'popularity', 'This text is the ending of the article and is used to present the hotness of the product among the consumer base.'
        else:
            return 'popularity', 'This text is used to present the hotness of the product among the consumer base.'

    # paragraph_3: The third paragraph focuses on price. It falls under the category of price.
    def paragraph_3(self,is_opening=False,is_closing=False):
        if is_opening:
            return 'price','This text is the beginning of the article and is used to present the price of the product.'
        elif is_closing:
            return 'price', 'This text is the ending of the article and is used to present the price of the product.'
        else:
            return 'price', 'This text is used to present the price of the product.'

    # paragraph_4: The fourth paragraph focuses on basic functions. It belongs to the category basic_functions.
    def paragraph_4(self,is_opening=False,is_closing=False):
        if is_opening:
            return 'basic_functions','This text is the beginning of the article and is used to present the basic functions of the product.'
        elif is_closing:
            return 'basic_functions', 'This text is the ending of the article and is used to present the basic functions of the product.'
        else:
            return 'basic_functions', 'This text is used to present the basic functions of the product.'

    # paragraph_5: The fifth paragraph focuses on advanced functions. It belongs to the category advanced_functions.
    def paragraph_5(self,is_opening=False,is_closing=False):

        if is_opening:
            return 'advanced_functions', 'This text is the beginning of the article and is used to present the advanced functions of the product.'
        elif is_closing:
            return 'advanced_functions', 'This text is the ending of the article and is used to present the advanced functions of the product.'
        else:
            return 'advanced_functions', 'This text is used to present the advanced functions of the product.'

    # paragraph_6: Paragraph 6 is mainly used for summarizing. It belongs to the category of summary.
    def paragraph_6(self,is_opening=False,is_closing=True):
        if is_opening:
            return 'summary', 'This text is the beginning of the article and is used to present the summary of the product.'
        elif is_closing:
            return 'summary', 'This text is the ending of the article and is used to summary of origin of the product.'
        else:
            return 'summary', 'This text is used to present the summary of the product.'

    # paragraph_7: The seventh paragraph is RULE-BASED generated without any cue words.
    def paragraph_7(self):
        return 'description'


'''
class Micro_Planning:
    This class defines which feature points should be included under each major class, and the system will make appropriate deletions to each class 
    as may be needed based on the available features available.
'''
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

    def summary(self):
        return ['country_of_origin','description']

    def description(self):
        return ['description']
