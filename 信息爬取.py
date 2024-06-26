# from gevent import monkey
# import gevent
# from gevent.queue import Queue
import pandas as pd

loc_file = pd.read_excel("A级旅游景区名录.xlsx")
loc_pd = loc_file[loc_file["等级"] == "5A"]

 # 协程运行
# monkey.patch_all()


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
        url_list.append("https://www.amap.com/service/poiInfo?query_type=RQBXY&pagesize=20" \
                        "&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000" \
                        "&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=9.55" \
                        "&longitude=" + longitude + "&latitude=" + latitude + "&range=1000&keywords=" + need)
    return url_list


# 爬虫部分1：编写爬虫具体任务，包括网页获取、数据获取、数据分析
def spyder_get_data(url):
    import json
    import traceback
    import random
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    import time

    # 创建浏览器实例
    option = webdriver.ChromeOptions()
    # 隐藏selenium的自动自动控制的功能的显示防止被检测
    option.add_argument('--disable-blink-features=AutomationControlled')
    # 设置修改selenium的特征值，防止被检测到
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # # 设置无头模式，不显示可视化界面
    # option.add_argument('--headless')
    # 加载浏览器驱动
    driver = webdriver.Chrome(options=option)

    # 打开网页
    try:
        driver.get(url)
        cookie = {'name': 'x-csrf-token', 'value': 'xxxxxxx',
                  'name': 'passport_login', 'value': 'xxxxxxx'
                  }
        driver.add_cookie(cookie)
        time.sleep(5)

        # 拖动滑块通过验证码
        def move_and_pass(maximum=5, now=1):
            # 执行 JavaScript 代码，获取滑块元素
            slider = driver.find_element(By.XPATH, "//*[@id='nc_1_n1z']")

            # 滑动距离
            distance_to_slide = random.randint(257, 263)

            # 创建一个动作链
            action = ActionChains(driver)

            # 滑动距离
            distance_to_slide = random.randint(258, 263)
            # 滑动时间
            slide_time = 2

            # 创建一个动作链
            action = ActionChains(driver)

            # 滑动方式一（借鉴他人代码）
            def move_block01():
                # 滑块移动轨迹
                def get_track(distance):
                    track = []
                    current = 0
                    mid = distance * 3 / 4
                    t = random.randint(2, 3) / 10
                    v = 0
                    while current < distance:
                        if current < mid:
                            a = 2
                        else:
                            a = -3
                        v0 = v
                        v = v0 + a * t
                        move = v0 * t + 1 / 2 * a * t * t
                        current += move
                        track.append(round(move))
                    return track

                # 生成拖拽移动轨迹，加3是为了模拟滑过缺口位置后返回缺口的情况
                track_list = get_track(distance_to_slide)
                time.sleep(2)
                action.click_and_hold(slider).perform()
                time.sleep(0.2)
                # 根据轨迹拖拽圆球
                for track in track_list:
                    action.move_by_offset(xoffset=track, yoffset=0).perform()
                # 模拟人工滑动超过缺口位置返回至缺口的情况，数据来源于人工滑动轨迹，同时还加入了随机数，都是为了更贴近人工滑动轨迹
                imitate = action.move_by_offset(xoffset=-1, yoffset=0)
                time.sleep(0.005)
                imitate.perform()
                time.sleep(random.randint(6, 10) / 10)
                imitate.perform()
                time.sleep(0.04)
                imitate.perform()
                time.sleep(0.012)
                imitate.perform()
                time.sleep(0.019)
                imitate.perform()
                time.sleep(0.003)
                action.move_by_offset(xoffset=1, yoffset=0).perform()

            # 滑动方式二（借助人工智能编写）
            def move_block02():
                # 鼠标按住滑块
                action.click_and_hold(slider).perform()
                # 通过多次小步滑动来模拟整个滑动过程，实现时间控制
                num_steps = 8  # 拆分滑动为多个小步
                step_size = int(distance_to_slide / num_steps)
                last_size = distance_to_slide - step_size * (num_steps - 1)
                for i in range(num_steps):
                    if i != num_steps - 1:
                        action.move_by_offset(step_size, 0).perform()
                    else:
                        action.move_by_offset(last_size, 0).perform()
                    time.sleep(slide_time / num_steps)  # 控制每一步的时间间隔

            action.release(slider).perform()

            move_block01()

            time.sleep(2)

            # 在这里检查是否成功通过验证码，以及获取所需的数据
            try:
                body_data = driver.find_element(By.TAG_NAME, 'body').text
                data_json = json.loads(body_data)  # 包含相关数据的json数据
            except json.decoder.JSONDecodeError:
                # 验证失败，重新尝试
                if maximum != 0:
                    driver.refresh()
                    time.sleep(3)
                    print('验证失败，第{}次尝试'.format(now))
                    move_and_pass(maximum - 1, now + 1)
                else:
                    #     达到最大次数也验证失败的判断，将滑动时间重置为最长时间，当前
                    print('数据获取失败！')
                # try:
                #     block = driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]')
                #     if '验证失败*' in block.text:
                #         print('验证失败，第{}次尝试'.format(now))
                #         block.click()
                #         time.sleep(1)
                #         move_and_pass(maximum - 1, now + 1)
                # except Exception as err:
                #     error_msg = ''.join(traceback.format_exception(type(err), err, err.__traceback__))
                #     print(error_msg)
            else:
                #通过验证，json数据正常获取到
                data_dict = analyze_data(data_json) # 提取到的有效数据
                # 数据处理部分
                print(json.loads(json.dumps(data_dict)))

        # 分析与提取数据
        def analyze_data(jsonData):
            data_list = jsonData['data']['poi_list']  # 提取出所有店的列表信息
            data_dict = {}  # 存储提取出来的所需保存的有效数据
            for index, line in enumerate(data_list):
                name = line['name']  # 名称
                address = line['address']  # 地址
                longitude = line['longitude']  # 经度
                latitude = line['latitude']  # 纬度
                cityname = line['cityname']  # 城市名称
                data_dict[index] = {
                    "name": name,
                    "address": address,
                    "cityname": cityname,
                    "longitude": longitude,
                    "latitude": latitude
                    }
            return data_dict

        move_and_pass()

    except Exception as err:
        error_msg = ''.join(traceback.format_exception(type(err), err, err.__traceback__))
        print(error_msg)
    finally:
        # 关闭浏览器窗口
        driver.quit()


# # 爬虫部分2：设置爬虫队列，开始爬虫任务
# def spyder_meishi(url_list):
#     work = Queue()
#     for uli in url_list:
#         work.put_nowait(uli)
#
#     # 爬虫具体任务，获取地址附近美食餐馆名称等信息
#     def crawler():
#         while not work.empty():
#             url = work.get_nowait()
#             spyder_get_data(url=url)
#
#     tasks_list = [gevent.spawn(crawler) for n in range(5)]
#
#     # 开始爬虫任务
#     gevent.joinall(tasks_list)
#     print('Done! All requests are processed.')


if __name__ == '__main__':
    need_list = ['美食', '酒店'] # 需要在地址周围查询的信息列表
    for i in need_list:
        for url in urlList(i):
            spyder_get_data(url)
