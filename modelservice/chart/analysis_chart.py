import os.path
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.charts import Bar3D

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
        y_scale_data = self.da.get_bard3d_y_scale()
        x_scale_data = self.da.get_bard3d_x_scale()
        z_data = self.da.get_bard3d_z_data(x_scale=x_scale_data,y_scale=y_scale_data)
        if (x_scale_data is None) | (y_scale_data is None) | (z_data is None):
            return None
        z_max = max([x[2] for x in z_data])
        html_path = os.path.join(self.chart_html_folder_path(), 'bard3d.html')
        chart = (
            Bar3D()
            .add(
                series_name="",
                data=z_data,
                xaxis3d_opts=opts.Axis3DOpts(type_="category", data=x_scale_data, name='Star Rating'),
                yaxis3d_opts=opts.Axis3DOpts(type_="category", data=y_scale_data, name='Brand'),
                zaxis3d_opts=opts.Axis3DOpts(type_="value", name='Avg Sale Price (₹)'),
                shading='realistic'
            )
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(
                    max_= z_max,
                    range_color=[
                        "#313695",
                        "#4575b4",
                        "#74add1",
                        "#abd9e9",
                        "#e0f3f8",
                        "#ffffbf",
                        "#fee090",
                        "#fdae61",
                        "#f46d43",
                        "#d73027",
                        "#a50026",
                    ],
                )
            )
            .render(html_path)
        )
        return html_path,y_scale_data,x_scale_data,z_data

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

                        return country_list,country_dic

    def get_bard3d_y_scale(self,rank_num=7):
        result = self.dbu.select_data_within_column(db= self.dbu.db_path(),table_name=self.dbu.table_name(),column_name='brand')
        if result is None:
            return None
        else:
            brands = result[1]
            if len(brands) == 0:
                return None
            else:
                brands = [x[0] for x in brands ]

                brands_set = set(brands)

                brands_dict = {}
                for brand in brands_set:
                    num = brands.count(brand)
                    brands_dict[brand]= num

                brands_dict_descending = dict(sorted(brands_dict.items(), key=lambda item: item[1], reverse=True))

                if len(brands_dict_descending) >= rank_num:
                    y_scale_data = list(brands_dict_descending.keys())[:7]

                else:
                    y_scale_data = list(brands_dict_descending.keys())

                return y_scale_data

    def get_bard3d_x_scale(self):
        result = self.dbu.select_data_within_column(db=self.dbu.db_path(), table_name=self.dbu.table_name(),
                                                    column_name='star_rating')
        if result is None:
            return None
        else:
            ratings = result[1]
            if len(ratings) == 0:
                return None
            else:

                filter_ratings = []
                for x in ratings:
                    if 'No' not in x[0]:
                        filter_ratings.append(float(x[0]))
                if len(filter_ratings) == 0:
                    return None

                else:
                    small_scale = 0.1
                    max_rating = max(filter_ratings)
                    x_range= np.arange(0,max_rating+small_scale,small_scale)
                    x_range = np.round(x_range,1)
                    x_scale = [str(x) for x in x_range]
                    x_scale = [str(int(float(value))) if '.0' in value else value for value in x_scale]
                    return x_scale

    def get_bard3d_z_data(self,x_scale,y_scale):
        z_data = []
        if (x_scale is None) | (y_scale is None):
            return None

        else:
            print('x_scale',x_scale)
            print('y_scale',y_scale)
            for i,v_x in enumerate(x_scale):
                for j,v_y in enumerate(y_scale):
                    # z_data.append([i,j])
                    kv = {'brand':v_y,'star_rating':v_x}

                    result = self.dbu.select_column_data_within_kv(db = self.dbu.db_path(),table_name=self.dbu.table_name(),column_name='sale_price',kv=kv)
                    if (result is None) | (len(result[1]) == 0):
                        z_data.append([i, j, 0])
                    else:
                        mean_price = int(np.mean([int(x[0]) for x in result[1]]))
                        z_data.append([i, j, mean_price])

            print(z_data)
            return z_data






if __name__ == '__main__':
    dc = Dashboard_Chart()
    dc.bard3d_analysis()
    # dc.world_map_analysis(brand='PHILIPS')
    # da= Dashboard_Analysis()
    # da.get_map_list('PHILIPS')
    # da.get_bard3d_y_scale()
    # x_scale = da.get_bard3d_x_scale()
    # y_scale = da.get_bard3d_y_scale()
    # z_data = da.get_bard3d_z_data(x_scale=x_scale,y_scale=y_scale)

