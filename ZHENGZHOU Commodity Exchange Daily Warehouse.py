import datetime
import os
import requests
updateDays = 10#今天向前
today = datetime.datetime.now()
date = today - datetime.timedelta(days = updateDays) 

if today.hour < 16:
    enddate = datetime.datetime.now() - datetime.timedelta(days = 1)
else:
    enddate = datetime.datetime.now()

while (date <= enddate):    
    split_date = enddate.strftime('%Y-%m-%d').split('-')
    url_excel = ("http://www.czce.com.cn/cn/DFSStaticFiles/Future/%s/%s/FutureDataWhsheet.xls"%\
        (split_date[0],split_date[0]+split_date[1]+split_date[2]))
    res =  requests.get(url_excel)
    s = './郑商所'
    if os.path.exists(s)==False:
        os.makedirs(s);    
    with open("./郑商所/"+split_date[0]+split_date[1]+split_date[2]+"_FutureDataWhsheet.xls",'wb') as file:
        file.write(res.content)
        print('取全部数据  日期 = '+enddate.strftime('%Y%m%d'))
        file.close()    
    enddate = enddate - datetime.timedelta(days = 1)
