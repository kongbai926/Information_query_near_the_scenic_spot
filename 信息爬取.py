from gevent import monkey
import gevent
import requests
from gevent.queue import Queue
import pandas as pd
from 经纬度查询并显示 import get_get_location_m

loc_file = pd.read_excel("A级旅游景区名录.xlsx")
loc_pd = loc_file[loc_file["等级"] == "5A"]


#  协程运行
monkey.patch_all()

# 构造景区查询网址列表
def urlList(need):
    """
    根据传入need参数确定查找美食或者酒店等网址
    return: url_list: 爬虫可以获取信息的直接网址
    """
    url_list = list()
    for line in loc_pd.itertuples():
        longitude = str(getattr(line, '经度'))
        latitude = str(getattr(line, '纬度'))
        url_list.append("https://ditu.amap.com/search" \
                        + "?query=" + need + "&query_type=RQBXY&longitude=" \
                        + longitude + "&latitude=" + latitude + "&range=1000")
    return url_list
    


#爬虫部分
def spyder_meishi(url_list):
    work = Queue()
    for uli in url_list:
        work.put_nowait(uli)
    
    # 爬虫具体任务，获取地址附近美食餐馆名称等信息
    def crawler():
        while not work.empty():
            url = work.get_nowait()
            response = requests.get(url)
            print(response.status_code)
    

    tasks_list = [gevent.spawn(crawler) for n in range(5)]

    #开始爬虫任务
    gevent.joinall(tasks_list)


# 获取经纬度信息 
def location_jingweidu(name):
    Longitude_and_latitude = get_get_location_m(name)['location']
    longitude, latitude = Longitude_and_latitude.split(',')[0], [1]
    print(longitude, latitude)
