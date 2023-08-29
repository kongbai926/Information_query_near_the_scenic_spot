import json
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
    # # 设置无头模式，不显示可视化界面
    # option.add_argument('--headless')
    # 加载浏览器驱动
    driver = webdriver.Chrome(options=option)

    # 高德
    uli = "https://www.amap.com/service/poiInfo?query_type=RQBXY&pagesize=20" \
          "&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000" \
          "&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=9.55" \
          "&longitude=103.919224&latitude=33.266991&range=1000&city=513200&keywords=美食"

    # response = requests.get(uli, headers = header)
    # 打开网页
    try:
        driver.get(uli)
        cookie = {'name': 'x-csrf-token', 'value': '4674d9cc4c97968d74763e840ed70bc5',
                  'name': 'passport_login', 'value': 'NDY5MDYxNzE4LGFtYXBCdXNRUUlKRmYsbGxxZGw2NTZwd2docXNjenFocGN4eGdwbWJyNG5jd2csMTY5MzI4MTM1OSxaRGc1TmpFM01EZzNOVFkyTUdabVptSmlNV1kwWW1GbU9HWTFZek0yWkdVPQ%3D%3D'
                  }
        driver.add_cookie(cookie)
        time.sleep(5)

        # 拖动滑块
        def move_and_pass(maximum=5, now=1):
            # 执行 JavaScript 代码，获取滑块元素
            slider = driver.find_element(By.XPATH, "//*[@id='nc_1_n1z']")

            # # 获取滑块的初始位置和目标位置
            # initial_position = slider.location['x']
            # target_position = 250

            # 计算滑动距离
            # distance_to_slide = target_position - initial_position
            distance_to_slide = random.randint(257, 263)

            # 创建一个动作链
            action = ActionChains(driver)

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
            #
            # action.click_and_hold(slider).perform()
            # action.move_by_offset(distance_to_slide, 0).perform()
            # action.release(slider).perform()

            time.sleep(2)

            # 在这里检查是否成功通过验证码，以及获取所需的数据
            try:
                body_data = driver.find_element(By.TAG_NAME, 'body').text
                data_json = loads(body_data)  # 包含相关数据的json数据
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
                #         通过验证，json数据正常获取到
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

                data_dict = analyze_data(data_json)
                print(json.dumps(data_dict))
                print(json.loads(json.dumps(data_dict)))

        move_and_pass()
    except Exception as err:
        error_msg = ''.join(traceback.format_exception(type(err), err, err.__traceback__))
        print(error_msg)
    finally:
        # 关闭浏览器窗口
        driver.quit()


huakuai()
