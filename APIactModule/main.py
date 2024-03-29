import json
import ntplib
import datetime
from time import ctime
import requests
import xmltodict
import difflib
import os

#----------------------------------------------------------------------------------#
#                                                                                  #
#                           API Action Module Version 1.4β                         #
#                                                                                  #
#----------------------------------------------------------------------------------#

#----------------------P2P地震情報----------------------#
class p2p_eq:
    def new_data():
        resp = "https://api.p2pquake.net/v2/history?codes=551&limit=1"
        js_l = requests.get(resp).json()
        hypocenter = js_l[0]["earthquake"]["hypocenter"]["name"]
        maxint = js_l[0]["earthquake"]["maxScale"]
        depth = js_l[0]["earthquake"]["hypocenter"]["depth"]
        magnitude = js_l[0]["earthquake"]["hypocenter"]["magnitude"]
        date = js_l[0]["earthquake"]["time"]
        type = js_l[0]["issue"]["type"]
        info = None
        shindo = None
        em_color = None
        match maxint:
            case -1:
                shindo = "不明"
            case 10:
                shindo = "1"
            case 20:
                shindo = "2"
            case 30:
                shindo = "3"
            case 40:
                shindo = "4"
            case 45:
                shindo = "5-"
            case 50:
                shindo = "5+"
            case 55:
                shindo = "6-"
            case 60:
                shindo = "6+"
            case 70:
                shindo = "7"
        match type:
            case "ScalePrompt":
                info = "震度速報"
            case "Destination":
                info = "震源に関する情報"
            case "ScaleAndDestination":
                info = "震源・震度に関する情報"
            case "DetailScale":
                info = "各地の震度に関する情報"
            case "Foreign":
                info = "遠地地震に関する情報"
            case _:
                info = "その他"
        data = {
            "type": info,
            "hypocenter": hypocenter,
            "maxInt": shindo,
            "magnitude": str(float(magnitude)),
            "depth": depth,
            "time": date
        }
        return data
    def history(offset=0):
        resp = "https://api.p2pquake.net/v2/jma/quake?limit=50&offset=1&quake_type=DetailScale"
        js_l = requests.get(resp).json()
        hypocenter = js_l[offset]["earthquake"]["hypocenter"]["name"]
        maxint = js_l[offset]["earthquake"]["maxScale"]
        depth = js_l[offset]["earthquake"]["hypocenter"]["depth"]
        magnitude = js_l[offset]["earthquake"]["hypocenter"]["magnitude"]
        date = js_l[offset]["earthquake"]["time"]
        type = js_l[offset]["issue"]["type"]
        info = None
        shindo = None
        em_color = None
        match maxint:
            case -1:
                shindo = "不明"
            case 10:
                shindo = "1"
            case 20:
                shindo = "2"
            case 30:
                shindo = "3"
            case 40:
                shindo = "4"
            case 45:
                shindo = "5-"
            case 50:
                shindo = "5+"
            case 55:
                shindo = "6-"
            case 60:
                shindo = "6+"
            case 70:
                shindo = "7"
        match type:
            case "ScalePrompt":
                info = "震度速報"
            case "Destination":
                info = "震源に関する情報"
            case "ScaleAndDestination":
                info = "震源・震度に関する情報"
            case "DetailScale":
                info = "各地の震度に関する情報"
            case "Foreign":
                info = "遠地地震に関する情報"
            case _:
                info = "その他"
        data = {
            "type": info,
            "hypocenter": hypocenter,
            "maxInt": shindo,
            "magnitude": str(float(magnitude)),
            "depth": depth,
            "time": date
        }
        return data
#----------------------NTP時刻取得----------------------#
def ntp_nict(kind="all"):
    match kind:
        case "all":
            timeformat = "%Y年%m月%d日 %H時%M分%S秒"
            datatype = "今日の日付と現在時刻"
        case "date":
            timeformat = "%Y年%m月%d日"
            datatype = "今日の日付"
        case "time":
            timeformat = "%H時%M分%S秒"
            datatype = "現在時刻"
        case "ex":
            timeformat= "%Y%m%d-%H%M%S"
            datatype = "ex"
    client = ntplib.NTPClient()
    res = client.request("ntp.nict.jp")
    nowtime = datetime.datetime.strptime(ctime(res.tx_time), "%a %b %d %H:%M:%S %Y")
    return nowtime.strftime(timeformat) ,datatype

#----------------------NHK地震情報震度分布画像取得----------------------#
def nhk_image():
    response = requests.get("https://www3.nhk.or.jp/sokuho/jishin/data/JishinReport.xml")
    response.encoding = 'shift_jis'
    JishinReport = json.loads(json.dumps(xmltodict.parse(response.text)))
    try:
        eq_url = (JishinReport['jishinReport']['record'][0]['item'][0]['@url'])
    except KeyError as e:
        eq_url = (JishinReport['jishinReport']['record'][0]['item']['@url'])
    response2 = requests.get(eq_url)
    response2.encoding = 'shift_jis'
    chiikibetsu = json.loads(json.dumps(xmltodict.parse(response2.text)))
    return f"https://www3.nhk.or.jp/sokuho/jishin/{chiikibetsu['Root']['Earthquake']['Detail']}"
#----------------------内容差分表示----------------------#
def sabun_txt(before,after,tex=None):
    date = ntp_nict("ex")
    diff = difflib.HtmlDiff()
    output_path = f"./edit-deleteLog/{date[0]}{tex}.htm"
    url = f"{date[0]}{tex}.htm"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(diff.make_file(before.split(),after.split()))

    data = difflib.ndiff(before.split(),after.split())  
    return url, data
#----------------------バージョン情報----------------------#
def version():
    return "APIactModule 1.4.6"