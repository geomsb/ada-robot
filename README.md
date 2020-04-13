# Ada Robot

I created this project to learn about chatbots, Microsoft Azure cognitive services API, Wolframalpha API and how to use the Raspberry Pi.

## Feature Set

1.  Ada robot can chat with you.
1.  Ada robot can hear you.
1.  Ada robot can talk to you.
1.  Ada robot can see you and take a picture.
1.  Ada robot can tell you your emotions.
1.  Ada robot can tell you about your accessories.
1.  Ada robot can tell you about your makeup.
1.  Ada robot turn on a LED with a specific color depending on the following:
      When she talks the LED will be blue.
      When she hears the LED will be magenta.
      When she does not know the answer the LED will be green.
1.  Ada robot has a 3D printed face.

## Technology Choices

- Raspberry Pi
- Python
- Azure cognitive services API
  - Azure face API
  - Azure text to speech API
  - Azure speech to text API
- Wolframalpha API
- Flask

## Pre-requisites
### Installation of Python
```
brew install python
```

**NLTK (Natural Language Toolkit)**

NLTK was a platform used to create Ada Robot. It provides a lot of text processing libraries that helped with the tokenization, lemmatization, etc.

### Installation of NLTK
```
pip3 install nltk
```

### Installation of NumPy
NumPy is the fundamental package for scientific computing with Python.

```
pip3 install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
```

### Installation of Scikit-learn
Scikit-learn is a Python module for machine learning.
```
pip3 install -U scikit-learn
```

### Installation of Azure Cognitive Services
Ada Robot uses the Text to Speech and Speech to text Azure Services.
```
pip3 install --upgrade azure-cognitiveservices-speech
```

### Get a key from the Azure Cognitive Services
1. You need to create an Azure account.
1. You should get a key in order to use the Azure API.
1. You can try the service for 30 days.

https://azure.microsoft.com/en-us/free/

### Installation of Requests
Requests allows you to send organic, grass-fed HTTP/1.1 requests, without the need for manual labor. There's no need to manually add query strings to your URLs, or to form-encode your POST data. 
```
pip3 install requests
```

### Installation of OpenCV
Ada robot uses this library in the Raspberry Pi to capture an image from the webcam.
```
sudo apt install python3-opencv
```

### Installation of Flask
Flask is a lightweight WSGI web application framework. Ada robot uses Flask in the Raspberry Pi to host a web server in order to turn on/off the led and take the picture.
```
pip3 install Flask
```

### Installation of Wolframalpha
Ada robot uses this library to answer questions if it does not find them with the chatbot process.
```
pip3 install wolframalpha
```

### Installation of required packages
After NLTK has been downloaded, install required packages
```python
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading popular packages
nltk.download('punkt') 
nltk.download('wordnet') 
```
