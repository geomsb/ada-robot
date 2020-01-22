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
from miscQuestions import misc_question
import sys, time
from adaLed import white_on, all_off, blue_on, magenta_on, green_on
from idxResp import idx_ans
load_dotenv()

key = os.getenv("SPEECH_KEY")
region = os.getenv("SERVICE_REGION")

speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

# Creates a speech synthesizer using the default speaker as audio output.
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

def error_handler():
    green_on()
    speech_synthesizer.speak_text_async("I am sorry! I can't help you with that question. Try to ask me about the mission, inclusivity, Jump Start, etc.")
    all_off()

def ada_response():
    idx, response_text = create_response(user_response, 'adaInfo.txt')
    if (idx == 0):
        speech_synthesizer.speak_text_async(idx_ans[0])
    elif (idx == 1):
        speech_synthesizer.speak_text_async(idx_ans[1]) 
    elif (idx == 2):
        speech_synthesizer.speak_text_async(idx_ans[2])
    elif (idx == 3):
        speech_synthesizer.speak_text_async(idx_ans[3])
    elif (idx == 4):
        speech_synthesizer.speak_text_async(idx_ans[4])
    elif (idx == 5):
        speech_synthesizer.speak_text_async(idx_ans[5])
    elif (idx == 6):
        speech_synthesizer.speak_text_async(idx_ans[6])
    elif (idx == 7):
        speech_synthesizer.speak_text_async(idx_ans[7])
    elif (idx == 8):
        speech_synthesizer.speak_text_async(idx_ans[8])
    elif (idx == 9):
        speech_synthesizer.speak_text_async(idx_ans[9])
    elif (idx == 10):
        speech_synthesizer.speak_text_async(idx_ans[10])
    elif (idx == 11):
        speech_synthesizer.speak_text_async(idx_ans[11])
    elif (idx == 12):
        speech_synthesizer.speak_text_async(idx_ans[12])
    else:
        error_handler()

def non_ada_response():
    idx, response_text = create_response(user_response, 'userQuestions.txt')
    if(idx != -1):
        white_on()
        take_picture()
        info = process_picture()
        print(info)
        all_off()
    if(idx == 0):
        if (info == []):
            error_handler()
        else:
            speech_synthesizer.speak_text_async("you look like" + str(round(info[0]["faceAttributes"]["age"])) + ", you look very young!").get()
    elif(idx == 1):
        if (info == []):
            error_handler()
        elif(info[0]["faceAttributes"]["makeup"]["eyeMakeup"] == True) and info[0]["faceAttributes"]["makeup"]["eyeMakeup"] == True:
            speech_synthesizer.speak_text_async("your eye makeup and lipstick are lovely!")
        elif(info[0]["faceAttributes"]["makeup"]["lipMakeup"] == False) and (info[0]["faceAttributes"]["makeup"]["eyeMakeup"] == False):
            speech_synthesizer.speak_text_async("it seems that you are not wearing makeup!")
        elif(info[0]["faceAttributes"]["makeup"]["eyeMakeup"] == True):
            speech_synthesizer.speak_text_async("your eye makeup is wonderful!")
        elif(info[0]["faceAttributes"]["makeup"]["eyeMakeup"] == False):
            speech_synthesizer.speak_text_async("it seems that you are not wearing makeup!")    
        elif(info[0]["faceAttributes"]["makeup"]["lipMakeup"] == True):
            speech_synthesizer.speak_text_async("your lipstick color is beautiful!")
        elif(info[0]["faceAttributes"]["makeup"]["eyeMakeup"] == False):
            speech_synthesizer.speak_text_async("it seems that you are not wearing makeup!")
    elif(idx == 2):
        if (info == []):
            error_handler()
        elif(not info[0]["faceAttributes"]["accessories"]):
            speech_synthesizer.speak_text_async("it seems that you are not wearing accessories").get()
        elif(info[0]["faceAttributes"]["accessories"][0]["type"] == "headwear"):
            speech_synthesizer.speak_text_async("your " + str(info[0]["faceAttributes"]["accessories"][0]["type"]) + " is so cool!").get()
        elif(info[0]["faceAttributes"]["accessories"][0]["type"] == "glasses"):
            speech_synthesizer.speak_text_async("your " + str(info[0]["faceAttributes"]["accessories"][0]["type"]) + " are so cool!").get()
    elif(idx == 3):
        if (info == []):
            error_handler()
        else:
            max_emotion = Keymax = max(info[0]["faceAttributes"]["emotion"], key=info[0]["faceAttributes"]["emotion"].get)
            emotions = { "anger": "angry","contempt": "contempty", "disgust": "disgusty","fear": "scared", "happiness": "happy", "neutral": "neutral", "sadness": "sad", "surprise": "surprised"} 
            speech_synthesizer.speak_text_async("you are " + emotions[max_emotion]).get()
    else:
        answer = misc_question(user_response)
        if (answer == []):
            error_handler()
        else:
            speech_synthesizer.speak_text_async(answer).get()

def general_response():
    idx, response_text = create_response(user_response, 'adaInfo.txt')
    if(idx == -1):
        non_ada_response()
    else:
        ada_response()

i=True
all_off()
blue_on()
result = speech_synthesizer.speak_text_async("My name is AdaRobot and my pronouns are she and her. I will try to answer your questions about Ada Developers Academy or any other topic. I can also see you, so you can ask me about your age, accessories, and feelings. If you want to exit, say thanks or thank you").get()
all_off()
while(i==True):
    magenta_on()
    user_input = speech_recognizer.recognize_once()
    user_response = user_input.text.lower()
    all_off()
    print(user_response)
    if(user_response!='bye.'):
        if(user_response=='thanks.' or user_response=='thank you.'):
            i=False
            blue_on()
            speech_synthesizer.speak_text_async("You are welcome! Thanks for comming to our presentation and for supporting Ada Developers Academy!").get()
            all_off()
        elif(user_response==''):
            green_on()
            speech_synthesizer.speak_text_async("I am sorry! I could not hear you! Try to ask me about the mission, inclusivity, Jump Start, etc.")
            all_off()
        else:
            blue_on()
            general_response()
            all_off()
    else:
        i=False
        blue_on()
        result = speech_synthesizer.speak_text_async("Bye! Thanks for comming to our presentation and for supporting Ada Developers Academy!").get()
        all_off()
