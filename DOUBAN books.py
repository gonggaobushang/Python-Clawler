#豆瓣书籍信息爬取
import json
import requests
import pandas as pd
from lxml import etree

bsdf=pd.read_excel('C:\\Users\\Administrator.000\\Desktop\\python\\实战\\爬虫\\豆瓣书籍.xlsx') 
blst=list(bsdf['书名']) #书名列表
bsdf.head(3)

def getBookInfo(binfo,cc):
    i=0
    rss={}
    k=''
    v=''
    f=0
    clw=[]
    for c in cc:
        #print(c)
        if '\n' in c:
            if '\xa0' in c:
                clw.append(c)
        else:
            clw.append(c)
    
    for m in binfo[0]:
        #print(m)
        if m.tag=='span':
            mlst=m.getchildren()
            if len(mlst)==0: 
                k=m.text.replace(':','')
                if '\xa0' in clw[i]:
                    f=1#需要m.tag=='a'下的值
                else:
                    v=clw[i].replace('\n','').replace(' ','')
                i+=1
            elif len(mlst)>0:#下面有子span 一种判断是m.attrib=={} 不够精确
                for n in mlst:
                    if n.tag=='span':
                        k=n.text.replace('\n','').replace(' ','') #不至于下面还有span，懒得用递归了
                    elif n.tag=='a':
                        v=n.text.replace('\n','').replace(' ','')
        
        elif m.tag=='a':
            if f==1: #是否可以不用这个if
                v=m.text.replace('\n','').replace(' ','')
                f=0
        elif m.tag=='br':
            if k=='':
                print(i,'err')
            else:
                rss[k]=v
        else:
            print(m.tag,i)
    return rss



rlst=[]
for bn in blst:
    res={}
    r=requests.get('https://book.douban.com/j/subject_suggest?q={0}'.format(bn))
    rj=json.loads(r.text)
    html=requests.get(rj[0]['url']) 
    con = etree.HTML(html.text)
    bname=con.xpath('//*[@id="wrapper"]/h1/span/text()')[0] #和bn比较
    res['bname_sq']=bn
    res['bname']=bname
    res['dbid']=rj[0]['id'] 
    binfo=con.xpath('//*[@id="info"]')
    cc=con.xpath('//*[@id="info"]/text()')
    res.update(getBookInfo(binfo,cc))  #在列表中增加
    bmark=con.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')[0]
    if bmark=='  ':
        bits=con.xpath('//*[@id="interest_sectl"]/div/div[2]/div/div[2]/span/a/text()')[0]
        if bits=='评价人数不足':
            res['评分']=''
            res['评价人数']='评价人数不足'
        else:
            res['评分']=''
            res['评价人数']=''
    else:
        res['评分']=bmark.replace(' ','')
        bmnum=con.xpath('//*[@id="interest_sectl"]/div/div[2]/div/div[2]/span/a/span/text()')[0]
        res['评价人数']=bmnum
    rlst.append(res)
    
    
outdf=pd.DataFrame(rlst)
outdf.to_excel('C:\\Users\\Administrator.000\\Desktop\\python\\实战\\爬虫\\豆瓣书籍_结果.xlsx',index=False) 


