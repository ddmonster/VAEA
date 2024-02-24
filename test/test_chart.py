from pyecharts.charts import Bar
from pyecharts import options as opts
# 内置主题类型可查看 pyecharts.globals.ThemeType
from pyecharts.globals import ThemeType
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
#
# | BUILTIN_THEMES = ['light', 'dark', 'white']
# |
# | CHALK = 'chalk'
# |
# | DARK = 'dark'
# |
# | ESSOS = 'essos'
# |
# | INFOGRAPHIC = 'infographic'
# |
# | LIGHT = 'light'
# |
# | MACARONS = 'macarons'
# |
# | PURPLE_PASSION = 'purple-passion'
# |
# | ROMA = 'roma'
# |
# | ROMANTIC = 'romantic'
# |
# | SHINE = 'shine'
# |
# | VINTAGE = 'vintage'
# |
# | WALDEN = 'walden'
# |
# | WESTEROS = 'westeros'
# |
# | WHITE = 'white'
# |
# | WONDERLAND = 'wonderland'

#基础
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION)) #WESTEROS
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
    .set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))
    # 或者直接使用字典参数
    # .set_global_opts(title_opts={"text": "主标题", "subtext": "副标题"})
)
bar.render(r'modelservice\chart\index.html')


#多加一个数列
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION))
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
    .add_yaxis("商家B", [15, 25, 30, 18, 65, 70])
    .set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))
)

bar.render('modelservice\chart\index1.html')

#实现堆叠
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION))
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90], stack="stack1")
    .add_yaxis("商家B", [15, 25, 30, 18, 65, 70], stack="stack1")
    .set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))
)
bar.render('modelservice\chart\index2.html')


#部分堆叠
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION))
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90], stack="stack1")
    .add_yaxis("商家B", [15, 25, 30, 18, 65, 70], stack="stack1")
    .add_yaxis("商家C", [25, 15, 50, 38, 25, 20])
    .set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))
)
bar.render('modelservice\chart\index3.html')


#修改标题栏
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION))
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90], stack="stack1")
    .add_yaxis("商家B", [15, 25, 30, 18, 65, 70], stack="stack1")
    .add_yaxis("商家C", [25, 15, 50, 38, 25, 20])
    .set_global_opts(title_opts=opts.TitleOpts(title="我的柱状图", subtitle="hello bar", pos_left=100))
)
bar.render('modelservice\chart\index4.html')


#修改坐标轴刻度旋转
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION))
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90], stack="stack1")
    .add_yaxis("商家B", [15, 25, 30, 18, 65, 70], stack="stack1")
    .add_yaxis("商家C", [25, 15, 50, 38, 25, 20])
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
        title_opts=opts.TitleOpts(title="我的柱状图", subtitle="hello bar", pos_left=100)
    )
)
bar.render('modelservice\chart\index5.html')


# 设置是否显示数值
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90], stack="stack1")
    .add_yaxis("商家B", [15, 25, 30, 18, 65, 70], stack="stack1")
    .add_yaxis("商家C", [25, 15, 50, 38, 25, 20])
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside"))
    .set_global_opts(
        # xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
        title_opts=opts.TitleOpts(title="我的柱状图", subtitle="hello bar", pos_left=100)
    )
)
bar.render('modelservice\chart\index6.html')


#增加区域选择组件
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90], stack="stack1")
    .add_yaxis("商家B", [15, 25, 30, 18, 65, 70], stack="stack1")
    .add_yaxis("商家C", [25, 15, 50, 38, 25, 20])
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside"))
    .set_global_opts(
        brush_opts=opts.BrushOpts(),
        title_opts=opts.TitleOpts(title="我的柱状图", subtitle="hello bar", pos_left=100)
    )
)
bar.render('modelservice\chart\index7.html')

#增加水平区域缩放
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90], stack="stack1")
    .add_yaxis("商家B", [15, 25, 30, 18, 65, 70], stack="stack1")
    .add_yaxis("商家C", [25, 15, 50, 38, 25, 20])
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside"))
    .set_global_opts(
        brush_opts=opts.BrushOpts(),
        datazoom_opts=opts.DataZoomOpts(),
        title_opts=opts.TitleOpts(title="我的柱状图", subtitle="hello bar", pos_left=100)
    )
)
bar.render('modelservice\chart\index8.html')


#增加垂直区域选择组件
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90], stack="stack1")
    .add_yaxis("商家B", [15, 25, 30, 18, 65, 70], stack="stack1")
    .add_yaxis("商家C", [25, 15, 50, 38, 25, 20])
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside"))
    .set_global_opts(
        brush_opts=opts.BrushOpts(),
        # datazoom_opts=opts.DataZoomOpts(),
        datazoom_opts=opts.DataZoomOpts(orient="vertical"),
        title_opts=opts.TitleOpts(title="我的柱状图", subtitle="hello bar", pos_left=100),
        yaxis_opts=opts.AxisOpts(name="我是 Y 轴"),
        xaxis_opts=opts.AxisOpts(name="我是 X 轴"),
    )
)
bar.render('modelservice\chart\index9.html')


#增加工具栏
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90], stack="stack1")
    .add_yaxis("商家B", [15, 25, 30, 18, 65, 70], stack="stack1")
    .add_yaxis("商家C", [25, 15, 50, 38, 25, 20])
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside"))
    # .set_series_opts(
    #         label_opts=opts.LabelOpts(is_show=False),
    #         markpoint_opts=opts.MarkPointOpts(
    #             data=[
    #                 opts.MarkPointItem(type_="max", name="最大值"),
    #                 opts.MarkPointItem(type_="min", name="最小值"),
    #                 opts.MarkPointItem(type_="average", name="平均值"),
    #             ]
    #         ),
    #     )
    .set_global_opts(
        brush_opts=opts.BrushOpts(),
        datazoom_opts=opts.DataZoomOpts(),
        toolbox_opts=opts.ToolboxOpts(),
        title_opts=opts.TitleOpts(title="我的柱状图", subtitle="hello bar", pos_left=100)
    )
)
bar.render('modelservice\chart\index10.html')


#tip侧边条

bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 60], stack="stack1")
    .add_yaxis("商家B", [15, 25, 30, 18, 65, 70], stack="stack1")
    .add_yaxis("商家C", [25, 15, 50, 38, 25, 20])
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside"))
    .set_global_opts(
        brush_opts=opts.BrushOpts(),
        datazoom_opts=opts.DataZoomOpts(),
        toolbox_opts=opts.ToolboxOpts(),
        title_opts=opts.TitleOpts(title="我的柱状图", subtitle="hello bar", pos_left=100),
        graphic_opts=[
            opts.GraphicGroup(
                graphic_item=opts.GraphicItem(
                    rotation=JsCode("Math.PI / 4"),
                    bounding="raw",
                    right=110,
                    bottom=110,
                    z=100,
                ),
                children=[
                    opts.GraphicRect(
                        graphic_item=opts.GraphicItem(
                            left="center", top="center", z=100
                        ),
                        graphic_shape_opts=opts.GraphicShapeOpts(width=400, height=50),
                        graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                            fill="rgba(0,0,0,0.3)"
                        ),
                    ),
                    opts.GraphicText(
                        graphic_item=opts.GraphicItem(
                            left="center", top="center", z=100
                        ),
                        graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                            text="pyecharts bar chart",
                            font="bold 26px Microsoft YaHei",
                            graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                fill="#fff"
                            ),
                        ),
                    ),
                ],
            )
        ]
    )
)
bar.render('modelservice\chart\index11.html')

#自定义颜色

color_function = """
        function (params) {
            if (params.value > 0 && params.value < 50) {
                return 'red';
            } else if (params.value > 50 && params.value < 100) {
                return 'blue';
            }
            return 'green';
        }
        """
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90],
               itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function)))
    .add_yaxis("商家C", [25, 15, 50, 38, 25, 20],
               itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function)))
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside"))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="我的柱状图", subtitle="hello bar", pos_left=100),
    )
)
bar.render('modelservice\chart\index12.html')

#设置markpoint
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
    .add_yaxis("商家B", [15, 25, 30, 18, 65, 70])
    .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False),
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="最大值"),
                opts.MarkPointItem(type_="min", name="最小值"),
                opts.MarkPointItem(type_="average", name="平均值"),
            ]
        ),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="我的柱状图", subtitle="hello bar", pos_left=100),
    )
)
bar.render('modelservice\chart\index13.html')

#设置markline
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
    .add_yaxis("商家B", [15, 25, 30, 18, 65, 70])
    .set_series_opts(
        label_opts=opts.LabelOpts(is_show=True),
        markline_opts=opts.MarkLineOpts(
            data=[opts.MarkLineItem(y=30, name="yAxis=30")],
            symbol_size=[20, 10],
            linestyle_opts=opts.LineStyleOpts(color='red', width=2)
        ),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="我的柱状图", subtitle="hello bar", pos_left=100),
    )
)
bar.render('modelservice\chart\index14.html')





