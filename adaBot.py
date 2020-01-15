import io #expects and produces str objects
import random
import string # to process standard python strings
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')
import nltk
from nltk.stem import WordNetLemmatizer
import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv
import requests
import json
import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()
name = '/Users/georginasanchez/repos/Ada/ada-robot/img/geomsb.jpeg'
picture = frame.copy()
cv2.imwrite(name, frame)

load_dotenv()

key = os.getenv("SPEECH_KEY")
region = os.getenv("SERVICE_REGION")
subscription_key = os.getenv("SUBSCRIPTION_KEY")

speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)


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
print(info[0]["faceAttributes"])

# Creates a speech synthesizer using the default speaker as audio output.
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)


def create_response(user_response, text):
    with open(text,'r', encoding='utf8', errors ='ignore') as adaInfo:
        adaText = adaInfo.read().lower()

    #Tokens
    sent_tokens = nltk.sent_tokenize(adaText)# converts to list of sentences
    lemmer = WordNetLemmatizer()

    def lem_tokens(tokens):
        return [lemmer.lemmatize(token) for token in tokens] #list comprenhension

    # remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation) #generator expresion
    remove_punct_dict = { ord(punct): None for punct in string.punctuation }

    def lem_normalize(text):
        return lem_tokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict))) #lowercase, remove punctuation, create tokens, and lemmatize

    # Generating response
    def response(user_response):
        ada_response=''
        sent_tokens.append(user_response) #push the response to the list
        TfidfVec = TfidfVectorizer(tokenizer=lem_normalize, stop_words='english') #it eliminates stop words
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx=vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if(req_tfidf==0):
            ada_response = ada_response + "I am sorry! I can't help you with that question try to ask me about the mission, inclusivity, Jump Start, etc."
            sent_tokens.remove(user_response)
            return (idx, ada_response)
        else:
            ada_response = ada_response + sent_tokens[idx]
            sent_tokens.remove(user_response)
            return (idx, ada_response)
    return response(user_response)

i=True
result = speech_synthesizer.speak_text_async("My name is AdaRobot and my pronouns are she and her. I will answer your questions about Ada Developers Academy. If you want to exit, say thanks or thank you").get()
while(i==True):
    user_input = speech_recognizer.recognize_once()
    user_response = user_input.text
    user_response = user_response.lower()
    print(user_response)
    if(user_response!='bye.'):
        if(user_response=='thanks.' or user_response=='thank you.'):
            i=False
            result = speech_synthesizer.speak_text_async("You are welcome! Thanks for comming to our presentation and for supporting Ada Developers Academy!").get()
        elif (user_response.split(',')=='how old am i?'):
            result = speech_synthesizer.speak_text_async("you look like" + str(round(info[0]["faceAttributes"]["age"])) + "you look very young!").get()
        else:
            idx, response_text = create_response(user_response, 'adaInfo.txt')
            # Synthesizes the received text to speech.
            # The synthesized speech is expected to be heard on the speaker with this line executed.
            speech_synthesizer.speak_text_async(response_text).get()

    else:
        i=False
        result = speech_synthesizer.speak_text_async("Bye! Thanks for comming to our presentation and for supporting Ada Developers Academy!").get()
        
