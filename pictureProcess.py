import cv2
from dotenv import load_dotenv
import requests
import os
import shutil

load_dotenv()

subscription_key = os.getenv("SUBSCRIPTION_KEY")

def take_picture():
    picture_api_url = 'http://georginapi:5000/picture'
    api_response = requests.get(picture_api_url, stream=True)
    with open('img/geomsb.jpeg', 'wb') as out_file:
        shutil.copyfileobj(api_response.raw, out_file)
    del api_response


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
