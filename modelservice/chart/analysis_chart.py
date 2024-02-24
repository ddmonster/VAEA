import os.path

from pyecharts import options as opts
from pyecharts.charts import Map

from modelservice.common.config import Config
from modelservice.common.utils import Data_Base_Util

class Dashboard_Chart(Config):
    def __init__(self):
        super().__init__()
        self.da = Dashboard_Analysis()

    def world_map_analysis(self,brand):
        result = self.da.get_map_list(brand=brand)
        if result is None:
            return None
        map_list, map_dic =result

        html_path = os.path.join(self.chart_html_folder_path(),'map_world.html')
        MAX = sum([i for i in map_dic.values()])
        print(MAX)
        chart = (
            Map()
            .add(f"{brand} Fryers", map_list, "world",)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                title_opts=opts.TitleOpts(title=f"Map - {brand} Fryers Country of Origin"),
                visualmap_opts=opts.VisualMapOpts(max_=MAX),
            )
            .render(html_path)
        )
        return html_path,map_dic

    def bard3d_analysis(self):
        pass

class Dashboard_Analysis():
    def __init__(self):
        self.dbu = Data_Base_Util()

    def get_map_list(self,brand):
        kv = {'brand':brand}
        result = self.dbu.select_data_within_kv(db=self.dbu.db_path(),table_name=self.dbu.table_name(),kv =kv)
        if result is None:
            return None

        else:
            if len(result[1]) == 0:
                return None

            else:
                country_search_result = self.dbu.get_columnB_from_columnA(db=self.dbu.db_path(),table_name=self.dbu.table_name(),
                                                                          columnB_name='country_of_origin',columnA_name='brand',columnA_value=brand)

                if country_search_result is None or len(country_search_result[1]) == 0:
                    return None

                else:
                    country_dic = {}

                    for i,country_tuple in enumerate(country_search_result[1]):
                        country = country_tuple[0]
                        if country == 'Not Available':
                            continue
                        if country == 'USA':
                            country ='United States'

                        if country in country_dic.keys():
                            country_dic[country] += 1

                        else:
                            country_dic[country] = 1

                    if len(country_dic.keys()) == 0:
                        return None

                    else:
                        country_list = []
                        for country,num in country_dic.items():
                            country_num = [country,num]
                            country_list.append(country_num)
                        print(country_list)
                        print(country_dic)
                        return country_list,country_dic



if __name__ == '__main__':
    dc = Dashboard_Chart()
    dc.world_map_analysis(brand='PHILIPS')
    # da= Dashboard_Analysis()
    # da.get_map_list('PHILIPS')