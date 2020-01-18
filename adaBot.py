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

load_dotenv()

key = os.getenv("SPEECH_KEY")
region = os.getenv("SERVICE_REGION")

speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

# Creates a speech synthesizer using the default speaker as audio output.
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

def error_handler():
    speech_synthesizer.speak_text_async("I am sorry! I can't help you with that question. Try to ask me about the mission, inclusivity, Jump Start, etc.")

def ada_response():
    idx, response_text = create_response(user_response, 'adaInfo.txt')
    if (idx == 0):
        speech_synthesizer.speak_text_async("The mission of Ada Developers Academy is to diversify tech by providing women and gender diverse people the skills, experience, and community support to become professional software developers to change the face of tech, Ada Developers Academy is a non-profit, tuition-free coding school for women and gender diverse adults.")
    elif (idx == 1):
        speech_synthesizer.speak_text_async("The program combines classroom training and a paid learning internship to teach our students both how to write code (practical tools and computer science fundamentals) and how to be a software developer (leadership, inclusivity, and career).") 
    elif (idx == 2):
        speech_synthesizer.speak_text_async("Our inclusivity is showed on students, staff, volunteers, TA’s, and reps from our sponsor companies come to Ada Developers Academy with an incredible diversity of identity and experience.") 
    elif (idx == 3):
        speech_synthesizer.speak_text_async("Augusta Ada Lovelace was a 19th-century mathematician and she is considered the founder of computer science.")
    elif (idx == 4):
        speech_synthesizer.speak_text_async("The Jump Start Live is for students who need extra support and it starts one month before the classes start and the Jump Start Curriculum must be completed by our students prior to their first day at Ada the content covers foundational concepts such as the basics of coding languages and getting comfortable with tools.")
    elif (idx == 5):
        speech_synthesizer.speak_text_async("The classroom experience consists of 8 hours a day, 5 days a week for 24 weeks, the curriculum is divided up into one-week units, and each week features a project that reinforces that week’s learning objectives.")
    elif (idx == 6):
        speech_synthesizer.speak_text_async("A capstone project is created by or students in order to show what they have learned.")
    elif (idx == 7):
        speech_synthesizer.speak_text_async("The advocacy of the program includes workshops focused on justice, bias intervention, and inclusive community therefore our Adies are not only trained to be strong developers but also strong advocates.")
    elif (idx == 8):
        speech_synthesizer.speak_text_async("The internship will be performed during the second part of the course, students will participate in an interview week where they will interview with six companies and they will be placed with one of the companies.")
    elif (idx == 9):
        speech_synthesizer.speak_text_async("You can apply if you have permanent work authorization in the United States and if you are able to participate for the full duration of the program, which is full-time, Monday through Friday.")
    elif (idx == 10):
        speech_synthesizer.speak_text_async("The application window opens approximately six months prior to the start of the cohort for about a three-week duration, it includes 4 parts: online application, code challenge, technical interview, and in-person/virtual interview, all phases after the application are by invitation only.")
    elif (idx == 11):
        speech_synthesizer.speak_text_async("There is financial support for students who need assistance covering their living expenses during the Ada lectures portion, we offer a low-interest loan through our lending partner, Craft3.")
    elif (idx == 12):
        speech_synthesizer.speak_text_async("You can donate at the website or by mail, please make checks payable to TSNE/Ada Developers Academy Mailing address: Third Sector New England, Inc. ATTN: Ada Developers Academy 89 South Street, Suite 700 Boston, MA 02111-2670.")
    else:
        error_handler()

def non_ada_response():
    idx, response_text = create_response(user_response, 'userQuestions.txt')
    if(idx != -1):
        take_picture()
        info = process_picture()
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
        elif(info[0]["faceAttributes"]["makeup"]["eyeMakeup"] == True):
            speech_synthesizer.speak_text_async("your eye makeup is wonderful!")
        elif(info[0]["faceAttributes"]["makeup"]["lipMakeup"] == True):
            speech_synthesizer.speak_text_async("your lipstick color is beautiful!")
        else:
            speech_synthesizer.speak_text_async("it seems that you are not wearing makeup!")
    elif(idx == 2):
        if (info == []):
            error_handler()
        elif(info[0]["faceAttributes"]["accessories"]):
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
result = speech_synthesizer.speak_text_async("My name is AdaRobot and my pronouns are she and her. I will try to answer your questions about Ada Developers Academy or any other topic. I can also see you, so you can ask me about your age, accessories, and feelings. If you want to exit, say thanks or thank you").get()
while(i==True):
    user_input = speech_recognizer.recognize_once()
    user_response = user_input.text.lower()
    print(user_response)
    if(user_response!='bye.'):
        if(user_response=='thanks.' or user_response=='thank you.'):
            i=False
            speech_synthesizer.speak_text_async("You are welcome! Thanks for comming to our presentation and for supporting Ada Developers Academy!").get()
        else:
            general_response() 
    else:
        i=False
        result = speech_synthesizer.speak_text_async("Bye! Thanks for comming to our presentation and for supporting Ada Developers Academy!").get()
        
