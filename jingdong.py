#requests库的基本运用
import requests
def jingdong():
    """
    爬取京东信息
    https://item.jd.com/848852.html
    """
    url="https://item.jd.com/848852.html"
    try:
        q=requests.get(url)
        q.raise_for_status()
        print(q.text)
    except:
        print("failed")
        


if __name__=="__main__":
    jingdong()
