from json import loads
import traceback
import random

import pandas as pd
# import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import time

loc_file = pd.read_excel('../A级旅游景区名录.xlsx')
loc_data = loc_file[loc_file['等级'] == '5A']

# for line in loc_data.itertuples():
#     longitude = float(getattr(line, '经度'))
#     latitude = float(getattr(line, '纬度'))
def login_by_cookie():
    from selenium import webdriver
    from time import sleep
    import json
    from selenium.webdriver.common.by import By

    driver = webdriver.Chrome()
    driver.get('https://mail.163.com/')
    driver.implicitly_wait(20)
    driver.switch_to.frame(0)
    driver.find_element(By.NAME, "email").send_keys('xxx@163.com')
    driver.find_element(By.NAME, "password").send_keys('xxxxxx')
    driver.find_element(By.ID, "dologin").click()
    sleep(3)
    mycookies = driver.get_cookies()
    jsoncookies = json.dumps(mycookies)
    with open("mycookie.json", 'w') as f:
        f.write(jsoncookies)
    driver.quit()


def huakuai():
    # 创建浏览器实例
    option = webdriver.ChromeOptions()
    # 隐藏selenium的自动自动控制的功能的显示防止被检测
    option.add_argument('--disable-blink-features=AutomationControlled')
    # 设置修改selenium的特征值，防止被检测到
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 加载浏览器驱动
    driver = webdriver.Chrome(options=option)



    # 高德
    uli = "https://www.amap.com/service/poiInfo?query_type=RQBXY&pagesize=20"\
          "&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000"\
          "&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=9.55"\
          "&longitude=103.919224&latitude=33.266991&range=1000&city=513200&keywords=美食"

    # response = requests.get(uli, headers = header)
    # 打开网页
    try:
        driver.get(uli)
        cookie = {'name': 'x-csrf-token', 'value': '4674d9cc4c97968d74763e840ed70bc5',
                  'name': 'passport_login', 'value': 'NDY5MDYxNzE4LGFtYXBCdXNRUUlKRmYsbGxxZGw2NTZwd2docXNjenFocGN4eGdwbWJyNG5jd2csMTY5MzI4MTM1OSxaRGc1TmpFM01EZzNOVFkyTUdabVptSmlNV1kwWW1GbU9HWTFZek0yWkdVPQ%3D%3D'}
        driver.add_cookie(cookie)
        time.sleep(5)

        # 执行 JavaScript 代码，获取滑块元素
        slider = driver.find_element(By.XPATH, "//*[@id='nc_1_n1z']")

        # # 获取滑块的初始位置和目标位置
        # initial_position = slider.location['x']
        # target_position = 250

        # 计算滑动距离
        # distance_to_slide = target_position - initial_position
        distance_to_slide = 260

        # 创建一个动作链
        action = ActionChains(driver)

        # 拖动滑块
        def move_and_pass(maximum=5, now = 1):
            #
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
            time.sleep(0.015)
            imitate.perform()
            time.sleep(random.randint(6, 10) / 10)
            imitate.perform()
            time.sleep(0.04)
            imitate.perform()
            time.sleep(0.012)
            imitate.perform()
            time.sleep(0.019)
            imitate.perform()
            time.sleep(0.033)
            action.move_by_offset(xoffset=1, yoffset=0).perform()
            #
            # action.click_and_hold(slider).perform()
            # action.move_by_offset(distance_to_slide, 0).perform()
            # action.release(slider).perform()

            time.sleep(2)

            # 在这里检查是否成功通过验证码，以及获取所需的数据
            body_data = driver.find_element(By.TAG_NAME, 'body').text
            data_json = loads(body_data) # 包含相关数据的json数据
            print(data_json)


        move_and_pass()
    except Exception as err:
        error_msg = ''.join(traceback.format_exception(type(err), err, err.__traceback__))
        print(error_msg)
    finally:
        # 关闭浏览器窗口
        driver.quit()

huakuai()

# res_json = response.json()

# res_list = res_json['content'] # 选项列表
# options_dict = {} # 选项字典
#
# if res_list:
#     for index, line in enumerate(res_list):
#         if line:
#             name = line['name'] # 名称
#             address = line['address_norm'] # 地址
#             distance = line['dis'] # 距离
#             options_dict[index] = [name, address, distance]
#         else:
#             continue
#
#     print(options_dict)
# else:
#     print('没有值', res_json)