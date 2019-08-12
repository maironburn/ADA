import os

import numpy as np
import pandas as pd
from joblib import dump, load
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

from core.ml.SVM.helper.general_helper import stop_words
from core.ml.SVM.settings.settings import RANDOM_STATE, TEST_SIZE


class Neural_Network(object):
    _logger = None
    _df = pd.DataFrame
    _model_dest_path = None

    _mlp = None
    _tfidf = None
    _X_train = None
    _X_test = None
    _y_train = None
    _y_test = None
    _indices_train = None
    _indices_test = None

    def __init__(self, **kw):

        print ("Inicializado Neural_Network ")

        self.tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2),
                                     stop_words=stop_words())

    # <editor-fold desc="Load  / Save model/ classifier ">

    def load_tf_idf(self):
        '''
        Carga el TfidfVectorizer
        :return:
        '''
        try:

            dest_file = "{}{}{}.joblib".format(self.model_dest_path, os.path.sep, "tf_idf")
            self.tfidf = load(dest_file)

        except Exception as e:
            print ("Exception in load_tf_idf -> {}".format(e))

    def load_neuronal_model(self):
        '''
        Carga el MLPClassifier
        :return:
        '''
        try:
            dest_file = "{}{}{}.joblib".format(self.model_dest_path, os.path.sep, "neuronal_model")
            self.mlp = load(dest_file)

        except Exception as e:
            print ("Exception in load_neuronal_model -> {}".format(e))

    def save_neuronal_model(self):
        '''
        guarda MLPClassifier
        :return:
        '''
        try:

            dest_file = "{}{}{}.joblib".format(self.model_dest_path, os.path.sep, "neuronal_model")
            dump(self.mlp, dest_file)

        except Exception as e:
            print ("Exception in save_neuronal_model -> {}".format(e))

    def save_classifier(self):
        '''
        guarda TfidfVectorizer
        :return:
        '''
        try:

            dest_file = "{}{}{}.joblib".format(self.model_dest_path, os.path.sep, "tf_idf")
            dump(self.tfidf, dest_file)

        except Exception as e:
            print ("Exception in save_classifier -> {}".format(e))

    # </editor-fold>

    def train_test_split(self):
        '''
        Division del dataset en train/test
        aprendizaje de vocabulario
        generacion de los tf_idf para los tokens
        persiste TfidfVectorizer
        :return:

        '''

        tf_idf = self.tfidf.fit_transform(self.df.detalle)
        self.X_train, self.X_test, self.y_train, self.y_test, self.indices_train, self.indices_test = train_test_split(
            tf_idf.toarray(), self.df.category_id,
            self.df.index, test_size=TEST_SIZE,
            random_state=RANDOM_STATE)

        self.save_classifier()

        print (" -> train_test_split : muestras para train: {} , para test: {}".format(
            len(self.X_train),
            len(self.X_test)))

    def train_model(self, category_id_df, show_graph=False):

        '''

        :param category_id_df:
        :param show_graph: booleano para mostrar o no el heatmap de seaborn
        persiste el modelo de la red
        :return:
        '''
        self.mlp = MLPClassifier(activation='relu', alpha=0.0001, batch_size='auto', beta_1=0.9,
                                 beta_2=0.999, early_stopping=False, epsilon=1e-08,
                                 hidden_layer_sizes=(13, 13, 13), learning_rate='constant',
                                 learning_rate_init=0.001, max_iter=500, momentum=0.9,
                                 nesterovs_momentum=True, power_t=0.5,
                                 solver='adam', tol=0.0001, validation_fraction=0.1,
                                 verbose=False, warm_start=False)

        self.mlp.fit(self.X_train, self.y_train)
        self.save_neuronal_model()

        predictions = self.mlp.predict(self.X_test)
        print(metrics.classification_report(self.y_test, predictions))

    def predict(self, dict_it, json_loaded=False):

        try:
            cat_predicted = None
            datos = self.df.sample(1)
            it = self.tfidf.transform(datos.detalle).toarray()
            prediction = self.mlp.predict(it)

            if json_loaded:
                print("tipo de la it: {} - prediccion {}".format(datos.descripcion.values[0],
                                                                 dict_it[str(prediction[0])]))
                cat_predicted = dict_it[str(prediction[0])]
            else:
                cat_predicted = dict_it.get(prediction[0])
                print(
                    "tipo de la it: {} - prediccion {}".format(datos.descripcion.values[0], cat_predicted))

            if datos.descripcion.values[0] == cat_predicted:
                return True


        except Exception as e:
            print ("Exception in predict -> {}".format(e))

    # <editor-fold desc="Getters / Setters">

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        if value:
            self._logger = value

    @property
    def mlp(self):
        return self._mlp

    @mlp.setter
    def mlp(self, value):
        if value:
            self._mlp = value

    @property
    def tfidf(self):
        return self._tfidf

    @tfidf.setter
    def tfidf(self, value):
        if value:
            self._tfidf = value

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

    @property
    def model_dest_path(self):
        return self._model_dest_path

    @model_dest_path.setter
    def model_dest_path(self, value):
        if value:
            self._model_dest_path = value

    # </editor-fold>
