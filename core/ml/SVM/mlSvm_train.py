import os

from core.ml.SVM.settings.settings import EXTRACCION_IT, MODELS_DEST_FOLDER
from core.ml.SVM.controller.neural_network_orquestador import NeuralOrquestador
from core.ml.SVM.helper.general_helper import check_file_and_dest_folder
from core.ml.SVM.model.neural_network import Neural_Network
from core.ml.SVM.model.pandas_df import PandasDF


class MLsvmTrain(object):
    _pandas_df = None
    _neural_orch = None
    _logger = None

    def __init__(self, **kw):
        self.pandas_df = PandasDF()
        self.neural_network = Neural_Network()

        self.neural_orch = NeuralOrquestador(
            **{'pandas_instance': self.pandas_df,
               'neural_network_instance': self.neural_network,
               'load_models': False, 'show_graph': True})


    def train(self, inputfile, mlpath):

        if not check_file_and_dest_folder(inputfile, mlpath):
            raise ValueError('{} -> error en los param de entrada de train  '.format(__class__.__name__))

        try:
            self.neural_orch.pandas_df.src = inputfile
            self.neural_orch.neural_network.model_dest_path = mlpath
            self.neural_orch.do_pandas_job()
            self.neural_orch.do_neural_network_job()
            self.neural_orch.test_predict()
        except Exception as e:
            print("Error en el training de los modelos ")


    # <editor-fold desc="Setters / Getters">

    @property
    def mlpath(self):
        return self._mlpath

    @mlpath.setter
    def mlpath(self, value):
        if value and os.path.exists(value) and os.path.isdir(value):
            self._mlpath = value

    @property
    def pandas_df(self):
        return self._pandas_df

    @pandas_df.setter
    def pandas_df(self, value):
        if value and isinstance(value, PandasDF):
            self._pandas_df = value

    @property
    def neural_orch(self):
        return self._neural_orch

    @neural_orch.setter
    def neural_orch(self, value):
        if value and isinstance(value, NeuralOrquestador):
            self._neural_orch = value

    # </editor-fold>


if __name__ == '__main__':
    print ("EXTRACCION_IT -> {}".formta(EXTRACCION_IT))
    trainer = MLsvmTrain()
    trainer.train(EXTRACCION_IT, MODELS_DEST_FOLDER)
