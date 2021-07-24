from flask import Flask , render_template
import os
import pandas as pd
import re
from pyecharts import options as opts
from pyecharts.charts import Pie , Bar ,TreeMap ,Sunburst

app = Flask(__name__)

file = os.path.dirname(os.path.realpath(__file__))
data = pd.read_csv(f'{file}/電動車拖吊資料.csv')

for x,y in enumerate(data['車型']) :
    try:
        data['車型'][x]=re.sub('\(.+\)', '', data['車型'][x])
    except:
        pass
    try:
        data['廠牌'][x]=re.sub('\s', '', data['廠牌'][x])
    except:
        pass
    try:
        data['廠牌'][x]=re.sub('Gogoro', 'GOGORO', data['廠牌'][x])
    except:
        pass

car_type = data['車種(二輪/四輪)'].value_counts() #ok
car_class = data['廠牌'].value_counts()
car_id = data['車型'].value_counts()
car_id_data = []
for i in dict(car_id).keys():
    ddata = {'value':int(dict(car_id)[i]) , 'name':i}
    car_id_data.append(ddata)
car_err = data['車輛故障原因'].value_counts()

Srr_data =[]
for i in range(0 , len(data['車種(二輪/四輪)'].unique())-1):
    a =data[data['車種(二輪/四輪)'].isin([data['車種(二輪/四輪)'].unique()[i]])]
    b = []
    
    for q in range(0 , len(a['廠牌'].unique())):
        if a['廠牌'].unique()[q] == 'nan':
            continue
        c = a[a['廠牌'].isin([a['廠牌'].unique()[q]])]
        d = []
        
        for r in range(0 , len(c['車型'].unique())):
            if c['車型'].unique()[r] == 'nan':
                continue
            e = c[c['車型'].isin([c['車型'].unique()[r]])]
            f = []
            
            for t in range(0 ,len(e['車輛故障原因'].unique())):
                if e['車輛故障原因'].unique()[t] == 'nan':
                    continue
                g = e[e['車輛故障原因'].isin([e['車輛故障原因'].unique()[t]])]
                f.append(opts.SunburstItem(name = e['車輛故障原因'].unique()[t],value=int(g['車輛故障原因'].count()),label_opts=opts.LabelOpts()))           
            
            d.append(opts.SunburstItem(name = c['車型'].unique()[r],value=int(e['車型'].count()),children=f ))
        b.append(opts.SunburstItem(name = a['廠牌'].unique()[q],value=int(c['廠牌'].count()) , children=d ))
    Srr_data.append(opts.SunburstItem(name =data['車種(二輪/四輪)'].unique()[i] , value=int(a['車種(二輪/四輪)'].count()),children=b))
    


def pie_base():
    c = (Pie()
    .add(series_name='車種(二輪/四輪)',
    data_pair=[(car_type.keys()[0] , int(car_type[0])),(car_type.keys()[1] , int(car_type[1]))]
    ).set_global_opts(title_opts=opts.TitleOpts('故障車種' ,
    title_textstyle_opts=opts.TextStyleOpts(font_size='20' ,color='rgb(46,68,84)'),pos_left='15')
    ,legend_opts=opts.LegendOpts(is_show=False))
    )
    return c

def Bar_base():
    c = (Bar(init_opts=opts.InitOpts( width="500px",height="200px"))
    .add_xaxis(list(car_class.keys()))
    .add_yaxis('',list(map(int , car_class)),category_gap='0%' ,bar_width='50%'
    ,label_opts=opts.LabelOpts(position='right') , itemstyle_opts=opts.ItemStyleOpts(color='rgb(46,68,84)'))
    .reversal_axis()
    .set_global_opts(title_opts=opts.TitleOpts('故障廠牌' ,
    title_textstyle_opts=opts.TextStyleOpts(font_size='20' ,color='rgb(46,68,84)'),pos_left='10',pos_top='15'),
        yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size='10')))
    )
    return c

def tree_base():
    c=(TreeMap()
    .add(
        series_name="",
        data=car_id＿data ,
        #levels 為每個層級分別設定
        levels=[opts.TreeMapLevelsOpts(treemap_itemstyle_opts=opts.TreeMapItemStyleOpts(border_color="white",
        border_width=1, gap_width=1))],color_alpha=[0.3 , 0.4],roam=False )
    .set_global_opts(title_opts=opts.TitleOpts('故障車型' ,
    title_textstyle_opts=opts.TextStyleOpts(font_size='20' ,color='rgb(46,68,84)'),pos_left='15') , visualmap_opts=opts.VisualMapOpts(type_='color' , range_color=['rgba(46,68,83,0.1)', 'rgba(46,68,84,1)'] , min_=0,max_=2500,dimension=0)
    ))
    return c

def pie_base2():
    car_err_data=[]
    for x in range(0 , len(car_err)):
        ddata = (car_err.keys()[x] , int(car_err[x]))
        car_err_data.append(ddata)
        if x == 5 :
            break
    c = (Pie()
    .add(series_name='車輛故障原因',
    data_pair=car_err_data , rosetype='radius',radius='80%'
    ).set_global_opts(title_opts=opts.TitleOpts('故障原因' ,
    title_textstyle_opts=opts.TextStyleOpts(font_size='20' ,color='rgb(46,68,84)'),pos_left='15'),legend_opts=opts.LegendOpts(is_show=False)) #隱藏標籤
    )
    return c

def Sun_base():
    c = (
    Sunburst(init_opts=opts.InitOpts(width="1000px", height="600px"))
    .add(series_name="", data_pair=Srr_data, radius=['10%', "90%"],highlight_policy='ancestor')
    .set_global_opts(title_opts=opts.TitleOpts('總覽' ,
    title_textstyle_opts=opts.TextStyleOpts(font_size='20' ,color='rgb(46,68,84)'),pos_left='15'))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}"))
)
    return c

@app.route('/')
def index():
    return render_template('Dashboard.html')

@app.route('/PieChart')
def get_pie_chart():
    c = pie_base()
    return c.dump_options_with_quotes()

@app.route('/BarChart')
def get_bar_chart():
    c = Bar_base()
    return c.dump_options_with_quotes()

@app.route('/treeChart')
def get_tree_chart():
    c = tree_base()
    return c.dump_options_with_quotes()

@app.route('/PieChart2')
def get_pie_chart2():
    c = pie_base2()
    return c.dump_options_with_quotes()

@app.route('/SunChart')
def get_Sun_chart():
    c = Sun_base()
    return c.dump_options_with_quotes()


if __name__ == "__main__":
    app.run(host='0.0.0.0' , port=5000 , debug=True)