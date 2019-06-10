#大商所仓单数据
#每个交易日下午4点左右更新
#网站url不变，但是每天的数值会变化
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

url="http://www.dce.com.cn/publicweb/quotesdata/wbillWeeklyQuotes.html"

today=datetime.datetime.now()-datetime.timedelta(7)    #随便选一个交易日     
day=today.strftime("%Y,%m,%d").split(",")  #将年月日分开
formdate={'wbillWeeklyQuotes.variety':'all',
          "year":day[0],
          "month":str(int(day[1])-1),   #网站独特设计：月份要提早一个月
          "day":day[2]}

res=requests.post(url,data=formdate)
soup=BeautifulSoup(res.content.decode("utf8"),"lxml")

temp=[]
table=[]
count=0
for i in soup.select("table")[0].find_all("td"):
    if(count==5):
        table.append(list(temp))
        temp.clear()   #清空
        temp.append(i.get_text().strip())
        count=1  #此时运行到下一行的第一列
    else:
        temp.append(i.get_text().strip())
        count+=1
#最后一行没有加上去
table.append(list(temp))   #加上最后一行的总计
data=pd.DataFrame(table)
data.to_excel("F:\\大商所仓单日报"+day[0]+day[1]+day[2]+".xls",index=None)


res.close()
