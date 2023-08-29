import pandas as pd
import requests

loc_file = pd.read_excel('A级旅游景区名录.xlsx')
loc_data = loc_file[loc_file['等级'] == '5A']


data = {
    "wd": "美食", # 搜索关键字
    "nb_x": 0, # 经度
    "nb_y": 0, # 纬度
    "b": (0, 0) # 经纬度组成的元组
    }

for line in loc_data.itertuples():
    longitude = float(getattr(line, '经度'))
    latitude = float(getattr(line, '纬度'))

    data["nb_x"] = longitude
    data["nb_y"] = latitude
    data['b'] = "(" + str(longitude - 500) + "," + str(latitude - 200) + ";" \
                + str(longitude + 500) + "," + str(latitude + 200) + ")"

print(data)

header = {
    "method": "GET",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400",
    "accept-language": "zh-CN,zh;q=0.9"}

# 百度
uli = "https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=nb&r=1000"\
    "&l=19&gr_radius=1000&pn=0&device_ratio=1&da_src=shareurl&tn=B_NORMAL_MAP"\
    "&nn=0&ie=utf-8&newfrom=zhuzhan_webmap"

response = requests.get(uli, headers = header, params = data)
# response = requests.get(uli, headers=header)
print(response.status_code)
res_json = response.json()

res_list = res_json['content'] # 选项列表
options_dict = {} # 选项字典

if res_list:
    for index, line in enumerate(res_list):
        if line:
            name = line['name'] # 名称
            address = line['address_norm'] # 地址
            distance = line['dis'] # 距离
            options_dict[index] = [name, address, distance]
        else:
            continue

    print(options_dict)
else:
    print('没有值', res_json)