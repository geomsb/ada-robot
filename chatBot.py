import nltk
from nltk.stem import WordNetLemmatizer
import string 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
            ada_response = ada_response + "I am sorry! I can't help you with that question. Try to ask me about the mission, inclusivity, Jump Start, etc."
            sent_tokens.remove(user_response)
            return (-1, ada_response)
        else:
            ada_response = ada_response + sent_tokens[idx]
            sent_tokens.remove(user_response)
            return (idx, ada_response)
    return response(user_response)
