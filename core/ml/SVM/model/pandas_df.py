import os
from json import dumps, dump
import numpy as np
import pandas as pd

from core.ml.SVM.settings.settings import JSON_ID_CAT, COL_NAMES


class PandasDF(object):
    _logger = None
    _df = pd.DataFrame
    _src = None

    _category_id_df = None
    _id_to_category = None

    def __init__(self, **kw):

        print ("Inicializado PandasDF")

    def load_data(self, describ_columns=False, limit_size=True):
        '''

        :param src: fichero csv de la extraccion de averias
        :return: boolean
        '''
        try:

            self.df = pd.read_csv(self.src, encoding='utf8')
            if limit_size:
                self.df = self.df.sample(10000)

            print (" load_data ->  fichero src :  {} ".format( self.src))

            if describ_columns:
                for c in self.df.columns[2:]:
                   print("column {} \t {}\n\n".format(c, self.df.eval(c).describe()))

            return True
        except Exception as e:
            print ("Exception in load_data - > {}".format(e))

        return False

    def prepare_label_data(self):
        '''
            factorizacion de categoria
            se contruye el diccionario key: category_id / value: descripcion (human) (tipo de la IT)
            persiste en fichero .json el diccionario resultante
        :return:
        '''
        self.df = self.df.replace(np.nan, "0")
        self.df = self.df[COL_NAMES]
        print("Filtrando columnas:-> rows: {}, cols: {}".format(self.df.shape[0], self.df.shape[1]))
        self.df = self.df[pd.notnull(self.df['detalle'])]

        self.df.columns = COL_NAMES
        self.df['category_id'] = self.df['descripcion'].factorize()[0]
        print("Factorizando categoria_id")
        self.category_id_df = self.df[['descripcion', 'category_id']].drop_duplicates().sort_values('category_id')
        # construimos un diccinario
        self.id_to_category = dict(self.category_id_df[['category_id', 'descripcion']].values)

        self.json_to_file(self.id_to_category)
        print(
            "id_to_category: {}".format(dumps(self.id_to_category, indent=4)))

    def json_to_file(self, data):
        with open(JSON_ID_CAT, 'w') as outfile:
            dump(data, outfile)

    # <editor-fold desc="getters /Setter">

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        if value:
            self._logger = value

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, value):
        if value and os.path.exists(value):
            self._src = value

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, value):
        if isinstance(value, pd.DataFrame) and not value.empty:
            self._df = value

    @property
    def category_id_df(self):
        return self._category_id_df

    @category_id_df.setter
    def category_id_df(self, value):
        if isinstance(value, pd.DataFrame) and not value.empty:
            self._category_id_df = value

    @property
    def id_to_category(self):
        return self._id_to_category

    @id_to_category.setter
    def id_to_category(self, value):
        if value:
            self._id_to_category = value
    # </editor-fold>
