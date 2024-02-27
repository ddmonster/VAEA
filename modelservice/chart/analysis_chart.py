import os.path
import numpy as np
import copy
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.charts import Bar3D
from pyecharts.charts import Timeline, Bar, Pie

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


    def flow_analysis(self):
        brands_list = self.da.get_flow_x_scale()
        date_list = self.da.get_flow_date(brands_list=brands_list)
        result = self.da.get_flow_sale_price_mrp(brands_list=brands_list,date_list=date_list)
        if result is None:
            return None

        else:
            sale_price_total_dic,mrp_total_dic = result
            timeline = Timeline()
            for date in date_list:
                timeline.add(self.get_date_overlap_chart(date=date,brands_list=brands_list,sale_price_total_dic=sale_price_total_dic,mrp_total_dic=mrp_total_dic), time_point=str(date))

            html_path = os.path.join(self.chart_html_folder_path(), 'flow_date.html')
            timeline.add_schema(is_auto_play=True, play_interval=1800)
            timeline.render(html_path)

            return html_path,date_list,brands_list,sale_price_total_dic,mrp_total_dic

    def get_date_overlap_chart(self,date,brands_list,sale_price_total_dic,mrp_total_dic) -> Bar:
        bar = (
            Bar()
            .add_xaxis(xaxis_data=brands_list)
            .add_yaxis(
                series_name="Sale Price",
                y_axis=sale_price_total_dic[date],
                label_opts=opts.LabelOpts(is_show=True),
            )
            .add_yaxis(
                series_name="MRP",
                y_axis=mrp_total_dic[date],
                label_opts=opts.LabelOpts(is_show=True),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="{} - Fryers Price Indicator".format(date), subtitle="Data from Amazon India"
                ),
                tooltip_opts=opts.TooltipOpts(
                    is_show=True, trigger="axis", axis_pointer_type="shadow"
                ),
                legend_opts=opts.LegendOpts(
                    selected_map={
                        "Sale Price": True,
                        "Suggested Retail Price": True,
                    }
                ),
            )
        )
        pie = (
            Pie()
            .add(
                series_name="MRP vs Sale Price",
                data_pair=[
                    ["Sale Price", sale_price_total_dic["{}sum".format(date)]],
                    ["MRP", mrp_total_dic["{}sum".format(date)]],

                ],
                center=["80%", "27%"],
                radius="28%",
            )
            .set_series_opts(tooltip_opts=opts.TooltipOpts(is_show=True, trigger="item"))
        )
        return bar.overlap(pie)


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
                    y_scale_data = list(brands_dict_descending.keys())[:rank_num]

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
            for i,v_x in enumerate(x_scale):
                for j,v_y in enumerate(y_scale):

                    kv = {'brand':v_y,'star_rating':v_x}

                    result = self.dbu.select_column_data_within_kv(db = self.dbu.db_path(),table_name=self.dbu.table_name(),column_name='sale_price',kv=kv)
                    if (result is None) | (len(result[1]) == 0):
                        z_data.append([i, j, 0])
                    else:
                        mean_price = int(np.mean([int(x[0]) for x in result[1]]))
                        z_data.append([i, j, mean_price])

            return z_data

    def get_flow_x_scale(self,rank_num=10):
        result = self.dbu.select_data_within_column(db=self.dbu.db_path(), table_name=self.dbu.table_name(),
                                                    column_name='brand')
        if result is None:
            return None
        else:
            brands = result[1]
            if len(brands) == 0:
                return None

            else:
                brands = [x[0] for x in brands]
                brands_set = set(brands)
                brands_dict = {}

                for brand in brands_set:
                    num = brands.count(brand)
                    brands_dict[brand] = num

                brands_dict_descending = dict(sorted(brands_dict.items(), key=lambda item: item[1], reverse=True))

                if len(brands_dict_descending) >= rank_num:
                    x_scale_data = list(brands_dict_descending.keys())[:rank_num]

                else:
                    x_scale_data = list(brands_dict_descending.keys())

                return x_scale_data

    def get_flow_date(self,brands_list):

        dates_list = []

        for brand in brands_list:
            result = self.dbu.get_columnB_from_columnA(db=self.dbu.db_path(), table_name=self.dbu.table_name(),
                                                       columnB_name='date',columnA_name='brand',columnA_value=brand)

            if result is None:
                continue

            else:
                dates = result[1]
                if len(dates) == 0:
                    continue

                else:
                    dates = [x[0] for x in dates]
                    dates_list += dates

        dates_list = list(set(dates_list))
        if len(dates_list) == 0:
            return None
        dates_list = self.sort_date(date_list=dates_list)
        return dates_list

    def get_flow_sale_price_mrp(self,brands_list,date_list):
        sale_price_total_dic ={}
        mrp_total_dic = {}
        if (brands_list is None) or (date_list is None):
            return None
        for date in date_list:
            sale_price_date_list = []
            mrp_date_list = []
            sale_price_list = []
            mrp_list = []

            for brand in brands_list:
                kv = {'brand':brand,'date':date}
                sale_prices_result = self.dbu.select_column_data_within_kv(db=self.dbu.db_path(), table_name=self.dbu.table_name(),
                                                               kv=kv,column_name='sale_price')

                mrps_result = self.dbu.select_column_data_within_kv(db=self.dbu.db_path(),
                                                                           table_name=self.dbu.table_name(),
                                                                           kv=kv, column_name='mrp')
                if (sale_prices_result is None) | (mrps_result is None):
                    continue

                else:
                    sale_prices = sale_prices_result[1]
                    mrps = mrps_result[1]
                    new_sale_prices = []
                    new_mrps = []
                    if (len(sale_prices) == 0) | (len(mrps) == 0):
                        new_sale_prices.append(0)
                        new_mrps.append(0)
                        mrp_mean = 0
                        sale_prices_mean = 0

                    else:

                        for i,price in enumerate(sale_prices.copy()):
                            if (price[0] == 'Not Available')|(mrps[i][0] == 'Not Available'):
                                new_sale_prices.append(0)
                                new_mrps.append(0)

                            else:
                                new_sale_prices.append(int(price[0]))
                                new_mrps.append(int(mrps[i][0]))

                        if len(new_sale_prices) ==0:
                            sale_prices_mean = 0

                        else:
                            no_zero_new_sale_prices = [x for x in new_sale_prices if x != 0]
                            sale_prices_mean = int(np.mean(no_zero_new_sale_prices))

                        if len(new_mrps) ==0:
                            mrp_mean = 0

                        else:
                            no_zero_new_mrps = [x for x in new_mrps if x != 0]
                            mrp_mean = int(np.mean(no_zero_new_mrps))

                    mrp_date_dic = {'name': brand,'value':mrp_mean}
                    sale_price_date_dic = {'name': brand, 'value': sale_prices_mean}
                    sale_price_date_list.append(sale_price_date_dic)
                    mrp_date_list.append(mrp_date_dic)
                    sale_price_list.append(sale_prices_mean)
                    mrp_list.append(mrp_mean)

            sale_price_total_dic[date] = sale_price_date_list
            sale_price_total_dic[f'{date}sum'] = sum(sale_price_list)
            mrp_total_dic[date] = mrp_date_list
            mrp_total_dic[f'{date}sum'] = sum(mrp_list)

        return sale_price_total_dic,mrp_total_dic

    def sort_date(self,date_list):
        from datetime import datetime
        date_objects = [datetime.strptime(date_str, '%m/%d/%Y') for date_str in date_list]
        sorted_dates = sorted(date_objects)
        sorted_dates = [x.strftime('%#m/%#d/%Y') for x in sorted_dates]
        return sorted_dates






if __name__ == '__main__':
    from modelservice.product_text_generation_engineering.rule_based_generation_text import Rule_Based_Generation_Text
    dc = Dashboard_Chart()
    rb = Rule_Based_Generation_Text()
    html_path,date_list,brands_list,sale_price_total_dic,mrp_total_dic = dc.flow_analysis()
    rb.flow_chart_text_generation(date_list=date_list,brands_list=brands_list,sale_price_total_dic=sale_price_total_dic,mrp_total_dic=mrp_total_dic)



    # dc.bard3d_analysis()
    # dc.world_map_analysis(brand='PHILIPS')
    # da= Dashboard_Analysis()
    # da.get_flow_x_scale()
    # brands_list = da.get_flow_x_scale()
    # date_list = da.get_flow_date(brands_list=brands_list)
    # da.get_flow_sale_price_mrp(brands_list=brands_list,date_list=date_list)
    # da.get_map_list('PHILIPS')
    # da.get_bard3d_y_scale()
    # x_scale = da.get_bard3d_x_scale()
    # y_scale = da.get_bard3d_y_scale()
    # z_data = da.get_bard3d_z_data(x_scale=x_scale,y_scale=y_scale)

