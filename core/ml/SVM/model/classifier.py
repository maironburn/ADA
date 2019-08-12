import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import chi2
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from core.ml.SVM.helper.general_helper import get_logger
from core.ml.SVM.helper.general_helper import stop_words
from core.ml.SVM.settings import RANDOM_STATE, TEST_SIZE


class Classifier(object):
    _logger = None
    _model = None
    _df = pd.DataFrame

    _X_train = None
    _X_test = None
    _y_train = None
    _y_test = None
    _indices_train = None
    _indices_test = None

    _features = None
    _labels = None

    def __init__(self, **kw):

        print ("Inicializado Classifier")

    def get_features_and_labels(self):
        '''
        halla los tf - idf
        :return:
        '''

        stopwords_my = stop_words()
        tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2),
                                stop_words=stopwords_my)

        self.features = tfidf.fit_transform(self.df.detalle).toarray()
        print ("features : {} | {}".format(self.features.shape[0], self.features.shape[1]))
        self.labels = self.df.category_id

    def train_test_split(self):
        '''
        Division del dataset en train/test
        :return:

        '''


        self.X_train, self.X_test, self.y_train, self.y_test, self.indices_train, self.indices_test = train_test_split(
            self.features, self.labels,
            self.df.index, test_size=TEST_SIZE,
            random_state=RANDOM_STATE)




    def naive_bayes_classifier(self, text):
        '''
        algoritmo / entrenamiento _ prediccion alternativo ~ accuracy svm
        :param df: dataframe
        :param text, texto descriptivo de una IT
        :return: nada , solo muestra en consola la clasificacion de la IT
        '''
        if text:

            X_train, X_test, y_train, y_test = train_test_split(self.df['detalle'], self.df['descripcion'],
                                                                random_state=0)
            count_vect = CountVectorizer()
            X_train_counts = count_vect.fit_transform(X_train)
            tfidf_transformer = TfidfTransformer()
            X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
            clf = MultinomialNB().fit(X_train_tfidf, y_train)
            predicted = clf.predict(count_vect.transform([text]))
            print(predicted)
            self._logger.info("naive_bayes_classifier: {} -> {}".format(text, predicted))

    def correlaciones_chi2(self, features, labels, tfidf, id_to_category):
        '''
        # distribucion de features mayoritarias por cada una de las categorias (palabras mas relevantes, mayor peso /freq)
        :param features:
        :param labels:
        :param tfidf:
        :param id_to_category:
        :param logger:
        :return:
        '''
        N = 2
        for category_id, descripcion in sorted(id_to_category.items()):
            features_chi2 = chi2(features, labels == category_id)
            indices = np.argsort(features_chi2[0])
            feature_names = np.array(tfidf.get_feature_names())[indices]
            unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
            bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
            self._logger.info("# '{}':".format(descripcion))
            self._logger.info("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
            self._logger.info("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))

    def show_linear_svc(self, category_id_df):
        '''
        muestra la grafica heatmap a partir de la confusion_matrix
        :param features:
        :param labels:
        :param df:
        :param category_id_df:
        :return:
        '''
        model = LinearSVC()
        model.fit(self.X_train, self.y_train)
        y_pred = model.predict(self.X_test)
        conf_mat = confusion_matrix(self.y_test, y_pred)


    # <editor-fold desc="getters / setters">
    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, value):
        if isinstance(value, np.ndarray):
            self._features = value

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, value):
        if isinstance(value, pd.Series):
            self._labels = value

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        if value:
            self._model = value

    @property
    def X_train(self):
        return self._X_train

    @X_train.setter
    def X_train(self, value):
        if isinstance(value, np.ndarray):
            self._X_train = value

    @property
    def X_test(self):
        return self._X_test

    @X_test.setter
    def X_test(self, value):
        if isinstance(value, np.ndarray):
            self._X_test = value

    @property
    def y_train(self):
        return self._y_train

    @y_train.setter
    def y_train(self, value):
        if isinstance(value, pd.Series):
            self._y_train = value

    @property
    def y_test(self):
        return self._y_test

    @y_test.setter
    def y_test(self, value):
        if isinstance(value, pd.Series):
            self._y_test = value

    @property
    def indices_train(self):
        return self._indices_train

    @indices_train.setter
    def indices_train(self, value):
        if isinstance(value, pd.Int64Index):
            self._indices_train = value

    @property
    def indices_test(self):
        return self._indices_test

    @indices_test.setter
    def indices_test(self, value):
        if isinstance(value, pd.Int64Index):
            self._indices_test = value

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, value):
        if isinstance(value, pd.DataFrame) and not value.empty:
            self._df = value
    # </editor-fold>
