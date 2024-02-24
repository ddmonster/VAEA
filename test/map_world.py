from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker
print([list(z) for z in zip(Faker.country, Faker.values())])
map_list = [['China', 62], ['Canada', 138], ['Brazil', 89], ['Russia', 31], ['United States', 44], ['Africa', 72], ['Germany', 138],['India',50]]
c = (
    Map()
    .add("商家A", map_list, "world",)
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Map-世界地图"),
        visualmap_opts=opts.VisualMapOpts(max_=200),
    )
    .render("../modelservice/chart/map_world.html")
)