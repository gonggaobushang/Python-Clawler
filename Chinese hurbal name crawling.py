#爬取中草药名称
import requests
from bs4 import BeautifulSoup
res=requests.get("http://m.zhongyoo.com/name/page_1.html")
res.encoding='gbk'
soup=BeautifulSoup(res.text,'html.parser') #lxml
plant_names=[]
names=soup.select('.t')   
for name in names:
    plant_names.append(name.text) 
name=[]
for t in range(1,11):
    print(t)
    tql=requests.get("http://m.zhongyoo.com/name/page_{0}.html".format(t))
    tql.encoding="gbk"
    text=BeautifulSoup(tql.text,'html.parser')
    names=text.select(".t")
    for p in names:
        name.append(p.text)
