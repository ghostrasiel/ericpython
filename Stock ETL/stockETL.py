import requests
from bs4 import BeautifulSoup
import json
url = 'https://mis.twse.com.tw/stock/group.jsp?ind=15&ex=tse&currPage=0&type=all'
res = requests.get(url)
print(res.text)




# page_url='https://mis.twse.com.tw/stock/api/getCategory.jsp?ex=tse&i=02'
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
# page_res=requests.get(url=page_url , headers=headers)
# page_jsons=json.loads(page_res.text)
# stock_xs = []
# for page_json in page_jsons['msgArray']:
#     x = page_json['key'].split('_')
#     stock_x=x[0]+'_'+x[1]
#     stock_xs.append(stock_x)
# s ='|'
# stock_str = s.join(stock_xs)

# url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={stock_str}|&json=1"
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
# res = requests.get(url=url , headers=headers)
# jsonData =json.loads(res.text)
# Data_arrays=jsonData['msgArray']
# for array in Data_arrays:
#     print('股票日期:'+array['d'])
#     print('更新時間點:'+array['t'])
#     print('股票名稱:'+array['n'])
#     print('股票代號:'+array['c'])
#     print('開盤價:'+array['o'])
#     print('漲停:'+array['u'])
#     print('跌停:'+array['w'])
#     print('當日最高:'+array['h'])
#     print('當日最低:'+array['l'])
#     print('成交價:'+array['z'])
#     print('成交量:'+array['v'])

