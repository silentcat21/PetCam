from gpiozero import MotionSensor, LED
from signal import pause
from datetime import datetime
from picamera import PiCamera,camera
import requests as req
import os
from subprocess import call

camera =PiCamera()
camera.resolution =(640, 480)


pir = MotionSensor(12)

video_url= 'http://192.168.0.6:8000/api/video/'
snapshot_url= 'http://192.168.0.6:8000/api/snapshot/'

led =LED(19)
start = 0

username ='hong'
video_path = ''

def capture():
    now =datetime.now()
    file_name =now.strftime('%Y%m%d_%H%M%S.jpg')
    file_path =os.path.join('./images', file_name)
    camera.capture(file_path, use_video_port=True)
    print('capture.....', file_path)
    return file_name, file_path

def upload(url, username, field, file_path, content_type):
    file_name= file_path.split('/')[-1]
    data = {
        'username': username,
        'size': os.path.getsize(file_path),
        'filename': file_name,
        'content_type': content_type     
    }
    res = req.post(url, data=data, files={field: open(file_path,'br')})

    if res.status_code ==200:
        print(res.json())
    else:
        print(res.text)

def convert(src, dst):
    command =f"MP4Box -add {src} {dst}"
    call([command], shell=True)

def start_record():
    global video_path, start
    
    led.on()

    file_name, file_path =capture()
    upload(snapshot_url,username,'image_file', file_path, 'image/jpeg')

    #녹화시작
    start =datetime.now()
    file_name = file_name.replace('.jpg','.h264')
    video_path =os.path.join('./videos',file_name)
    camera.start_recording(video_path)
    print('녹화시작',video_path)

def stop_record():
    #카메라 녹화 중지
    led.off()
    delta = datetime.now() - start
    print('녹화중지(녹화시간)', delta)
    camera.stop_recording()

    #비디오 파일 변환 및 업로드
    mp4_file_path = video_path.replace('h264','mp4')
    convert(video_path,mp4_file_path)
    os.remove(video_path) #.h264 파일 삭제
    
    upload(video_url,username,'video_file', mp4_file_path, 'video/mp4')

pir.when_motion = start_record
pir.when_no_motion = stop_record

pause()
