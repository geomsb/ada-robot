import cv2
from dotenv import load_dotenv
import requests
import os

load_dotenv()

subscription_key = os.getenv("SUBSCRIPTION_KEY")

def take_picture():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    name = '/Users/georginasanchez/repos/Ada/ada-robot/img/geomsb.jpeg'
    picture = frame.copy()
    cv2.imwrite(name, frame)

def process_picture():
    face_api_url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect'
    image_url = 'img/geomsb.jpeg'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    params = {
        'returnFaceAttributes': 'age,glasses,emotion,hair,makeup,accessories',
    }
    data = open('img/geomsb.jpeg', 'rb').read()
    api_response = requests.post(face_api_url, params=params,
                            headers=headers, data=data)
    info = api_response.json()
    return info
