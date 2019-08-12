# features | label
import os
from   django.conf import settings

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

EXTRACCION_IT ="/home/ada/app/ApiADA/ApiADA/core/ml/SVM/averias_train_all_to_coremain/averias_train_all_to_coremain.csv"

MODELS_DEST_FOLDER= "/home/ada/app/ApiADA/ApiADA/core/ml/SVM/data_file_model"
MLP_JOBLIB = os.path.join(MODELS_DEST_FOLDER, "neuronal_model.joblib")
TF_IDF =os.path.join(MODELS_DEST_FOLDER, "tf_idf.joblib")
JSON_ID_CAT =  os.path.join(MODELS_DEST_FOLDER,"json_id_cat.json")

COL_NAMES = ['descripcion', 'detalle']
TEST_SIZE = 0.33
RANDOM_STATE = 0


