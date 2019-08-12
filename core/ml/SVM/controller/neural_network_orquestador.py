

from core.ml.SVM.model.neural_network import Neural_Network
from core.ml.SVM.model.pandas_df import PandasDF


class NeuralOrquestador(object):
    _pandas_df = None
    _neural_network = None
    _logger = None
    _json_id_cat = None
    _load_models = None


    def __init__(self, **kw):

        self.load_models = kw.get('load_models', False)

        if kw.get('neural_network_instance') and isinstance(kw.get('neural_network_instance'), Neural_Network):
            self._neural_network = kw.get('neural_network_instance')

            if kw.get('model_dest_path'):
                self.neural_network.model_dest_path = kw.get('model_dest_path')

        if kw.get('pandas_instance') and isinstance(kw.get('pandas_instance'), PandasDF):
            self._pandas_df = kw.get('pandas_instance')

    def do_pandas_job(self, describ_columns=False, limit_size=True):
        try:
            if self.pandas_df.load_data(describ_columns, limit_size):
                self.pandas_df.prepare_label_data()

        except Exception as e:
           pass

    def load_and_setup_neural_network(self):
        '''
        Preparado para la carga del clasificador y mlp a partir de dumps existentes
        ready to predict
        :return:
        '''

        self._neural_network.load_tf_idf()
        self.neural_network.load_neuronal_model()

    def test_predict(self):

        if self.load_models:
            dict_it = self.json_id_cat
        else:
            dict_it = self.pandas_df.id_to_category

        aciertos = 0
        # for i in range(0, 5000): self.pandas_df.df.shape[0]
        for i in range(0, 100):
            if self.neural_network.predict(dict_it=dict_it,  json_loaded=self.load_models):
                aciertos += 1

        print("Total aciertos: {}".format(aciertos))
        print("aciertos: {} /100 , accuracy {}".format(aciertos, (aciertos / 100) * 100))

    def do_neural_network_job(self):
        '''
        Se realiza el proceso completo
            carga de datos con panda ds
            fit transform / transform  Tf_IDF
            persistencia del Vectorizer y del MLP
        :return:
        '''
        try:

            self.neural_network.df = self.pandas_df.df
            self.neural_network.train_test_split()
            self.neural_network.train_model(self._pandas_df.category_id_df)


        except Exception as e:
            pass

    # <editor-fold desc="Setters / Getters">
    @property
    def pandas_df(self):
        return self._pandas_df

    @pandas_df.setter
    def pandas_df(self, value):
        if value and isinstance(value, PandasDF):
            self._pandas_df = value

    @property
    def neural_network(self):
        return self._neural_network

    @neural_network.setter
    def neural_network(self, value):
        if value and isinstance(value, Neural_Network):
            self._neural_network = value

    @property
    def json_id_cat(self):
        return self._json_id_cat

    @json_id_cat.setter
    def json_id_cat(self, value):
        if value:
            self._json_id_cat = value

    @property
    def load_models(self):
        return self._load_models

    @load_models.setter
    def load_models(self, value):
        if value:
            self._load_models = value



    # </editor-fold>
