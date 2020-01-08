## Pre-requisites
### Installation of Python
```
$ brew install python
```

**NLTK (Natural Language Toolkit)**

NLTK was a platform used to create Ada Robot. It provides a lot of text processing libraries that helped with the tokenization, lemmatization, etc.

### Installation of NLTK
```
pip install nltk
```

### Instalation of NumPy
NumPy is the fundamental package for scientific computing with Python.

```
python3 -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
```

### Instalation of Scikit-learn
Scikit-learn is a Python module for machine learning.
```
pip install -U scikit-learn
```

### Instalation of Azure Cognitive Services
Ada Robot uses the Text to Speech and Speech to text Azure Services.
```
pip install --upgrade azure-cognitiveservices-speech
```

### Get a key from the Azure Cognitive Services
1. You need to create an Azure account.
1. You should get a key in order to use the Azure API.
1. You can try the service for 30 days.

https://azure.microsoft.com/en-us/free/

### Installing required packages
After NLTK has been downloaded, install required packages
```
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading popular packages
nltk.download('punkt') 
nltk.download('wordnet') 
```