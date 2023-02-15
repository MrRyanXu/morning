from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://apis.juhe.cn/simpleWeather/query?key=fc2734eed55956fcb86ed3a43bd86212&city=" + city
  response = requests.get(url)
  data = json.loads(response.text)
  if data['error_code'] == 0:
    city = data['city']
    current_temp = data['realtime']['temperature']
    current_humidity = data['realtime']['humidity']
    current_weather = data['realtime']['info']
    current_wind_direction = data['realtime']['direct']
    current_wind_power = data['realtime']['power']
    current_aqi = data['realtime']['aqi']

    print(f"{city}在2023年2月15日的天气情况是：")
    print(f"当前温度：{current_temp}°C")
    print(f"当前湿度：{current_humidity}%")
    print(f"当前天气：{current_weather}")
    print(f"风向和风力：{current_wind_direction}，{current_wind_power}")
    print(f"空气质量指数（AQI）：{current_aqi}")
else:
    print("数据获取失败。")

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
