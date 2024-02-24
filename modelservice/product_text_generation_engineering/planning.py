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

    # def paragraph_6(self,is_opening=False,is_closing=True):
    #     if is_opening:
    #         return 'source', 'This text is the beginning of the article and is used to present the country of origin of the product.'
    #     elif is_closing:
    #         return 'source', 'This text is the ending of the article and is used to present the country of origin of the product.'
    #     else:
    #         return 'source', 'This text is used to present the country of origin of the product.'

    def paragraph_6(self,is_opening=False,is_closing=True):
        if is_opening:
            return 'summary', 'This text is the beginning of the article and is used to present the summary of the product.'
        elif is_closing:
            return 'summary', 'This text is the ending of the article and is used to summary of origin of the product.'
        else:
            return 'summary', 'This text is used to present the summary of the product.'

    def paragraph_7(self):
        return 'description'

# a=  ["HEALTHY FRYING: This appliance uses air crisp technology to cook healthy-low fat versions of your favorite foods,using little to no oil. Deliver a much healthier version of the same food with great crispy fried taste and texture", "EFFORTLESS COOKING: Prepare amazing meals from your cookbook such as french fries,chicken,steak,pudding and donuts.Make yourself feel like a professional chef in your kitchen with this air fryer that will replace any one of your kitchen appliances", "FAST & EFFICIENT HEATING: With 1000W of power, this air fryer heats up in 2-3 minutes and cooks food faster than a conventional oven so you can save money at the same time as cutting down the calories", "DIGITAL TEMPERATURE & TIME CONTROL: With digital touch control panel,simply insert food into the hot air fryer,set the time and temperature and cook your ingredients efficiently.Cook-up casseroles, beef, chicken breasts and even desserts", "SELECTIONS AT A TOUCH: Easy to use 8 Preset Menu that do all the cooking math for you. Just choose your preset with 1 easy tap on the display and you"re ready to cook. You can also set cooking temp/time as per your convenience."]

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

    # def source(self):
    #     return ['country_of_origin']
    def summary(self):
        return ['country_of_origin','description']

    def description(self):
        return ['description']
