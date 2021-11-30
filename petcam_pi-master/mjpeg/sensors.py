from gpiozero import MotionSensor, LED
import requests
import json

pir = MotionSensor(12)
led = LED(19)

def send_talk(message):
        talk_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        with open("access_token.txt", "r") as f:
            token = f.read()
        header = {"Authorization": f"Bearer {token}"}
        
        feed_template = {
            'object_type': 'feed',
          
            "content": {
            "title": "움직임이 감지되었습니다",
            "image_url": "https://images.ctfassets.net/cnu0m8re1exe/1GxSYi0mQSp9xJ5svaWkVO/d151a93af61918c234c3049e0d6393e1/93347270_cat-1151519_1280.jpg?fm=jpg&fl=progressive&w=660&h=433&fit=fill",
            #"image_width": 1024,
            #"image_height": 1024,
            "link": {
            # "web_url": "http://192.168.0.50:8000/mjpeg?mode=stream",
            # "mobile_web_url": "http://192.168.0.50:8000/mjpeg?mode=stream",
            # "web_url": "http://www.google.com/",
            # "mobile_web_url": "http://www.google.com/",
            "web_url": "http://192.168.219.150:8080/",
            "mobile_web_url": "http://192.168.219.150:8080/",
            }
            },


           
            'button_title' : '카메라 보기'
            
        }
        
        # payload = {'template_object': json.dumps(text_template)}
        payload = {'template_object': json.dumps(feed_template)}
        res = requests.post(talk_url, data=payload, headers=header)
        return res

def detect():
    led.on()
    #카톡메시지 보내기
    send_talk('움직임이 감지되었습니다!')

pir.when_motion = detect
pir.when_no_motion = led.off