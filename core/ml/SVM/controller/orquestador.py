
import pandas as pd
from core.ml.SVM.settings.settings import EXTRACCION_IT
from core.ml.SVM.model.pandas_df import PandasDF
from core.ml.SVM.model.classifier import Classifier
from core.ml.SVM.helper.general_helper import get_logger



class Orquestador(object):
    _pandas_df = None
    _classifier = None
    _logger = None

    def __init__(self, **kw):

        print("Iniciado el Orquestador")
        if isinstance(kw.get('pandas_instance'), PandasDF) and isinstance(kw.get('classifier_instance'), Classifier):
            self._pandas_df = kw.get('pandas_instance')
            self._classifier = kw.get('classifier_instance')
            self.panda_ds.src = EXTRACCION_IT if not kw.get('src', None) else kw.get('src')
            self.do_pandas_job()
            self.do_classifier_job()

    def do_pandas_job(self):
        try:
            print("do_pandas_job")
            self.panda_ds.load_data(describ_columns=True)
            self.panda_ds.prepare_label_data()
        except Exception as e:
            print ("Exception do_pandas_job -> {}".format(e))

    def do_classifier_job(self):

        try:
            if isinstance(self.panda_ds.df, pd.DataFrame):

                self.classifier.df = self.panda_ds.df
                self.classifier.show_graph_it_distribution()
                self.classifier.get_features_and_labels()
                self.classifier.train_test_split()
                self.classifier.show_linear_svc(self.panda_ds.category_id_df)

        except Exception as e:
            print ("Exception do_classifier_job -> {}".format(e))

    @property
    def panda_ds(self):
        return self._pandas_df

    @panda_ds.setter
    def panda_ds(self, value):
        if value and isinstance(value, PandasDF):
            self._panda_ds = value

    @property
    def classifier(self):
        return self._classifier

    @classifier.setter
    def classifier(self, value):
        if value and isinstance(value, Classifier):
            self._classifier = value
