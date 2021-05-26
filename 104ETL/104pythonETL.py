import requests
from bs4 import BeautifulSoup
import time
import json
import re
import pandas as pd
import random

# 同意字
sysets = []
with open('./ss.txt', 'r', encoding='utf-8') as f:
    xs = f.readlines()
    for s in xs:
        s = s.split(',')
        s.pop()
        sysets.append(s)

columns = ['keywords', '地點', '工作抬頭', '公司名', '工作url', '需要工作經歷', '需求科系', '語言', '語言程度']
skill = []
skill_bigdata = []
data = []
url = f'https://www.104.com.tw/jobs/search/'
keywords = []
with open('./bigData.txt', 'r', encoding='utf-8-sig') as f:
    for x in f.readlines():
        keywords.append(x.replace('\n', ''))
# keywords = ['資料分析','數據分析']
for keyword in keywords:
    print(f'---------{keyword}職位---------')
    for i in range(3):
        params = {'keyword': keyword, 'page': i}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        res = requests.get(url=url, headers=headers, params=params)
        soup = BeautifulSoup(res.text, 'html.parser')
        articles = soup.select('article.b-block--top-bord')
        for article in articles:
            try:
                time.sleep(random.uniform(0, 2))
                job_data = []
                if len(article.select('svg.b-icon--gray.b-icon--w18 use')) == 3:
                    continue
                job_title = article.select('a.js-job-link')[0].text  # 工作抬頭
                job_url = 'https:' + article.select('a.js-job-link')[0]['href']  # 工作url
                company = article.select('ul.b-list-inline li a')[0].text.replace(' ', '').replace('\n', '')  # 公司
                print(company)
                job_address = article.select('ul.b-list-inline.b-clearfix.job-list-intro li')[0].text  # 地區
                ajax_url_x = re.search('/.{5}\?', job_url).span()
                x = job_url[(ajax_url_x[0] + 1):(ajax_url_x[1] - 1)]
                ajax_url = f'https://www.104.com.tw/job/ajax/content/{x}'
                headers['Referer'] = f'https://www.104.com.tw/job/{x}'
                job_res = requests.get(url=ajax_url, headers=headers)
                jd = json.loads(job_res.text)
                job_skills = jd['data']['condition']['specialty']  # 需要技能
                job_workexp = jd['data']['condition']['workExp']  # 工作經歷
                # 學歷
                if len(jd['data']['condition']['major']) == 0:
                    job_major = None
                else:
                    job_major = jd['data']['condition']['major']

                # 語言
                job_language = jd['data']['condition']['language']
                if len(job_language) > 0:
                    job_language_l = jd['data']['condition']['language'][0]['language']
                    job_language_level = jd['data']['condition']['language'][0]['ability']
                    job_language_data = job_language_l + ':' + job_language_level
                else:
                    job_language_l = None
                    job_language_level = None
                job_data = [keyword, job_address, job_title, company, job_url, job_workexp, job_major, job_language_l,
                            job_language_level]
                skill_data = []
                for job_skill in job_skills:
                    y = 0
                    for syset in sysets:
                        if job_skill['description'] in syset:
                            skill.append(syset[0])
                            skill_data.append(syset[0])
                            y = y + 1
                            break
                    if y == 0:
                        skill.append(job_skill['description'])
                        skill_data.append(job_skill['description'])
                print(skill_data)
                data.append(job_data)
                skill_bigdata.append(skill_data)
            except AttributeError:
                print('資料有誤')

#     time.sleep(2)
skill = set(skill)
# columns =['keyword','地點','工作抬頭','公司名','工作url','需要工作經歷','需求科系','語言','語言程度']
df = pd.DataFrame(data=data, columns=columns)
for s in skill:
    df[s] = ''
for i, xs in enumerate(skill_bigdata):
    if len(s) == 0:
        continue
    for s in xs:
        df[s][i] = 'v'

df.to_csv('./104data.csv', encoding='utf-8-sig')
df.head()