#encoding:utf-8
import requests, sys
import json
import datetime
import configparser

# 定数の定義
ZIP_API_URL = 'https://map.yahooapis.jp/search/zip/V1/zipCodeSearch'
API_URL = 'https://map.yahooapis.jp/weather/V1/place'
OUTPUT = 'json'

# 設定読み込み
inifile = configparser.ConfigParser()

# APIキー取得
inifile.read("../config.ini", "UTF-8") # gitと同期するフォルダから外しておく
API_ID = inifile.get("settings","yahooapikey")


if len(sys.argv) == 2:
    # 郵便番号から座標を検索
    zip_code = sys.argv[1]
    zip_url = ZIP_API_URL + "?appid=%s&query=%s&output=%s" % (API_ID,zip_code,OUTPUT)
    zip_resp = requests.get(zip_url)
    zip_resp = zip_resp.json()
    COORDINATES = zip_resp['Feature'][0]['Geometry']['Coordinates']
    ADDR = zip_resp['Feature'][0]['Property']['Address']

else:
    # 固定位置
    COORDINATES = '139.767097,35.681154'        # 東京駅

# GIT練習

RequestUrl = API_URL + '?appid={}&coordinates={}&output={}'.format(API_ID,COORDINATES,OUTPUT)

resp = requests.get(RequestUrl)

# 読み込んだJSONデータをディクショナリ型に変換
resp = resp.json()
print ('**************************')
# print (resp['Feature'][0]['Name'])
print ('{} の天気'.format(ADDR))
print ('**************************')

for forecast in resp['Feature'][0]['Property']['WeatherList']['Weather']:
    print ('**************************')
    ymd = forecast['Date']
    print ('{}/{}/{} {}:{} [{}]  雨量：{} mm'.format(ymd[0:4], ymd[4:6], ymd[6:8], ymd[8:10], ymd[10:12], forecast['Type'], forecast['Rainfall']))

print ('**************************')
