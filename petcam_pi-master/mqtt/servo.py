from gpiozero import AngularServo
from time import sleep
import paho.mqtt.client as mqtt

servo = AngularServo(14, min_angle=-90, max_angle=90, min_pulse_width=0.00045, max_pulse_width=0.0023)

def on_connect(client, userdate, flags, rc):
    print("connected with result code"+str(rc))
    if rc == 0:
        client.subscribe("control/camera")
    else:
        print('연결 실패:' ,rc)

def on_message(client, userdate, msg):
    value = -int(msg.payload.decode())
    print(f"{msg.topic} {value}")
    servo.angle = value #서보모터 각도 조절
    


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect("192.168.219.150")
    client.loop_forever()
except Exception as err:
    print('에러: %s'%err)