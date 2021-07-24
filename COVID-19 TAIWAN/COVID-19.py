import re
import requests
from bs4 import BeautifulSoup
from requests.sessions import session
from selenium.webdriver import Chrome
import time
import json
url = 'https://nidss.cdc.gov.tw/nndss/DiseaseMap_Pro'
# driver = Chrome('C:/Users/Tibame_25/Desktop\ericpython/104ETL/chromedriver.exe')
# driver.get(url)
# time.sleep(2)
# driver.close()
y='桃園'
a='%u6843%u5712%u5E02'
print(a.encode('utf-8'))
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
'referer': 'https://nidss.cdc.gov.tw/nndss/DiseaseMap?id=19CoV','content-length': '251','x-requested-with':'XMLHttpRequest'}
data = {'pty_Q': 'N','pty_disease':'19CoV','position':'1','pty_period':'y','pty_y_s':'2021','pty_y_e':'2021','pty_m_s':'1',
'pty_m_e':'5','pty_d_s':'1','pty_d_e':'27','pty_w_s':'1','pty_w_e':'1','pty_sickclass_value':'determined_cnt','pty_immigration':'0',
'pty_date_type':'3','pty_level':'area','region_name':x}
res = requests.get(url=url,headers=headers , data = data)
# jsonData=json.loads(res)
# print(res.text)
