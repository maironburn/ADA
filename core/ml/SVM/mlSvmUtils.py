from time import time
import os
from nltk.corpus import stopwords


class Mlsvmutils(object):

    def __init__(self):
        pass


    def lemmatize_text(self, text):
        from nltk.tokenize import word_tokenize
        import nltk

        w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
        lemmatizer = nltk.stem.WordNetLemmatizer()

        # output=[]
        # tokens=w_tokenizer.tokenize(text)

        # for w in tokens:
        #  t1= time()
        #  output.append(lemmatizer.lemmatize(w))
        #  print("time to lematize ", time()-t1, " tokens:", str(w))
        # return output

        return [lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(text)]

    def dummy_fun(self, doc):
        return doc


    # @todo, tbd...chapu temporal
    def stop_words(self):
        return [w.encode('utf-8') for w in stopwords.words('spanish')]

    def check_folder(self, path):
        return os.path.exists(path) and os.path.isdir(path)
