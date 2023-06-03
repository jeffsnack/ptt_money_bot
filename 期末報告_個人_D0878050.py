#!/usr/bin/env python
# coding: utf-8

# In[14]:


import requests
from bs4 import BeautifulSoup
import concurrent.futures
import datetime

#TODO LIST
#建一個空LIST，還有一個字典，把每一筆PTT資訊塞進字典裏面再塞進LIST，用SET方法去除重複SET

list_keywords = ['蝦皮','uber','line','星巴克','買一送一','SWITCH','國泰','優步','全家'] #每一個關鍵字都去執行下面的函數

result = []


def scrape(list_keywords):
    try:
        today = datetime.date.today() #今日日期
        
        if today.day<10: #ptt日期格式
            today_time = str(today.month)+'/0'+str(today.day)
        else:
            today_time = str(today.month)+'/'+str(today.day)
        for i in range(1,4): #執行搜尋到的前三頁
            url = f'https://www.ptt.cc/bbs/Lifeismoney/search?page={i}&q={list_keywords}'

            req = requests.get(url)

            soup = BeautifulSoup(req.text,'html.parser')

            sel = soup.select('div.r-ent')

            for j in sel:
                title = j.find('a').text
                href = 'https://www.ptt.cc' + j.find('a')['href']
                date = j.find('div','date').text.strip() #將取得日期的空白清掉
                if date == today_time:#有查詢到資料，只是不符合今天日期
                    result_data = {'title':title,'href':href,'date':date}
                    result.append(result_data)
                    print(r.status_code)  #200表示成功
                    print(title,date)
                    print(href)
                         
            return result
    except:
        print('目前並無相關資料')

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor: #平行處理
    executor.map(scrape,list_keywords)

#print(result)
result_data = [dict(t) for t in set([tuple(d.items()) for d in result])] #用set去除相同的情報

for i in result_data: #寄送line通知    
    headers = {
        "Authorization": "Bearer " + "olB8DG5BR8BePOAC98V185IAnFUWUel35MWiLiYs9bv",
        "Content-Type": "application/x-www-form-urlencoded"}
    params = {"message":f"{i['title']}\n{i['href']}\n{i['date']}"}
    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=params)
    print(r)


# In[ ]:




