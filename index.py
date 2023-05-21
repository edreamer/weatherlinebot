import requests
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('8y8UFvvBgPWyCdLQUJJ53eeYQB9z5PMOSJXt5vSvedXBmO6mPRd3aFFMi/YL/tUGolkth7W80ZMkNXOGrryB4T0aryW9QAQzb3z4O/MFbWzopRocAXyY7X4tva+o1MXbloySdO3lq5ny2rGzBUM5EQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('476f5fd7e7855093a98ff4985ea587fb')

def getWeather(city):
    url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=CWB-A781924B-758D-474E-AC05-D5681DB85505&downloadType=WEB&format=JSON'
    data = requests.get(url)   # 取得 JSON 檔案的內容為文字
    data_json = data.json()    # 轉換成 JSON 格式
    locations = data_json['cwbopendata']['dataset']['location']
    
    for location in locations:
        if city.replace("台","臺") in location['locationName']:
            wx8 = location['weatherElement'][0]['time'][0]['parameter']['parameterName']    # 天氣現象
            maxt8 = location['weatherElement'][1]['time'][0]['parameter']['parameterName']  # 最高溫
            mint8 = location['weatherElement'][2]['time'][0]['parameter']['parameterName']  # 最低溫
            ci8 = location['weatherElement'][3]['time'][0]['parameter']['parameterName']    # 舒適度
            pop8 = location['weatherElement'][4]['time'][0]['parameter']['parameterName']   # 降雨機率
            
            cityname = location['locationName']
            msg = f'{cityname}\n'
            msg += f'{wx8}\n'            
            msg += f'最高溫 {maxt8} 度\n'
            msg += f'最低溫 {mint8} 度\n'
            msg += f'舒適度 {ci8}\n'
            msg += f'降雨機率 {pop8} %'
            break
    return msg


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = getWeather(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))


if __name__ == "__main__":
    app.run()
