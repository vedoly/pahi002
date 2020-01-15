from flask import Flask, request, abort
import requests
import json
import random
from project.Config import *
from uncleengineer import thaistock

app = Flask(__name__)
chat_state=[0]
ans=[3]

Q1=["กุ๊งกิ๊งกิ๊ง","กุ๊งกิ๊งกุ๊งกิ๊ง","กุ๊งกุ๊งกิ๊งกิ๊งกิ๊ง","กุ๊งกุ๊งกุ๊งกุ๊ง","กุ๊งกุ๊งกุ๊งกิ๊ง","กิ๊งกิ๊งกิ๊งกิ๊ง"]
Q1_follow=["","","เท่าไหร่","มีเท่าไหร่","ทั้งหมดเท่าไหร่","มีทั้งหมดเท่าไหร่"]

def GET_BTC_PRICE():
    data = requests.get('https://bx.in.th/api/')
    BTC_PRICE = data.text.split('BTC')[1].split('last_price":')[1].split(',"volume_24hours')[0]
    return BTC_PRICE




@app.route('/webhook', methods=['POST','GET'])
def webhook():
    if request.method == 'POST':
        payload = request.json

        Reply_token = payload['events'][0]['replyToken']
        print(payload)
        print(Reply_token)
        message = payload['events'][0]['message']['text']
        print(message)
       
        if chat_state[0] == 0:
            ReplyMessage(Reply_token,"กุ้งกิ๊งกุ๊งกิ๊ง มีเท่าไหร่",Channel_access_token)
            chat_state[0] = 1
       
        elif chat_state[0] == 1:
            if int(message) == ans[0] :
                Reply_messasge = "ถูกต้องงงง พร้อมสำหรับข้อต่อไปหรือยัง"
                ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
                chat_state[0] = 2
            
                
            
            elif int(message) != ans[0] :
                Reply_messasge = "ผิดจ้า ลองตอบใหม่นะ"
                ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        
        elif chat_state[0] == 2:
            Reply_messasge,ans[0]=game()
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
            chat_state[0] = 1


        return request.json, 200

    elif request.method == 'GET' :
        return 'this is method GET!!!' , 200

    else:
        Reply_messasge = 'ราคา BITCOIN ขณะนี้ : {}'.format(GET_BTC_PRICE())

@app.route('/')
def hello():
    return 'hello world bok',200

def ReplyMessage(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token) ##ที่ยาวๆ
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }

    data = {
        "replyToken":Reply_token,
        "messages":[{
            "type":"text",
            "text":TextMessage
        }]
    }

    data = json.dumps(data) ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data) 
    return 200

def game():
    index1 = random.randint(0, 5)
    index2 = random.randint(2,5)
    
    return Q1[index1]+" "+Q1_follow[index2] , index2