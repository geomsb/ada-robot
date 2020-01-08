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
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

key = os.getenv("SPEECH_KEY")
region = os.getenv("SERVICE_REGION")

speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

with open('adaInfo.txt','r', encoding='utf8', errors ='ignore') as adaInfo:
    adaText = adaInfo.read().lower()

#Tokens
sent_tokens = nltk.sent_tokenize(adaText)# converts to list of sentences 
lemmer = WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens] #list comprenhension

# remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation) #generator expresion
remove_punct_dict = { ord(punct): None for punct in string.punctuation }

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict))) #lowercase, remove punctuation, create tokens, and lemmatize

# Creates a speech synthesizer using the default speaker as audio output.
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# Keyword Matching
GREETING_INPUTS = ("hello.", "hi.", "greetings.", "sup.", "what's up.","hey.",)
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

# Generating response
def response(user_response):
    ada_response=''
    sent_tokens.append(user_response) #push the response to the list
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english') #it eliminates stop words
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        ada_response = ada_response + "I am sorry! I don't understand you"
        # Synthesizes the received text to speech.
        # The synthesized speech is expected to be heard on the speaker with this line executed.
        return speech_synthesizer.speak_text_async(ada_response + "I am sorry! I don't understand you").get()
    else:
        ada_response = ada_response + sent_tokens[idx]
        # Synthesizes the received text to speech.
        # The synthesized speech is expected to be heard on the speaker with this line executed.
        return speech_synthesizer.speak_text_async(ada_response).get()

i=True
result = speech_synthesizer.speak_text_async("My name is AdaRobot and my pronouns are she and her. I will answer your questions about Ada Developers Academy. If you want to exit, say thanks or thank you").get()
while(i==True):
    user_input = speech_recognizer.recognize_once()
    user_response = user_input.text
    user_response = user_response.lower()
    if(user_response!='bye.'):
        if(user_response=='thanks.' or user_response=='thank you.'):
            i=False
            result = speech_synthesizer.speak_text_async("You are welcome! Thanks for comming to our presentation and for supporting Ada Developers Academy!").get()
        else:
            if(greeting(user_response)!=None):
                result = speech_synthesizer.speak_text_async(greeting(user_response)).get()
            else:
                response(user_response)
                sent_tokens.remove(user_response)
    else:
        i=False
        result = speech_synthesizer.speak_text_async("Bye! Thanks for comming to our presentation and for supporting Ada Developers Academy!").get()
        
