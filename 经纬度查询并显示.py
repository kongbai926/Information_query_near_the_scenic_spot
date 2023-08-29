# 手机无法运行，上传到电脑运行
import requests
import re
import json
import folium
import webbrowser
def get_get_location_m(name):
    url = "https://restapi.amap.com/v3/place/text?s=rsv3" \
          "&children=&key=b1a5c61ed6fd006b6e5db7fce30e755f"\
          "&jscode=1c8a0dce1957438f8af72cc1e9c9fa8f&page=1" \
          "&offset=10&city=510100&language=zh_cn" \
          "&callback=jsonp_755735_" \
          "&platform=JS&logversion=2.0" \
          "&sdkversion=1.3" \
          "&appname=https%3A%2F%2Flbs.amap.com%2Fconsole%2Fshow%2Fpicker" \
          "&csid=F028E84F-6601-43AE-88A8-13425E3DE7C7" \
          "&keywords={}".format(name)
    res_text = requests.get(url).text
    if re.findall('"info":"OK"', res_text):
        res_data = json.loads(res_text.replace(re.findall("jsonp_\d+_\(", res_text)[0], "")[0:-1])["pois"][0]
        item = {}
        item["name"] = res_data["name"]
        item["type"] = res_data["type"]
        item["location"] = res_data["location"]
        item["pname"] = res_data["pname"]
        item["cityname"] = res_data["cityname"]
        item["adname"] = res_data["adname"]
        return item
    else:
        return None

def show_map_by_location(location, zoom_start=12):
    location = [float(location[1]), float(location[0])]
    map_osm = folium.Map(location=location,zoom_start=zoom_start,
tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}', attr='&copy; <a href="http://ditu.amap.com/">高德地图</a>"')

    # 标记一个实心圆
    folium.CircleMarker(
        location=tuple(location),
        radius=10,
        popup='popup',
        parse_html=True,
        tooltip="click here",
        color='#DC143C',  # 圈的颜色
        fill=True,
        fill_color='#6495ED'  # 填充颜色
    ).add_to(map_osm)
    map_osm.save('f1.html')
    webbrowser.open('f1.html')
##location_ = get_get_location_m("建设一路  武汉科技大学")['location']
##loca_list = list(localtion_.split(','))
###print(loca_list)
##show_map_by_location(loca_list)
