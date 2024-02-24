
import copy
from modelservice.common.utils import Rule_Bsed_Language_Util

# The rest of our suppliers come from United States, Canada and Australia.



class Rule_Based_Generation_Text(Rule_Bsed_Language_Util):
    def __init__(self):
        super().__init__()
        pass

    def world_map_text_generation(self,brand,map_dic):
        MAX = sum([i for i in map_dic.values()])
        sorted_dict_descending = dict(sorted(map_dic.items(), key=lambda item: item[1], reverse=True))
        print(sorted_dict_descending)
        max_key = max(map_dic, key=map_dic.get)
        print(max_key)
        text1 = (
            f"For {brand} Fryers, we {self.random_choose(['use', 'adopt'])} the global supply chain cooperation model to create a {self.random_choose(['solid', 'robust', 'strong'])}"
            f" {self.random_choose(['globalization', 'international'])} {self.random_choose(['cooperation', 'partnership'])}. ")

        text2 = f"{self.random_choose(['Among','Out of'])} our {MAX} {brand} {self.random_choose(['suppliers','vendors'])}, the {self.random_choose(['majority','predominance'])} of {brand} fryers are {self.random_choose(['manufactured','produced'])} in {max_key}, accounting for {int(map_dic[max_key]/MAX * 100)}% ({map_dic[max_key]}) of all {self.random_choose(['suppliers','merchants'])}. "
        text3 = ''
        text4 = ''

        if len(sorted(set(map_dic.values()), reverse=True)) >=2:
            second_max_value  = sorted(set(map_dic.values()), reverse=True)[1]
            second_max_keys = [key for key, value in map_dic.items() if value == second_max_value]
            print(second_max_keys)
            top_keys = second_max_keys + [max_key]
            rest_keys = [x for x in sorted_dict_descending.keys() if x not in top_keys]
            print(rest_keys)

            if len(second_max_keys)>0:
                text3 = f"The {self.random_choose(['next largest','following major'])} {self.random_choose(['supplier','vendor'])} {'are' if len(second_max_keys) > 1  else 'is'} {self.split_list_2_language(words_list=second_max_keys)} with {second_max_value}{' separately' if len(second_max_keys) > 1  else ''}, accounting for {int(second_max_value/MAX * len(second_max_keys) *100)}% of all suppliers. "

            if len(rest_keys) > 0:
                text4 = f"The rest of our {self.random_choose(['suppliers','vendors'])} come from {self.split_list_2_language(words_list=rest_keys)}."

        print(text1+text2+text3+text4)
        return text1+text2+text3+text4

    def bar3d_map_text_generation(self):
        pass

if __name__ == '__main__':
    rb = Rule_Based_Generation_Text()
    rb.world_map_text_generation(brand='PHILIPS',map_dic={'China': 4, 'India': 3,'United States':2,'United Kingdom':1})