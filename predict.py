# @todo from core.exceptions.customexceptions import ApiException
# @todo from django.conf import settings
# @todo from ApiADA.loggers import logging

import os

#from core.ml.SVM.settings.settings import MODELS_DEST_FOLDER
from common_config import MODELS_DEST_FOLDER
import pandas as pd
from core.ml.SVM.controller.neural_network_orquestador import NeuralOrquestador
from core.ml.SVM.helper.general_helper import check_folder, load_json_id_cat
from core.ml.SVM.model.neural_network import Neural_Network
from core.ml.SVM.model.pandas_df import PandasDF


# log = logging.getLogger(__name__)


class MLsvm(object):

    _neural_orch = None
    _logger = None
    _mlpath = None

    def __init__(self, mlpath):
        try:

            if check_folder(mlpath):

                self.mlpath = mlpath
                neural_network = Neural_Network()

                self.neural_orch = NeuralOrquestador(
                    **{'neural_network_instance': neural_network,
                       'load_models': True, 'model_dest_path': self.mlpath})

                self.neural_orch.load_and_setup_neural_network()

            else:
                raise ValueError(' -> {} directorio no valido'.format(mlpath))

        except Exception as e:
            pass
            # raise ApiException("Exception creating SVM object" + str(e))


    def predict(self, data = None):
        print ("dentro del metodo predict")
        self.neural_orch.json_id_cat = load_json_id_cat(os.path.join(self.mlpath, "json_id_cat.json"))
        tfidf= self.neural_orch.neural_network.tfidf
        mlp= self.neural_orch.neural_network.mlp

        train = pd.DataFrame.from_dict(data)
        it =tfidf.transform(train.detalle).toarray()
        prediction = mlp.predict(it)

        self.neural_orch.json_id_cat.get(str(prediction[0]))



    # <editor-fold desc="Setters / Getters">

    @property
    def mlpath(self):
        return self._mlpath

    @mlpath.setter
    def mlpath(self, value):
        if value and os.path.exists(value) and os.path.isdir(value):
            self._mlpath = value

    @property
    def neural_orch(self):
        return self._neural_orch

    @neural_orch.setter
    def neural_orch(self, value):
        if value and isinstance(value, NeuralOrquestador):
            self._neural_orch = value

    # </editor-fold>





if __name__ == '__main__':

    from common_config import data
    predictor = MLsvm(MODELS_DEST_FOLDER)
    predictor.predict(data)
