import json
import time
import requests
import pandas as pd

def get_comments(page):
    """
    获取网易云李圣杰《最近》的评论信息
    只能爬部分数据
    """
    url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_114369?limit=20&offset=' + str(page)
    response = requests.get(url=url)
    result = json.loads(response.text)
    items = result['comments']
    tmp= []
    for item in items:
        # 用户名
        user_name = item['user']['nickname'].replace(',', '，')
        # 用户ID
        user_id = str(item['user']['userId'])
        # 获取用户信息
        user_message = get_user(user_id)
        # 用户年龄
        user_age = str(user_message['age'])
        # 用户性别
        user_gender = str(user_message['gender'])
        # 用户所在地区
        user_city = str(user_message['city'])
        # 个人介绍
        user_introduce = user_message['sign'].strip().replace('', '').replace(',', '，')
        # 评论内容
        comment = item['content'].strip().replace('', '').replace(',', '，')
        # 评论ID
        comment_id = str(item['commentId'])
        # 评论点赞数
        praise = str(item['likedCount'])
        # 评论时间
        date = time.localtime(int(str(item['time'])[:10]))
        date = time.strftime("%Y-%m-%d %H:%M:%S", date)
        #print(user_name, user_id, user_age, user_gender, user_city, user_introduce, comment, comment_id, praise, date)
        #print(user_name)
        temp=[user_name,user_id,user_age,user_gender,user_city,user_introduce,comment,comment_id,praise,date]
        tmp.append(temp)
        
        
data_com = pd.DataFrame(tmp)        
data_com.to_excel('./《最近》'+'.xls',encoding='gbk',index=None)     
        

def get_user(user_id):
    """
    获取用户注册时间
    """
    data = {}
    url = 'https://music.163.com/api/v1/user/detail/' + str(user_id)
    response = requests.get(url=url)
    js = json.loads(response.text)
    if js['code'] == 200:
        # 性别
        data['gender'] = js['profile']['gender']
        # 年龄
        if int(js['profile']['birthday']) < 0:
            data['age'] = 0
        else:
            data['age'] = (2018 - 1970) - (int(js['profile']['birthday']) // (1000 * 365 * 24 * 3600))
        if int(data['age']) < 0:
            data['age'] = 0
        # 城市
        data['city'] = js['profile']['city']
        # 个人介绍
        data['sign'] = js['profile']['signature']
    else:
        data['gender'] = '无'
        data['age'] = '无'
        data['city'] = '无'
        data['sign'] = '无'
    return data


def main():
    for i in range(0, 120, 20):
        #print(i)
        print('---------------第 ' + str(i // 20 + 1) + ' 页---------------')
        get_comments(i)

#__name__ 是当前模块名，当模块被直接运行时模块名为 __main__ 。当模块被直接运行时，代码将被运行
#当模块是被导入时，代码不被运行。
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
  