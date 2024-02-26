import numpy as np

from modelservice.common.utils import Rule_Bsed_Language_Util




class Rule_Based_Generation_Text(Rule_Bsed_Language_Util):
    def __init__(self):
        super().__init__()
        pass

    def world_map_text_generation(self,brand,map_dic):
        MAX = sum([i for i in map_dic.values()])
        sorted_dict_descending = dict(sorted(map_dic.items(), key=lambda item: item[1], reverse=True))
        max_key = max(map_dic, key=map_dic.get)
        text1 = (
            f"For {brand} Fryers, we {self.random_choose(['use', 'adopt'])} the global supply chain cooperation model to create a {self.random_choose(['solid', 'robust', 'strong'])}"
            f" {self.random_choose(['globalization', 'international'])} {self.random_choose(['cooperation', 'partnership'])}. ")

        text2 = f"{self.random_choose(['Among','Out of'])} our {MAX} {brand} {self.random_choose(['suppliers','vendors'])}, the {self.random_choose(['majority','predominance'])} of {brand} fryers are {self.random_choose(['manufactured','produced'])} in {max_key}, accounting for {int(map_dic[max_key]/MAX * 100)}% ({map_dic[max_key]}) of all {self.random_choose(['suppliers','merchants'])}. "
        text3 = ''
        text4 = ''

        if len(sorted(set(map_dic.values()), reverse=True)) >=2:
            second_max_value  = sorted(set(map_dic.values()), reverse=True)[1]
            second_max_keys = [key for key, value in map_dic.items() if value == second_max_value]
            top_keys = second_max_keys + [max_key]
            rest_keys = [x for x in sorted_dict_descending.keys() if x not in top_keys]

            if len(second_max_keys)>0:
                text3 = f"The {self.random_choose(['next largest','following major'])} {self.random_choose(['supplier','vendor'])} {'are' if len(second_max_keys) > 1  else 'is'} {self.split_list_2_language(words_list=second_max_keys)} with {second_max_value}{' separately' if len(second_max_keys) > 1  else ''}, accounting for {int(second_max_value/MAX * len(second_max_keys) *100)}% of all suppliers. "
            if len(rest_keys) > 0:
                text4 = f"The rest of our {self.random_choose(['suppliers','vendors'])} come from {self.split_list_2_language(words_list=rest_keys)}."

        print(text1+text2+text3+text4)
        return text1+text2+text3+text4

    def bar3d_map_text_generation(self,y_scale_data,x_scale_data,z_data):
        x_scale = np.asarray([float(i) for i in x_scale_data])
        z_data = np.asarray(z_data)

        text = f"We have {self.random_choose(['shortlisted','picked'])} {len(y_scale_data)} top Fryer brands on Amazon India which {'are' if len(y_scale_data) > 1  else 'is'} {self.split_list_2_language(words_list=y_scale_data)}{self.random_choose([' separately',' respectively']) if len(y_scale_data) > 1  else ''}. "

        for i,brand in enumerate(y_scale_data):
            indices_1 = np.where(z_data[:, 1] == y_scale_data.index(brand))[0]
            price_list = z_data[indices_1, 2]
            price_list = price_list[price_list != 0]
            avg_price = int(np.mean(price_list))
            max_price = int(max(price_list))
            min_price = int(min(price_list))

            indices_2 = np.where((z_data[:, 2] != 0) & (z_data[:, 1] == i))[0]
            rating_list = z_data[indices_2, 0]
            mode_result = round(np.median(rating_list) / 10, 1)
            if i == 0:
                text_i=f"{self.random_choose(['First and foremost','Chiefly'])}, the most {self.random_choose(['admired','fashionable'])} is the {brand} fryer, with a star rating of {mode_result} for most of their fryers, which is clearly {self.random_choose(['well-received','appreciated'])} by users. {brand} fryers are sold at an average price of {avg_price}₹. "

            elif i==len(y_scale_data)-1:
                indices_first = np.where(z_data[:, 1] == y_scale_data.index(y_scale_data[0]))[0]
                price_list_first = z_data[indices_first, 2]
                price_list_first = price_list_first[price_list_first != 0]
                avg_price_first = int(np.mean(price_list_first))
                percent = int(avg_price/avg_price_first * 100)
                text_i = f"The {self.random_choose(['last','ultimate'])} and {self.random_choose(['relatively','comparatively'])} popular brand is {brand}. Their fryers, despite having a star rating of only {mode_result} on average, are {self.random_choose(['the least expensive of these brands','the most budget-friendly among these brands'])}, averaging only {avg_price}₹, which is {percent}% of the average price of the first place! This means that if you are on a budget, then {brand}'s fryers are your first choice for value for money. "

            else:
                max_price_rating_index = np.where((z_data[:, 1] == y_scale_data.index(brand)) & (z_data[:, 2] == max_price))[0]
                min_price_rating_index = np.where((z_data[:, 1] == y_scale_data.index(brand)) & (z_data[:, 2] == min_price))[0]
                max_price_rating = z_data[max_price_rating_index,0][0]
                min_price_rating = z_data[min_price_rating_index, 0][0]
                text_i = f"{self.random_choose(['Thereafter','Next','Then','Subsequently'])}, it's {brand}. their {self.random_choose(['highest priced','premium-priced','top-priced'])} fryers sell for {max_price}₹ with an average rating of {max_price_rating}, while the {self.random_choose(['most affordable','least expensive','most pocket-friendly'])} ones have a rating of {min_price_rating}. and sell for only {min_price}₹. "
            text += text_i

        print(text)
        return text

if __name__ == '__main__':
    rb = Rule_Based_Generation_Text()
    from modelservice.chart.analysis_chart import Dashboard_Chart
    dc = Dashboard_Chart()
    html_path,y_scale_data,x_scale_data,z_data = dc.bard3d_analysis()
    rb.bar3d_map_text_generation(x_scale_data=x_scale_data,y_scale_data=y_scale_data,z_data=z_data)

    # rb.world_map_text_generation(brand='PHILIPS',map_dic={'China': 4, 'India': 3,'United States':2,'United Kingdom':1})
