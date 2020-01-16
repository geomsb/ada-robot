import io #expects and produces str objects
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
from chatBot import create_response
from pictureProcess import take_picture, process_picture

load_dotenv()

key = os.getenv("SPEECH_KEY")
region = os.getenv("SERVICE_REGION")

speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

# Creates a speech synthesizer using the default speaker as audio output.
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

i=True
result = speech_synthesizer.speak_text_async("My name is AdaRobot and my pronouns are she and her. I will answer your questions about Ada Developers Academy. If you want to exit, say thanks or thank you").get()
while(i==True):
    user_input = speech_recognizer.recognize_once()
    user_response = user_input.text.lower()
    print(user_response)
    if(user_response!='bye.'):
        if(user_response=='thanks.' or user_response=='thank you.'):
            i=False
            speech_synthesizer.speak_text_async("You are welcome! Thanks for comming to our presentation and for supporting Ada Developers Academy!").get()
        else:
            idx, response_text = create_response(user_response, 'adaInfo.txt')
            if(idx == -1):
                take_picture()
                info = process_picture()
                print(info)
                idx, response_text = create_response(user_response, 'userQuestions.txt')
                if(idx == 0):
                    speech_synthesizer.speak_text_async("you look like" + str(round(info[0]["faceAttributes"]["age"])) + "you look very young!").get()
                elif(idx == 1):
                  if(info[0]["faceAttributes"]["makeup"]["eyeMakeup"]) and info[0]["faceAttributes"]["makeup"]["eyeMakeup"]:
                      speech_synthesizer.speak_text_async("your eye makeup and lipstick are lovely!")
                  elif(info[0]["faceAttributes"]["makeup"]["eyeMakeup"]):
                      speech_synthesizer.speak_text_async("your eye makeup is wonderful!")
                  elif(info[0]["faceAttributes"]["makeup"]["lipstick"]):
                      speech_synthesizer.speak_text_async("your lipstick color is beautiful!")
                  else:
                      speech_synthesizer.speak_text_async("it seems that you are not wearing makeup!")
                elif (idx == 2):
                  if (info[0]["faceAttributes"]["accessories"]):
                      speech_synthesizer.speak_text_async("your " + str(info[0]["faceAttributes"]["accessories"][0]["type"]) + " are so cool!").get()
                  else:
                    speech_synthesizer.speak_text_async("I am sorry! I can't help you with that question. Try to ask me about the mission, inclusivity, Jump Start, etc.").get()
                elif (idx == 3):
                  max_emotion = Keymax = max(info[0]["faceAttributes"]["emotion"], key=info[0]["faceAttributes"]["emotion"].get)
                  emotions = { "anger": "angry","contempt": "contempty", "disgust": "disgusty","fear": "scared", "happiness": "happy", "neutral": "neutral", "sadness": "sad", "surprise": "surprised"} 
                  speech_synthesizer.speak_text_async("you are " + emotions[max_emotion]).get()
                else:
                  speech_synthesizer.speak_text_async("I am sorry! I can't help you with that question. Try to ask me about the mission, inclusivity, Jump Start, etc.").get()
            else:
                # Synthesizes the received text to speech.
                # The synthesized speech is expected to be heard on the speaker with this line executed.
                speech_synthesizer.speak_text_async(response_text).get()
    else:
        i=False
        result = speech_synthesizer.speak_text_async("Bye! Thanks for comming to our presentation and for supporting Ada Developers Academy!").get()
        
