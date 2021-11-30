import requests as req
import os
url= 'http://192.168.0.11:8000/api/snapshot/'
file_name = 'com.jpg'
file_path = os.path.join('.', 'com.jpg')
data = {
    'size': os.path.getsize('com.jpg'),
    'filename': file_name,
    'content_type': 'image/jpeg'
}
res = req.post(url, data=data, files={'image_file': open(file_path, 'br')})
if res.status_code == 200:
    print(res.json())
else:
    print(res.text)
