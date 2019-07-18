import os
import time 
import json
import random
import requests

path="C:\\Users\\Administrator.000\\Desktop\\京东-水-评论.txt"

def jingdong_comments(page=0):
    """
    爬取京东商品评论信息
    https://item.jd.com/848852.html
    """
    url="https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv32191&productId=848852&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&fold=1" % page
    lv={"User-Agent": "Mozilla/5.0","Referer": "https://item.jd.com/848852.html"}
    try:
        q=requests.get(url,headers=lv)
        q.raise_for_status()
        print(q.text[27:-2]) #只需要json格式的部分
    except:
        print("failed")
        
    q_str=q.text[27:-2]
    q_com=json.loads(q_str)["comments"]
    for com in q_com:
        print(com["content"])
        with open(path,"a+") as file:
            file.write(com["content"]+"\n")
            
    
        
def   jingdong_morecomments():
    """
    分页
    爬取多个url
    """
    if os.path.exists(path):
        os.remove(path)
    for i in range(10):
        jingdong_comments(i)
        time.sleep(random.random()*2)
        


if __name__=="__main__":
    jingdong_morecomments()
