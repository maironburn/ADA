import os
import json
import pandas as pd
from nltk.corpus import stopwords
from sklearn.preprocessing import LabelEncoder



def datos_model_fit_transform(datos_model, cat):
    encoder = LabelEncoder()
    cleaned_values = list(map(lambda x: x.strip(), datos_model.eval(cat).values))
    datos_model[cat] = encoder.fit_transform(cleaned_values)
    name_mapping = dict(zip(encoder.classes_, encoder.transform(encoder.classes_)))
    return pd.DataFrame.from_dict(name_mapping, orient='index')


# @todo, tbd...chapu temporal
def stop_words():
    return [w.encode('utf-8') for w in stopwords.words('spanish')]


def check_folder(path):
    return os.path.exists(path) and os.path.isdir(path)


def load_json_id_cat(json_file):
    with open(json_file) as jf:
        data = json.load(jf)

    return data

def check_file_and_dest_folder(pandas_src, model_dir):

    return os.path.exists(pandas_src) and os.path.isfile(pandas_src) and os.path.exists(
        model_dir) and os.path.isdir(model_dir)

# class StemmedCountVectorizer(CountVectorizer):
#
#     def __init__(self):
#         stemmer_spanish = SnowballStemmer('spanish')
#     def build_analyzer(self):
#         analyzer = super(StemmedCountVectorizer, self).build_analyzer()
#         return lambda doc: ([self.stemmer_spanish.stem(w) for w in analyzer(doc)])
#


#
# if __name__ == "__main__":
#     vectorizer_s = StemmedCountVectorizer(min_df=3, analyzer="word", stop_words='spanish')
#
#
#
