import traceback

import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

loc_file = pd.read_excel('A级旅游景区名录.xlsx')
loc_data = loc_file[loc_file['等级'] == '5A']

# for line in loc_data.itertuples():
#     longitude = float(getattr(line, '经度'))
#     latitude = float(getattr(line, '纬度'))
def wangye():
    import requests

    url = 'https://www.amap.com/service/poiInfo?query_type=RQBXY&pagesize=20'\
          '&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000'\
          '&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=9.55'\
          '&longitude=103.919224&latitude=33.266991&range=1000&city=513200&keywords=%E7%BE%8E%E9%A3%9F'

    header = {
        "method": "GET",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "X-Csrf-Token": "f8d1bfee71ac75349c72dd96063bb842",
        "X-Requested-With": "XMLHttpRequest"
        }

    response = requests.get(url, headers=header)
    print(response.status_code, response.text)

def huakuai():
    # 创建浏览器实例
    driver = webdriver.Chrome()

    # 高德
    uli = "https://www.amap.com/service/poiInfo?query_type=RQBXY&pagesize=20"\
          "&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000"\
          "&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=9.55"\
          "&longitude=103.919224&latitude=33.266991&range=1000&city=513200&keywords=美食"

    # response = requests.get(uli, headers = header)
    # 打开网页
    try:
        driver.get(uli)
        wait = WebDriverWait(driver, 5)

        time.sleep(5)

        # 执行 JavaScript 代码，获取滑块元素
        slider = driver.find_element(By.XPATH, "//*[@id='nc_1_n1z']")

        # # 获取滑块的初始位置和目标位置
        # initial_position = slider.location['x']
        # target_position = 250

        # 计算滑动距离
        # distance_to_slide = target_position - initial_position
        distance_to_slide = 259

        # 创建一个动作链
        action = ActionChains(driver)

        # 拖动滑块
        def move_and_pass(maximum=5, now = 1):
            action.click_and_hold(slider).perform()
            action.move_by_offset(distance_to_slide, 0).perform()
            action.release().perform()

            time.sleep(2)

            # 在这里检查是否成功通过验证码，以及获取所需的数据
            try:
                block = wait.until(EC.presence_of_element_located((By.ID, 'nc_1__scale_text'))) # 滑块验证码的方框
            except selenium.common.exceptions.TimeoutException as err:
                error_msg = ''.join(traceback.format_exception(type(err), err, err.__traceback__))
                print(error_msg)
            except selenium.common.exceptions.NoSuchElementException as e:
                time.sleep(3)  # 通过验证，等待网页加载
                print(driver.page_source)
            else:
                if '验证失败' in block.text and maximum != 0:
                    print('第{}次尝试：'.format(now))
                    block.click()
                    move_and_pass(maximum - 1, now + 1)


        move_and_pass()
    except Exception as err:
        error_msg = ''.join(traceback.format_exception(type(err), err, err.__traceback__))
        print(error_msg)
    finally:
        # 关闭浏览器窗口
        driver.quit()

# wangye(
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