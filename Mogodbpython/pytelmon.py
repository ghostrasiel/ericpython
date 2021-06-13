from pymongo import collection
from pymongo.message import insert
import requests
from bs4 import BeautifulSoup
import os 
import random
import time
import datetime
import pymongo

url = 'https://www.ptt.cc/bbs/stock/index.html'
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
headers = {'User-Agent' : userAgent}
cookies = {'over18':'1'}
today = datetime.datetime.today().strftime('%Y-%m-%d')
#Mongodb
client = pymongo.MongoClient(host='localhost',port=27017)
mydb = client.erictest
collection = mydb.pttstock
if collection.find_one() != None:
    for r in collection.find().sort("_id",-1).limit(1):
        mongo_id = r['_id']
else:
    mongo_id = 0

for i in range(3): 
    print(f'-------第{i+1}頁開始--------')
    res = requests.get(url = url , headers  = headers , cookies = cookies) 
    soup = BeautifulSoup(res.text)
    clums = soup.select('div.r-ent') #文章格
    y = 0
    for clum in clums :
        date = {}
        try:
            y =y+1
            title = clum.find('a').text.replace('\w','')
            for a in ('/','?','.','*','>','<',':'):
                title = title.replace(a ,'')
            href ='https://www.ptt.cc'+clum.find('a')['href']
            time.sleep(random.randint(1,3))
            post_res = requests.get(url = href , headers=headers , cookies = cookies)
            post_soup = BeautifulSoup(post_res.text)
            post_title = post_soup.title.text.split(' - ')[0]
            post_author = post_soup.findAll('div' , class_='article-metaline')[0].find('span' , 'article-meta-value').text
            post_time = post_soup.findAll('div' , class_='article-metaline')[2].find('span' , 'article-meta-value').text
            post_reply = post_soup.findAll('div' , class_='push')
            n = 0
            good = 0
            bad = 0
            for r in range(0, len(post_reply)):
                n = n+1
                if len(post_reply[r].find('span')['class']) == 2:
                    good = good +1
                elif len(post_reply[r].find('span')['class']) == 3:
                    if '噓 ' in post_reply[r].find('span' , class_='f1 hl push-tag'):
                            bad =bad + 1
            print(title)

            if collection.find_one({'文章標題':post_title}) == None :
                mongo_id = mongo_id + 1
                date['_id']=mongo_id
                date['爬蟲時間']=today
                date['文章標題']=post_title
                date['作者']=post_author
                date['發文時間']=post_time
                date['回文數']=n
                date['讚數']=good
                date['噓數']=bad
                collection.insert(date)
            else:
                print('此資料已經存在')
        except:
            print('水桶文章')
        time.sleep(random.randint(1,3))
    print(f'共{y}個文章被下載')
    print('-------結束--------')
    url = 'https://www.ptt.cc'+soup.find('div', class_='btn-group btn-group-paging').findAll('a')[1]['href']